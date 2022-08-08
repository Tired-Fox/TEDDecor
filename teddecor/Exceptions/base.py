from functools import cached_property
from inspect import stack, FrameInfo
from os import get_terminal_size

from ..TED.markup import TED
from ..Util import slash

__all__ = ["BaseException", "HintedException", "MissingValueException"]


def get_len(string: str) -> int:
    from re import sub

    string = sub(r"\x1b\[(\d{0,2};?)*m|(?<!\\)\[.*\]", "", string)
    return len(string)


class Frame:
    """Parses FrameInfo into it's string representation."""

    def __init__(self, frame: FrameInfo):
        self._line = frame.lineno
        self._func = frame.function
        self._path = frame.filename
        self._module = frame.filename.split(slash())[-1].split(".")[0]

    def __str__(self) -> str:
        return f"*<[@F blue ~{self._path}]{self._module}[~ @F]:[@F yellow]{self._line}[@F]> in {self._func}*"


class BaseException(Exception):
    def __init__(self, message: str = "[@F red]*An unknown error occured*[@F]"):
        #  config: Dict[str, Dict[str, bool]] = {"stack": {"bold": True}}
        self._stack = [Frame(frame) for frame in stack()]
        self._message = TED.parse(message)
        super().__init__(self._message)
        self.slice_stack()

    def slice_stack(self) -> list:
        self._stack = self._stack[1:]

    @property
    def stack(self) -> str:
        return "\n".join("  " + str(frame) for frame in self._stack)

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return TED.parse(self.message)

    def throw(self, exits: bool = True) -> str:
        from sys import exit

        TED.print(self.stack)
        TED.print(self.message)

        if exits:
            exit(2)


class HintedException(BaseException):
    def __init__(
        self,
        value: str,
        index: int,
        hint: str,
        message: str = "Error with specific value",
    ):
        super().__init__(message)
        self.slice_stack()

        self._value = value
        self._hint = hint
        self._index = index

    @cached_property
    def error(self) -> str:
        width = get_terminal_size().columns
        # self._index = self._index % width if self._index > width else self._index
        arrow = "[@F yellow]↑[@F]"
        if ((self._index + len(self.hint + arrow) + 1) > width) and (
            get_len(self.hint + arrow) + 1 < self._index
        ):
            error = (
                f"  {self.value}\n "
                + " " * (self._index - get_len(self.hint) + get_len(arrow) - 2)
                + f"{self.hint} {arrow}"
            )
        else:
            error = f"  {self.value}\n " + " " * (self._index) + f"{arrow} {self.hint}"

        return error

    @property
    def value(self) -> str:
        return self._value

    @property
    def hint(self) -> str:
        return self._hint

    @property
    def index(self) -> int:
        return self._index

    def throw(self, exits: bool = True) -> str:
        from sys import exit

        TED.print("*Hinted Error:*")
        TED.print(self.stack, "\n")
        TED.print("*[@F red]" + self.message, "*:*")
        TED.print("*" + self.error)

        if exits:
            exit(3)


class MissingValueException(BaseException):
    def __init__(
        self,
        value: str,
        index: int,
        missing: str,
        message: str = "Missing Value",
    ):
        super().__init__(message)
        self.slice_stack()

        self._value = value
        self._index = index
        self._missing = missing

    @cached_property
    def error(self) -> str:
        return f"  {self.value[:self._index]}[@F red]{self._missing}[@F]{self.value[self._index:]}\n "

    @property
    def value(self) -> str:
        return self._value

    @property
    def index(self) -> int:
        return self._index

    def throw(self, exits: bool = True) -> str:
        from sys import exit

        TED.print("*Missing Value Error:*")
        TED.print(self.stack, "\n")
        TED.print("*[@F red]" + self.message, "*:*")
        TED.print("*" + self.error)

        if exits:
            exit(4)


def main():
    MissingValueException(
        value="Dog is out of control you know that right",
        index=42,
        missing="?",
        message="Missing Punctuation",
    ).throw(False)

    HintedException(
        value="Dog is out of control you know that right",
        index=42,
        hint="Missing the punctuation [@F green]?[@F]",
        message="Missing Punctuation",
    ).throw(False)


if __name__ == "__main__":
    main()
