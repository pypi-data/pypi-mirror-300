# menus.rofi.py
from __future__ import annotations

import logging
import shlex
import sys
from dataclasses import dataclass
from dataclasses import field
from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import Self

from pyselector import constants
from pyselector import extract
from pyselector import helpers
from pyselector.constants import UserCancel
from pyselector.key_manager import KeyManager

if TYPE_CHECKING:
    from pyselector.interfaces import MenuInterface

log = logging.getLogger(__name__)

ROFI_RETURN_CODE_START = 10
BULLET = '\u2022'


def remove_theme_str(args: list[str], value: str) -> list[str]:
    i = 0
    while i < len(args):
        if value in args[i] and args[i - 1] == '-theme-str':
            del args[i - 1 : i + 1]
            return args
        i += 1
    return args


@dataclass
class Args:
    _args: list[str] = field(default_factory=list)
    _message: list[str] = field(default_factory=list)

    def replace(self, arg: str, value: str) -> Self:
        idx = self._args.index(arg)
        self._args[idx + 1] = value
        return self

    def dimensions(self, w: int, h: int) -> Self:
        remove_theme_str(self._args, 'window {width:')
        remove_theme_str(self._args, 'window {height:')
        d = shlex.split(f"-theme-str 'window {{width: {w}; height: {h}; }}'")
        self.extend(d)
        return self

    def remove(self, s: str) -> None:
        for arg in self._args:
            if s in arg:
                self._args.remove(arg)
                break

    def exists(self, s: str) -> bool:
        return any(s in arg for arg in self._args)

    def extend(self, args: list[str]) -> None:
        self._args.extend(args)

    def save_append(self, s: str) -> None:
        args = self._args
        for arg in self._args:
            if s == arg:
                return
            if s in arg:
                args.remove(arg)
                break
        args.append(s)

    def prompt(self, s: str) -> Self:
        if '-p' in self._args:
            self.replace('-p', s)
            return self
        self.extend(shlex.split(f'-p {s}'))
        return self

    def mesg(self, s: str) -> Self:
        self._message.append(s)
        return self

    def lines(self, n: int) -> Self:
        if '-l' in self._args:
            self.replace('-l', str(n))
            return self
        self.extend(shlex.split(f'-l "{n}"'))
        return self

    def markup(self, b: bool) -> Self:
        if b:
            self._args.append('-markup-rows')
        else:
            self.remove('-markup-rows')
        return self

    def case_sensitive(self, b: bool) -> Self:
        if b:
            self._args.append('-case-sensitive')
        else:
            self._args.append('-i')
        return self

    def multi(self, b: bool) -> Self:
        if b:
            self._args.append('-multi-select')
        else:
            self.remove('-multi-select')
        return self

    def filter(self, s: str) -> Self:
        self.extend(shlex.split(f'-filter {s}'))
        return self

    def location(self, s: str) -> Self:
        loc = set_location(s)
        self.extend(shlex.split(f'-location {loc}'))
        return self

    def theme(self, s: str) -> Self:
        self.extend(shlex.split(f'-theme {s}'))
        return self

    def print(self) -> None:
        print(self._args)  # noqa: T201


class Options:
    def __init__(self, menu: MenuInterface):
        self.menu = menu

    def replace(self, arg: str, value: str) -> Self:
        idx = self.menu.args.index(arg)
        self.menu.args[idx + 1] = value
        return self

    def remove(self, s: str) -> None:
        for arg in self.menu.args:
            if s in arg:
                self.menu.args.remove(arg)
                break

    def greet(self, s: str) -> list[str]:
        return self.menu.args.append(s)

    def prompt(self, s: str) -> Self:
        if '-p' in self.menu.args:
            self.replace('-p', s)
            return self
        self.menu.args.extend(shlex.split(f'-p {s}'))
        return self

    def lines(self, n: int) -> Self:
        if '-l' in self.menu.args:
            self.replace('-l', str(n))
            return self
        self.menu.args.extend(shlex.split(f'-l "{n}"'))
        return self

    def add_override(self, key: str, value: str) -> Self:
        self.menu.args.extend(shlex.split(f"-theme-str '{key} {{ {value}; }}'"))
        return self

    def del_override(self, value: str) -> None:
        i = 0
        while i < len(self.menu.args):
            if value in self.menu.args[i] and self.menu.args[i - 1] == '-theme-str':
                del self.menu.args[i - 1 : i + 1]
                break
            i += 1

    def markup(self, b: bool) -> Self:
        if b:
            self.menu.args.append('-markup-rows')
        else:
            self.remove('-markup-rows')
        return self


def set_location(direction: str = 'center') -> str:
    """
    Specify where the window should be located. The numbers map to the
    following locations on screen:

        1 2 3
        8 0 4
        7 6 5

    Default: 0
    """
    try:
        location = {
            'upper-left': 1,
            'left': 8,
            'bottom-left': 7,
            'upper-center': 2,
            'center': 0,
            'bottom-center': 6,
            'upper-right': 3,
            'right': 4,
            'bottom-right': 5,
        }
        return str(location[direction])
    except KeyError as e:
        msg = 'location %s not found.\nchosse from %s'
        raise KeyError(msg, e, list(location.keys())) from e
        sys.exit(1)


class RofiBeta:
    def __init__(self) -> None:
        self.name = 'rofi'
        self.url = constants.HOMEPAGE_ROFI
        self.keybind = KeyManager()
        self.keybind.code_count = ROFI_RETURN_CODE_START
        self.args: list[str] = []
        self._message: list[str] = []
        self.opts = Options(self)

    @property
    def command(self) -> str:
        return helpers.check_command(self.name, self.url)

    def selection(
        self,
        items: list[Any] | tuple[Any] | None = None,
        preprocessor: Callable[..., Any] | None = None,
        **kwargs,
    ) -> tuple[Any, int]:
        if items is None:
            items = []

        args = self._build_args(**kwargs)
        selected, code = helpers.run(args, items, preprocessor)

        if not selected or code == UserCancel(1):
            return None, code

        if '-multi-select' in args:
            result = extract.items(items, selected, preprocessor)
        else:
            result = extract.item(items, selected, preprocessor)

        if not result:
            log.warning('result is empty')
            return selected, 1

        return result, code

    def _build_args(self, **kwargs) -> list[str]:
        args = shlex.split(self.command)
        args.append('-dmenu')
        args.append('-sync')
        args.extend(self.args)

        # Add custom keybindings
        for key in self.keybind.current:
            args.extend(shlex.split(f'-kb-custom-{key.id} {key.bind}'))
            if not key.hidden:
                self._message.append(f'{BULLET} Use <{key.bind}> {key.description}')

        if self._message:
            args.append('-mesg')
            args.append('\n'.join(self._message))
            self._message = []
        return args

    def prompt(
        self,
        items: list[Any] | tuple[Any] | None = None,
        case_sensitive: bool = False,
        multi_select: bool = False,
        prompt: str = constants.PROMPT,
        preprocessor: Callable[..., Any] | None = None,
        **kwargs,
    ) -> tuple[Any, int]:
        """Prompts the user with a rofi window containing the given items
           and returns the selected item and code.

        Args:
            items (Iterable[str, int], optional):  The items to display in the rofi window
            case_sensitive (bool, optional):       Whether or not to perform a case-sensitive search
            multi_select (bool, optional):         Whether or not to allow the user to select multiple items
            prompt (str, optional):                The prompt to display in the rofi window
            **kwargs:                              Additional keyword arguments.

        Keyword Args:
            lines    (int): The number of lines to display in the selection window.
            mesg     (str): A message to display at the top of the selection window.
            filter   (str): Filter the list by setting text in input bar to filter.
            location (str): The location of the selection window (e.g. "upper-left", "center" or "bottom-right").
            width    (str): The width of the selection window (e.g. 60%).
            height   (str): The height of the selection window (e.g. 50%).
            theme    (str): The path of the rofi theme to use.

        Returns:
            A tuple containing the selected item (str or list of str if `multi_select` enabled)
            and the return code (int).

        Return Code Value
            0: Row has been selected accepted by user.
            1: User cancelled the selection.
            10-28: Row accepted by custom keybinding.
        """
        # if items is None:
        #     items = []
        #
        # args = self._old_build_args(case_sensitive, multi_select, prompt, **kwargs)
        # selected, code = helpers._execute(args, items, preprocessor)
        #
        # if not selected or code == UserCancelSelection(1):
        #     return None, code
        #
        # if multi_select:
        #     result = extract.items(items, selected, preprocessor)
        # else:
        #     result = extract.item(items, selected, preprocessor)
        #
        # if not result:
        #     log.warning('result is empty')
        #     return selected, 1
        #
        # return result, code
        raise NotImplementedError
