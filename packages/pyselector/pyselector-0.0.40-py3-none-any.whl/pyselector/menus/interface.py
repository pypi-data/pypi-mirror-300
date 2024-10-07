# interface.py
from __future__ import annotations

from typing import TYPE_CHECKING
from typing import Any
from typing import Callable
from typing import NewType
from typing import Protocol

from src.pyselector import constants

if TYPE_CHECKING:
    from pyselector.key_manager import KeyManager

PromptReturn = tuple[Any, int]
UserConfirmsSelection = NewType('UserConfirmsSelection', int)
UserCancelSelection = NewType('UserCancelSelection', int)


class ExecutableNotFoundError(Exception):
    pass


class ArgsUtils:
    @staticmethod
    def replace(args: list[str], arg: str, value: str) -> list[str]:
        idx = args.index(arg)
        args[idx + 1] = value
        return args

    @staticmethod
    def remove(args: list[str], s: str) -> list[str]:
        for arg in args:
            if s in arg:
                args.remove(arg)
                return args
        return args

    @staticmethod
    def extend(args: list[str]) -> None:
        args.extend(args)

    @staticmethod
    def exists(args: list[str], s: str) -> bool:
        return any(s in arg for arg in args)


class Args:
    _args: list[str]
    utils: ArgsUtils


class MenuInterface(Protocol):
    name: str
    url: str
    keybind: KeyManager
    args: Args

    @property
    def command(self) -> str: ...

    def prompt(
        self,
        items: list[Any] | tuple[Any] | None = None,
        case_sensitive: bool = False,
        multi_select: bool = False,
        prompt: str = constants.PROMPT,
        preprocessor: Callable[..., Any] | None = None,
        **kwargs,
    ) -> tuple[Any, int]: ...

    def beta_prompt(self, **kwargs) -> str | None: ...

    def selection(
        self,
        items: list[Any] | tuple[Any] | None = None,
        preprocessor: Callable[..., Any] | None = None,
        **kwargs,
    ) -> tuple[Any, int]: ...
