from __future__ import annotations

import typing as t
from dataclasses import dataclass
from enum import Enum

from .base import UNKNOWN, Unknownish


@dataclass()
class Component:
    #: component type (valid for: all types)
    type: int
    #: the choices in the select, max 25 (valid for: Select Menus)
    options: t.List[SelectOption]
    #: a developer-defined identifier for the component, max 100 characters
    #: (valid for: Buttons, Select Menus)
    custom_id: Unknownish[str] = UNKNOWN
    #: whether the component is disabled, default false (valid for: Buttons,
    #: Select Menus)
    disabled: Unknownish[bool] = UNKNOWN
    #: one of button styles (valid for: Buttons)
    style: Unknownish[int] = UNKNOWN
    #: text that appears on the button, max 80 characters (valid for: Buttons)
    label: Unknownish[str] = UNKNOWN
    #: name, id, and animated (valid for: Buttons)
    emoji: Unknownish[t.Dict[str, object]] = UNKNOWN
    #: a url for link-style buttons (valid for: Buttons)
    url: Unknownish[str] = UNKNOWN
    #: custom placeholder text if nothing is selected, max 100 characters
    #: (valid for: Select Menus)
    placeholder: Unknownish[str] = UNKNOWN
    #: the minimum number of items that must be chosen; default 1, min 0, max
    #: 25 (valid for: Select Menus)
    min_values: Unknownish[int] = UNKNOWN
    #: the maximum number of items that can be chosen; default 1, max 25
    #: (valid for: Select Menus)
    max_values: Unknownish[int] = UNKNOWN
    #: a list of child components (valid for: Action Rows)
    components: Unknownish[t.List[Component]] = UNKNOWN


class ComponentTypes(Enum):
    #: A container for other components
    ACTION_ROW = 1
    #: A button object
    BUTTON = 2
    #: A select menu for picking from choices
    SELECT_MENU = 3


@dataclass()
class Button:
    #: 2 for a button
    type: int
    #: one of button styles
    style: int
    #: text that appears on the button, max 80 characters
    label: Unknownish[str] = UNKNOWN
    #: name, id, and animated
    emoji: Unknownish[t.Dict[str, object]] = UNKNOWN
    #: a developer-defined identifier for the button, max 100 characters
    custom_id: Unknownish[str] = UNKNOWN
    #: a url for link-style buttons
    url: Unknownish[str] = UNKNOWN
    #: whether the button is disabled (default false)
    disabled: Unknownish[bool] = UNKNOWN


class ButtonStyle(Enum):
    PRIMARY = 1
    SECONDARY = 2
    SUCCESS = 3
    DANGER = 4
    LINK = 5


@dataclass()
class SelectMenu:
    #: 3 for a select menu
    type: int
    #: a developer-defined identifier for the button, max 100 characters
    custom_id: str
    #: the choices in the select, max 25
    options: t.List[SelectOption]
    #: custom placeholder text if nothing is selected, max 100 characters
    placeholder: Unknownish[str] = UNKNOWN
    #: the minimum number of items that must be chosen; default 1, min 0, max
    #: 25
    min_values: Unknownish[int] = UNKNOWN
    #: the maximum number of items that can be chosen; default 1, max 25
    max_values: Unknownish[int] = UNKNOWN
    #: disable the select, default false
    disabled: Unknownish[bool] = UNKNOWN


@dataclass()
class SelectOption:
    #: the user-facing name of the option, max 25 characters
    label: str
    #: the dev-define value of the option, max 100 characters
    value: str
    #: an additional description of the option, max 50 characters
    description: Unknownish[str] = UNKNOWN
    #: id, name, and animated
    emoji: Unknownish[t.Dict[str, object]] = UNKNOWN
    #: will render this option as selected by default
    default: Unknownish[bool] = UNKNOWN
