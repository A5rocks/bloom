from __future__ import annotations

import attr
import bloom.substrate
import enum
import typing
import bloom.models.base as base_models
import bloom.models.guild as guild_models
import bloom.models.user as user_models
import bloom.models.gateway as gateway_models
import collections
import weakref


class CacheFlag(enum.Flag):
    NONE = 0
    MEMBERS = enum.auto()
    USERS = enum.auto()
    GUILDS = enum.auto()

    ALL = MEMBERS | USERS | GUILDS


@attr.frozen(kw_only=True)
class CachedGuild(guild_models.Guild):
    # FIXME: when I make this more an ADT, this will violate LSP
    members: base_models.UNKNOWN_TYPE = base_models.UNKNOWN
    presences: base_models.UNKNOWN_TYPE = base_models.UNKNOWN

    @classmethod
    def from_guild(cls, guild: guild_models.Guild) -> CachedGuild:
        attributes = attr.asdict(guild, recurse=False)
        attributes.update({
            'members': base_models.UNKNOWN,
            'presences': base_models.UNKNOWN
        })
        return cls(
            **attributes
        )


@attr.define()
class Cache:
    substrate: bloom.substrate.Substrate
    wants: CacheFlag = CacheFlag.NONE

    _events: typing.Dict[
        typing.Type[typing.Any],
        typing.Callable[[typing.Any], None]
    ] = attr.ib(init=False)

    # resources

    users: typing.MutableMapping[
        base_models.Snowflake,
        user_models.User
    ] = attr.Factory(dict)

    members: typing.MutableMapping[
        base_models.Snowflake,
        typing.MutableMapping[
            base_models.Snowflake,
            guild_models.GuildMember
        ]
    ] = attr.Factory(lambda: collections.defaultdict(dict))

    guilds: typing.MutableMapping[
        base_models.Snowflake,
        CachedGuild
    ] = attr.Factory(dict)

    # lowpowered `Member` for association
    _guilds_to_users: typing.MutableMapping[
        base_models.Snowflake,
        typing.List[base_models.Snowflake]
    ] = attr.Factory(dict)
    _users_to_guilds: typing.MutableMapping[
        base_models.Snowflake,
        typing.List[base_models.Snowflake]
    ] = attr.Factory(lambda: collections.defaultdict(list))

    def __attrs_post_init__(self) -> None:
        self._events = {}

        if CacheFlag.USERS in self.wants and CacheFlag.MEMBERS in self.wants:
            # users should be a weak ref dict
            self.users = weakref.WeakValueDictionary()

        if CacheFlag.USERS in self.wants or CacheFlag.MEMBERS in self.wants:
            self._events[gateway_models.GuildMemberAddEvent] = self._guild_member_add
            self._events[gateway_models.GuildMemberUpdateEvent] = self._guild_member_update
            self._events[gateway_models.GuildMemberRemoveEvent] = self._guild_member_remove

        if CacheFlag.MEMBERS in self.wants and CacheFlag.USERS not in self.wants:
            # TODO: better errors
            raise Exception(
                'You cannot cache members without users, unless you make a custom cache.'
            )

        self._events[gateway_models.GuildCreateEvent] = self._guild_create
        self._events[gateway_models.GuildUpdateEvent] = self._guild_update
        self._events[gateway_models.GuildDeleteEvent] = self._guild_delete

    async def run(self) -> None:
        async with self.substrate.register(object, None) as chan:
            async for event in chan:
                self._events.get(type(event), lambda _: None)(event)

    def _guild_create(self, evt: gateway_models.GuildCreateEvent) -> None:
        if CacheFlag.GUILDS in self.wants:
            self.guilds[evt.id] = CachedGuild.from_guild(evt)

        if (
            CacheFlag.MEMBERS in self.wants
            and not isinstance(evt.members, base_models.UNKNOWN_TYPE)
        ):
            for member in evt.members:
                # `Member#user` is not included on `MESSAGE_CREATE` /
                # `MESSAGE_DELETE`...
                # this is neither of those.

                # TODO: cattr custom converter for both of those events to
                # remove this
                member_user: user_models.User = member.user  # type: ignore[assignment]
                self.members[evt.id][member_user.id] = member

        if CacheFlag.USERS in self.wants and not isinstance(evt.members, base_models.UNKNOWN_TYPE):
            ids = []

            for member in evt.members:
                # `Member#user` is not included on `MESSAGE_CREATE` /
                # `MESSAGE_DELETE`...
                # this is neither of those.

                # TODO: cattr custom converter for both of those events to
                # remove this
                user: user_models.User = member.user  # type: ignore[assignment]
                self.users[user.id] = user
                ids.append(user.id)
                self._users_to_guilds[user.id].append(evt.id)

            self._guilds_to_users[evt.id] = ids

    def _guild_update(self, evt: gateway_models.GuildUpdateEvent) -> None:
        if CacheFlag.GUILDS in self.wants:
            self.guilds[evt.id] = CachedGuild.from_guild(evt)

    def _guild_delete(self, evt: gateway_models.GuildDeleteEvent) -> None:
        if not evt.unavailable:
            if CacheFlag.GUILDS in self.wants:
                del self.guilds[evt.id]

            if CacheFlag.MEMBERS:
                del self.members[evt.id]

            # weak ref dicts won't need this.
            if CacheFlag.USERS in self.wants and CacheFlag.MEMBERS not in self.wants:
                for user_id in self._guilds_to_users[evt.id]:
                    self._users_to_guilds[user_id].remove(evt.id)
                    if not self._users_to_guilds[user_id]:
                        del self._users_to_guilds[user_id]
                        del self.users[user_id]

                del self._guilds_to_users[evt.id]

    def _guild_member_add(self, evt: gateway_models.GuildMemberAddEvent) -> None:
        # `Member#user` is not included on `MESSAGE_CREATE` /
        # `MESSAGE_DELETE`...
        # this is neither of those.

        # TODO: cattr custom converter for both of those events to
        # remove this
        user: user_models.User = evt.user  # type: ignore[assignment]

        if CacheFlag.USERS in self.wants:
            self.users[user.id] = user
            self._guilds_to_users[evt.guild_id].append(user.id)
            self._users_to_guilds[user.id].append(evt.guild_id)

        if CacheFlag.MEMBERS in self.wants:
            self.members[evt.guild_id][user.id] = evt

    def _guild_member_update(self, evt: gateway_models.GuildMemberUpdateEvent) -> None:
        user: user_models.User = evt.user

        if CacheFlag.USERS in self.wants:
            self.users[user.id] = user

        if CacheFlag.MEMBERS in self.wants:
            attributes = attr.asdict(evt, recurse=False)
            del attributes['guild_id']
            try:
                self.members[evt.guild_id][user.id] = attr.evolve(
                    self.members[evt.guild_id][user.id],
                    **attributes
                )
            except KeyError:
                # offline member that was updated in a guild too large...
                # nothing can be done.
                pass

    def _guild_member_remove(self, evt: gateway_models.GuildMemberRemoveEvent) -> None:
        # weak ref dict takes care of this
        if CacheFlag.USERS in self.wants and CacheFlag.MEMBERS not in self.wants:
            self._guilds_to_users[evt.guild_id].remove(evt.user.id)
            self._users_to_guilds[evt.user.id].remove(evt.guild_id)
            if not self._users_to_guilds[evt.user.id]:
                del self._users_to_guilds[evt.user.id]
                del self.users[evt.user.id]

        if CacheFlag.MEMBERS in self.wants:
            try:
                del self.members[evt.guild_id][evt.user.id]
            except KeyError:
                # offline member that left in a guild too large...
                # nothing can be done.
                pass
