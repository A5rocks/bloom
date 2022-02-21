from __future__ import annotations

import enum
import typing

import attr

from bloom.ll.models.base import UNKNOWN, Unknownish

# docs in this module are copied from the Discord Documentation


class ComponentTypes(enum.Enum):
    #: A container for other components
    ACTION_ROW = 1
    #: A button object
    BUTTON = 2
    #: A select menu for picking from choices
    SELECT_MENU = 3
    #: A text input object
    TEXT_INPUT = 4


@attr.frozen(kw_only=True)
class ActionRow:
    #: 1 for an action row
    type: typing.Literal[1, ComponentTypes.ACTION_ROW]
    # a list of child components
    components: typing.List[Component]


@attr.frozen(kw_only=True)
class Button:
    #: 2 for a button
    type: typing.Literal[2, ComponentTypes.BUTTON]
    #: one of button styles
    style: int
    #: text that appears on the button, max 80 characters
    label: Unknownish[str] = UNKNOWN
    #: name, id, and animated
    emoji: Unknownish[typing.Dict[str, typing.Any]] = UNKNOWN
    #: a developer-defined identifier for the button, max 100 characters
    custom_id: Unknownish[str] = UNKNOWN
    #: a url for link-style buttons
    url: Unknownish[str] = UNKNOWN
    #: whether the button is disabled (default false)
    disabled: Unknownish[bool] = UNKNOWN


class ButtonStyle(enum.Enum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


@attr.frozen(kw_only=True)
class SelectMenu:
    #: 3 for a select menu
    type: typing.Literal[3, ComponentTypes.SELECT_MENU]
    #: a developer-defined identifier for the button, max 100 characters
    custom_id: str
    #: the choices in the select, max 25
    options: typing.List[SelectOption]
    #: custom placeholder text if nothing is selected, max 100 characters
    placeholder: Unknownish[str] = UNKNOWN
    #: the minimum number of items that must be chosen; default 1, min 0, max
    #: 25
    min_values: Unknownish[int] = UNKNOWN
    #: the maximum number of items that can be chosen; default 1, max 25
    max_values: Unknownish[int] = UNKNOWN
    #: disable the select, default false
    disabled: Unknownish[bool] = UNKNOWN


@attr.frozen(kw_only=True)
class SelectOption:
    #: the user-facing name of the option, max 100 characters
    label: str
    #: the dev-define value of the option, max 100 characters
    value: str
    #: an additional description of the option, max 100 characters
    description: Unknownish[str] = UNKNOWN
    #: id, name, and animated
    emoji: Unknownish[typing.Dict[str, typing.Any]] = UNKNOWN
    #: will render this option as selected by default
    default: Unknownish[bool] = UNKNOWN


@attr.frozen(kw_only=True)
class TextInput:
    #: 4 for a text input
    type: typing.Literal[4, ComponentTypes.TEXT_INPUT]
    #: a developer-defined identifier for the input, max 100 characters
    custom_id: str
    #: the Text Input Style
    style: int
    #: the label for this component
    label: str
    #: the minimum input length for a text input, min 0, max 4000
    min_length: Unknownish[int] = UNKNOWN
    #: the maximum input length for a text input, min 1, max 4000
    max_length: Unknownish[int] = UNKNOWN
    #: whether this component is required to be filled, default true
    required: Unknownish[bool] = UNKNOWN
    #: a pre-filled value for this component, max 4000 characters
    value: Unknownish[str] = UNKNOWN
    #: custom placeholder text if the input is empty, max 100 characters
    placeholder: Unknownish[str] = UNKNOWN


class TextInputStyle(enum.IntEnum):
    #: A single-line input
    SHORT = 1
    #: A multi-line input
    PARAGRAPH = 2


Component = typing.Union[ActionRow, Button, SelectMenu, TextInput]
