from __future__ import annotations

import sys
from io import TextIOWrapper
from typing import Any, Callable, Optional, TextIO

from teddecor import TED

from .encoding import encodings
from .LL import LL


class Log:
    encoding: str
    """The encoding to output with. Default utf-8"""

    def __init__(
        self,
        output: TextIO | TextIOWrapper = sys.stdout,
        level: str = LL.INFO,
        compare: Callable = LL.ge,
        encoding: str = "utf-8",
    ):
        self.config(output, level, compare, encoding)
        self.buffer = []

    def config(
        self,
        output: TextIO | TextIOWrapper,
        level: str,
        compare: Callable,
        encoding: str = "utf-8",
    ):
        self.output(output)
        self.level(level)
        self.comparator(compare)
        self.encode(encoding)

    def output(self, output: TextIO | TextIOWrapper):
        """Set where logging should be printed/outputed to.

        Args:
            output (TextIO): The TextIO object to output to.

        Raises:
            TypeError: Raised when output is not a TextIO object.
        """
        if isinstance(output, TextIO) or isinstance(output, TextIOWrapper):
            self._output = output
        else:
            raise TypeError(
                f"output was {type(output)} must be of type {TextIO} or {TextIOWrapper}"
            )

        return self

    def level(self, level: str):
        """Set the level at which logging should occur.

        Args:
            level (str): `LL.{DEBUG,INFO,WARNING,IMPORTANT,ERROR}`

        Raises:
            TypeError: Raised when level is not a string
            TypeError: Raised when level is not an attribute in `<class 'LL'>`
        """
        if isinstance(level, str):
            if level in LL.all():
                self._level = level
            else:
                raise TypeError(
                    f"level must be an attribute in <class 'LL'>. Valid options include {', '.join(LL.all())}"
                )
        else:
            raise TypeError(f"level was {type(level)} must be of type <class 'str'>")

        return self

    def comparator(self, compare: Callable):
        """Set the compare function for logging. Determine if logs of level that are gt, lt, eq, le, ge should be logged.

        Args:
            compare (Callable): `LL.{gt,lt,eq,ge,le}`

        Raises:
            TypeError: Raised when compare is not Callable
            TypeError: Raised when compare isn't a function from `<class 'LL'>`
        """
        if isinstance(compare, Callable):
            if (
                compare in [LL.gt, LL.lt, LL.eq, LL.le, LL.ge]
                or compare.__name__ == "within"
            ):
                self._compare = compare
            else:
                raise TypeError(
                    "compare must be one of the compare functions in LL. Can be LL.gt, LL.lt, LL.eq, LL.le, LL.ge, or LL.within"
                )
        else:
            raise TypeError(f"compare was {type(compare)} must be of type Callable")

        return self

    def encode(self, encoding: str):
        """Set the encoding type that is used."""
        if isinstance(encoding, str):
            if encoding.replace("-", "_") in encodings:
                self._encoding = encoding
            else:
                raise TypeError(
                    "Invalid encoding type. Valid encoding types can be found at https://docs.python.org/3.7/library/codecs.html#standard-encodings"
                )
        else:
            raise TypeError(
                f"encoding was {type(encoding)} must be of type <class 'str'>"
            )

        return self

    def flush(self, file: Optional[TextIOWrapper] = None):
        """Takes all values stored in the log buffer
        and flushes them to the TextIO output or stdout as default.
        """

        if file is not None:
            for log in self.buffer:
                file.write(TED.strip(log))
        else:
            for log in self.buffer:
                self._output.write(log)
            self._output.flush()
        
        self.buffer = []

        return self

    @classmethod
    def path(cls, *args: str, clr: str = "yellow", spr: str = " > ") -> str:
        """Takes all the arguments, segments of path, and combines them with the given seperator and color.

        Args:
            clr (int): The color to apply to each segment of the path
            spr (str): The seperator between each segement of the path

        Returns:
            str: The formatted string
        """
        return f"{spr}".join([TED.parse(f"[@F {clr}]{arg}[@F] ") for arg in args])

    def __out(self, *args: str, label: str, clr: str, gaps: Optional[list[bool]] = None):
        """Base function for formatting a log output.

        Args:
            label (str): The label to apply to the output
            clr (str): Color to give the label
            gaps (Optional[list[bool]], optional): Whether to put a one line
            space on the top, bottom, or both. Defaults to neither. Array indexes
            equivelant to [top, bottom]. If you enter a single bool value it is
            used for both top and bottom. Ex: `[False]` == `[False,  False]`
        """
        gaps = gaps or []

        if len(gaps) == 1:
            gaps.append(gaps[0])

        if len(gaps) == 2 and gaps[0]:
            self.buffer.append("\n")

        message = []
        for arg in args:
            if isinstance(arg, list):
                message.extend([str(a) for a in arg])
            else:
                message.append(str(arg))

        message = " ".join(message)
        message += "\n" if not message.endswith("\n") else ""

        self.buffer.append(TED.parse(f"*\[[@F{clr}]{label}[@F]\]* ") + message)

        if len(gaps) == 2 and gaps[1]:
            self.buffer.append("\n")
            
        return self

    def debug(self, *args: Any):
        """Debug log event."""

        if self._compare(LL.DEBUG, self._level):
            return self.__out(*args, label="Debug", clr="white")
        return self

    def info(self, *args: Any):
        """Info log event."""

        if self._compare(LL.INFO, self._level):
            return self.__out(*args, label="Info", clr="cyan")
        return self

    def warning(self, *args: Any):
        """Warning log event."""

        if self._compare(LL.WARNING, self._level):
            return self.__out(*args, label="Warning", clr="yellow")
        return self

    def important(self, *args: Any):
        """Important log event."""

        if self._compare(LL.IMPORTANT, self._level):
            return self.__out(*args, label="Important", clr="magenta")
        return self

    def success(self, *args: Any):
        """Success log event."""

        if self._compare(LL.SUCCESS, self._level):
            return self.__out(*args, label="Success", clr="green")
        return self

    def error(self, *args: Any):
        """Error log event."""

        if self._compare(LL.ERROR, self._level):
            return self.__out(*args, label="Error", clr="red")
        return self

    def custom(
        self,
        *args: Any,
        label: str = LL.CUSTOM,
        clr: str = "blue",
        gaps: list[bool] = [False],
    ):
        """Custom log event. This gives control over label, color, message, and gaps, individually.

        Args:
            label (str, optional): Label to apply before the message. Defaults to "Custom".
            clr (str, optional): Color of the label. Defaults to "blue".
            gaps (list[bool], optional): Gaps to apply to the top and bottom of the log.
            Defaults to [False].
        """

        if self._compare(LL.CUSTOM, self._level):
            return self.__out(*args, label=label, clr=clr, gaps=gaps)
        return self

    def message(self, *args: Any):
        """A generic message to be logged without a label."""

        message = []
        for arg in args:
            if isinstance(arg, list):
                message.extend([str(a) for a in arg])
            else:
                message.append(str(arg))

        message = " ".join(message)
        message += "\n" if not message.endswith("\n") else ""

        self.buffer.append(message)
        return self
        


Logger = Log(level=LL.INFO)
"""Global instance of a logger."""
