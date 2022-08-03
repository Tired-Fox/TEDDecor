from __future__ import annotations
from functools import cached_property
from typing import Union

from babel import parse_locale
from formatting import build_color, ColorType, LINK


class Token:
    def __repr__(self) -> str:
        return f"<{type(self).__name__}: {self._markup}, {self.value}>"


class HLink(Token):
    def __init__(self, markup: str) -> None:
        self._markup = markup.strip()
        self._closing = False
        self._value = self.parse_link()

    def parse_link(self) -> str:
        """Determine if the token is a closing link token and assign _closing accordingly.

        Returns:
            str: The value of the token based on if the token is closing
        """
        if len(self._markup) == 1:
            self._closing = True
            return LINK.CLOSE
        elif len(self._markup) > 1:
            return LINK.OPEN(self._markup[1:])

    @property
    def value(self) -> str:
        """Value of the token."""
        return self._value

    @value.setter
    def value(self, value: str) -> str:
        self._value = value

    @property
    def closing(self) -> bool:
        """True if this link token is a closing link token."""
        return self._closing

    def __str__(self) -> str:
        return self.value


class Text(Token):
    def __init__(self, markup: str) -> None:
        self._markup: str = markup

    @cached_property
    def value(self) -> str:
        return self._markup

    def __repr__(self) -> str:
        return f"<{type(self).__name__}: '{self._markup}'>"

    def __str__(self) -> str:
        return self._markup


class Color(Token):
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
        return f"{';'.join(self._colors)}"

    @cached_property
    def type_str(self) -> str:
        if len(self._type) == 1 and self._type[0] == ColorType.FG:
            return "FG"
        elif len(self._type) == 1 and self._type[0] == ColorType.BG:
            return "BG"
        else:
            return "FG + BG"

    @property
    def colors(self) -> list[int]:
        return self._colors

    @colors.setter
    def colors(self, colors: list[int]) -> None:
        self._colors = colors

    @property
    def type(self) -> ColorType:
        return self._type

    def pretty(self) -> str:
        return f"<Color:\n  focus: {self.type_str}\n  value: {repr(self.value)}\n>"

    def __repr__(self) -> str:
        return f"<Color: {self.type}, {repr(self.value)}>"

    def __str__(self) -> str:
        return self.value


class Bold(Token):
    def __init__(self, value: str) -> None:
        self._markup: str = "*"
        self._value: str = value

    @property
    def value(self) -> int:
        return self._value

    def __str__(self) -> str:
        return f"\x1b[{self.value}m"


class Underline(Token):
    def __init__(self, value: str) -> None:
        self._markup: str = "_"
        self._value: str = value

    @property
    def value(self) -> int:
        return self._value

    def __str__(self) -> str:
        return f"\x1b[{self.value}m"


class Formatter(Token):
    def __init__(self):
        self._fg = None
        self._bg = None
        self._underline = None
        self._bold = None

    @property
    def color(self) -> str:
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
        return self._bold

    @bold.setter
    def bold(self, bold: Bold) -> None:
        self._bold = bold if self._bold is None else None

    @property
    def underline(self) -> Union[Underline, None]:
        return self._underline

    @bold.setter
    def underline(self, underline: Underline) -> None:
        self._underline = underline if self._underline is None else None

    def is_empty(self) -> bool:
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
