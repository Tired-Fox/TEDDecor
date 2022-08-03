from __future__ import annotations
from functools import cached_property
from typing import Union
from .formatting import build_color, ColorType


class Token:
    """Generic base class that has a default repr."""

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: {self._markup}, {self.value}>"


class Text(Token):
    """Plain text token."""

    def __init__(self, markup: str) -> None:
        self._markup: str = markup

    @cached_property
    def value(self) -> str:
        """Fomatted value of the tokens markup."""
        return self._markup

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: '{self._markup}'>"

    def __str__(self) -> str:
        return self._markup


class Color(Token):
    """A color tokens that is either hex, xterm, rgb, or predefined."""

    def __init__(
        self, markup: str, colors: list[int] = None, ctype: ColorType = None
    ) -> None:

        self._markup: str = markup
        self._type, self._colors = build_color(markup)
        if colors is not None:
            self._colors = colors
        if ctype is not None:
            self._type = ctype

    @cached_property
    def value(self) -> str:
        """Fomatted value of the tokens markup."""
        return f"{';'.join(self._colors)}"

    @cached_property
    def type_str(self) -> str:
        """Redable type of the color."""
        if len(self._type) == 1 and self._type[0] == ColorType.FG:
            return "FG"
        elif len(self._type) == 1 and self._type[0] == ColorType.BG:
            return "BG"
        else:
            return "FG + BG"

    @property
    def colors(self) -> list[int]:
        """List of color codes."""
        return self._colors

    @colors.setter
    def colors(self, colors: list[int]) -> None:
        self._colors = colors

    @property
    def type(self) -> ColorType:
        """The colors type; fg, bg, or both."""
        return self._type

    def __repr__(self) -> str:
        """String representation of the class when printing class."""
        return f"<Color: {self.type}, {repr(self.value)}>"

    def __str__(self) -> str:
        """Full ansi representation of the token."""
        return f"\x1b[{';'.join(self._colors)}m"


class Bold(Token):
    def __init__(self, value: str) -> None:
        self._markup: str = "*"
        self._value: str = value

    @property
    def value(self) -> int:
        """The ansi code for the markup."""
        return self._value

    def __str__(self) -> str:
        """Full ansi representation of the token."""
        return f"\x1b[{self.value}m"


class Underline(Token):
    def __init__(self, value: str) -> None:
        self._markup: str = "_"
        self._value: str = value

    @property
    def value(self) -> int:
        """The ansi code for the markup."""
        return self._value

    def __str__(self) -> str:
        """Full ansi representation of the token."""
        return f"\x1b[{self.value}m"


class Formatter(Token):
    """A class used to combine format tokens that are next to eachother."""

    def __init__(self):
        self._fg = None
        self._bg = None
        self._underline = None
        self._bold = None

    @property
    def color(self) -> str:
        """The colors current in the format"""
        return f"{self._fg};{self._bg}"

    @color.setter
    def color(self, color: Color) -> None:
        if color.type == [ColorType.FG]:
            self._fg = color
        elif color.type == [ColorType.BG]:
            self._bg = color
        elif color.type == ColorType.BOTH:
            self._fg = Color("", [color.colors[0]], [ColorType.FG])
            self._bg = Color("", [color.colors[1]], [ColorType.BG])

    @property
    def bold(self) -> Union[Bold, None]:
        """The bold toggle currently in the format."""
        return self._bold

    @bold.setter
    def bold(self, bold: Bold) -> None:
        self._bold = bold if self._bold is None else None

    @property
    def underline(self) -> Union[Underline, None]:
        """The underline toggle currently in the format."""
        return self._underline

    @bold.setter
    def underline(self, underline: Underline) -> None:
        self._underline = underline if self._underline is None else None

    def is_empty(self) -> bool:
        """True if all of fg, bg, underline, and bold are None."""
        return (
            self._fg is None
            and self._bg is None
            and self._underline is None
            and self._bold is None
        )

    def __str__(self) -> str:
        values = []
        if self._bold is not None:
            values.append(self._bold.value)
        if self._underline is not None:
            values.append(self._underline.value)
        if self._fg is not None:
            values.append(self._fg.value)
        if self._bg is not None:
            values.append(self._bg.value)

        if len(values) > 0:
            return f"\x1b[{';'.join(str(value) for value in values)}m"
        else:
            return ""

    def __repr__(self) -> str:
        return f"<Format: {repr(str(self))}>"