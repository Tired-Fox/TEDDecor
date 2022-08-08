from functools import cached_property
from inspect import stack, FrameInfo
from os import get_terminal_size

from ..TED.markup import TED
from ..Util import slash

__all__ = ["BaseException", "HintedException", "MissingValueException"]


def get_len(string: str) -> int:
    """Get the length of a string with TED markup removed.

    Args:
        string (str): The string to get the length of

    Returns:
        int: The actual length of the string with inline markup
    """
    from re import sub

    string = sub(r"\x1b\[(\d{0,2};?)*m|(?<!\\)\[.*\]|(?<!\\)\*|(?<!\\)_", "", string)
    return len(string)


class Frame:
    """Parses FrameInfo into it's string representation."""

    def __init__(self, frame: FrameInfo):
        self._line = frame.lineno
        self._func = frame.function
        self._path = frame.filename
        self._module = frame.filename.split(slash())[-1].split(".")[0]

    def __str__(self) -> str:
        return f"<[@F blue ~{self._path}]{self._module}[~ @F]:[@F yellow]{self._line}[@F]> in {self._func}"


class BaseException(Exception):
    """Base exception that uses TED markup. It will parse and clean up the stack trace along with printing a custom message.

    Note:
        The TEDDecor exceptions have two ways of calling them:

        1. raise the exception as you would any other
        2. Use the included throw method
            * Will be like raise but use the custom pretty stack trace
            * Will also allow for the exception to be used like an error and display the result and continue without a try except.
    """

    def __init__(self, message: str = "An unknown error occured"):
        #  config: Dict[str, Dict[str, bool]] = {"stack": {"bold": True}}
        self._stack = [Frame(frame) for frame in stack()]
        self._message = message
        super().__init__(TED.parse(message))
        self.slice_stack()

    def slice_stack(self) -> list:
        """Removes the part of the stack trace that includes this exceptions processing.

        Returns:
            list: The updated stack trace
        """
        self._stack = self._stack[1:]

    @property
    def stack(self) -> list[str]:
        """Gets the stack trace as a list of type str instead of type Frame."""
        return [str(frame) for frame in self._stack]

    @property
    def message(self) -> str:
        """Get the error message."""
        return self._message

    def __str__(self) -> str:
        """Only used when class is called with raise"""
        return TED.parse(self.message)

    def throw(self, exits: bool = True) -> str:
        """Custom throw method that allows for more custom output.

        Args:
            exits (bool, optional): Whether the throw method should exit like raise would. Defaults to True.

        Returns:
            str: The output that would be to the screen if exits, else None
        """
        if exits:
            from sys import exit

            TED.print("*" + self.stack)
            TED.print("[@ red]*" + self.message)
            exit(2)
        else:
            output = [TED.parse(self.stack), TED.parse(self.message)]
            return "\n".join(output)


class HintedException(BaseException):
    """This exception has a hint. In this case this means that the exception points to a part of a string and describes the problem.

    Example:
        Hint Exception:
          Are you having a good day
                                   ↑ You must end sentances with punctuation
    """

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
        """The combination of the string that is being hinted to and the hint.
        Will automatically adjust for terminal width.
        """
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
        """The value to be hinted too."""
        return self._value

    @property
    def hint(self) -> str:
        """The values hint."""
        return self._hint

    @property
    def index(self) -> int:
        """At what index of the value that is hinted to should the hint be placed.
        This is where the arrow will appear.
        """
        return self._index

    def throw(self, exits: bool = True) -> str:
        """Custom throw method that allows for more custom output.

        Args:
            exits (bool, optional): Whether the throw method should exit like raise would. Defaults to True.

        Returns:
            str: The output that would be to the screen if exits, else None
        """
        if exits:
            from sys import exit

            TED.print("*Hinted Error:*")
            TED.print("*" + self.stack, "\n")
            TED.print("*[@F red]" + self.message + "*:*")
            TED.print("*" + self.error)
            exit(3)
        else:
            output = [TED.parse("*Hinted Error:*")]
            output.append(TED.parse("*" + self.stack))
            output.append(TED.parse("*[@F red]" + self.message + "*:*"))
            output.append(TED.parse("*" + self.error))
            return "\n".join(output)


class MissingValueException(BaseException):
    """This exception is to point out a missing value.
    In the example below, ` `, indicates text that is injected as a missing value.

    Example:
        Missing punctuation:
           Are you haveing a good day`?`
    """

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
        """The value with the injected missing value."""
        return f"  {self.value[:self._index]}[@F red]{self._missing}[@F]{self.value[self._index:]}\n "

    @property
    def value(self) -> str:
        """The value that is missing something."""
        return self._value

    @property
    def missing(self) -> str:
        """What is missing from the value."""
        return self._missing

    @property
    def index(self) -> int:
        """The index where the value should be injected."""
        return self._index

    def throw(self, exits: bool = True) -> str:
        """Custom throw method that allows for more custom output.

        Args:
            exits (bool, optional): Whether the throw method should exit like raise would. Defaults to True.

        Returns:
            str: The output that would be to the screen if exits, else None
        """
        if exits:
            from sys import exit

            TED.print("*Missing Value Error:*")
            TED.print("*" + self.stack + "\n")
            TED.print("*[@F red]" + self.message + "*:*")
            TED.print("*" + self.error)

            exit(4)
        else:
            output = [TED.parse("*Missing Value Error:*")]
            output.append(TED.parse("*" + self.stack + "\n"))
            output.append(TED.parse("*[@F red]" + self.message + "*:*"))
            output.append(TED.parse("*" + self.error))
            return "\n".join(output)
