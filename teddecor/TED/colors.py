"""Colors

Colors must be RGB, Xterm index, predefined, or hex.

* RGB = 255,255,255 ... `[@F 255,255,255]`
* Xterm = 0-255 ... `[@B 123]`
* hex = #aaa or #aaaaaa ... `[@F #abc]` or `[@B #abcabc]`
* predefined = black, red, green, yellow, blue, magenta, cyan, and white ... `[@F green]`

Function macros can be of types rainbow, gradient, esc, and repr

* rainbow takes a string and returns a rainbow formatted string
* gradient is more complex. It takes a comma seperated string with the format {color n}...,string.
    * All but last value is the color value. Must have at least two colors which are hex.
    * Finally, the last value is the string that the gradient will be applied too.
* esc takes a string and returns the literal value thus escaping the markup
* repr takes a given string and returns the literal value surrounded by `'`
"""
from __future__ import annotations
from dataclasses import dataclass
from .exception import *

__all__ = [
    "PREDEFINED",
    "RGB",
    "XTERM",
    "RESETFOREGROUND",
    "RESETBACKGROUND",
    "RESETCOLORS",
    "UNDERLINE",
    "BOLD",
    "RESET",
    "MACROS",
    "HEX",
    "Context",
]

# @{δ}           <=> @F = foreground, @B = background
# [@F]           <=> reset foreground \x1b[39m
# [@B]           <=> reset background \x1b[49m
# []             <=> reset all color -> \x1b[39;49m
# [@δ color]     <=> predifened color name which equal ex. \x1b[31m or \x1b[41m
# [@δ 0;215;215] <=> (rgb) 3 numbers seperated by `;` or `,` defining r,g,b => \x1b[{38/48};2;r;g;b
# [@δ #ababab]   <=> (hex) `#` followed by 2, 3, or 6 numbers or letter defining a hex code hex -> rgb
# [@δ 3]         <=> (XTERM) 256 color index. \x1b[{38/48};5;n
PREDEFINED = {
    "black": lambda c: f"{c + 0}",
    "red": lambda c: f"{c + 1}",
    "green": lambda c: f"{c + 2}",
    "yellow": lambda c: f"{c + 3}",
    "blue": lambda c: f"{c + 4}",
    "magenta": lambda c: f"{c + 5}",
    "cyan": lambda c: f"{c + 6}",
    "white": lambda c: f"{c + 7}",
}
MACROS = {
    "rainbow": lambda string: __RAINBOW(string),
    "repr": lambda string: repr(string),
    "esc": lambda string: repr(string).removeprefix("'").removesuffix("'"),
    "gradient": lambda string: __GRADIENT(string),
}
RGB = lambda c, r, g, b: f"{c + 8};2;{r};{g};{b}"
XTERM = lambda c, v: f"{c + 8};5;{v}"
RESETFOREGROUND = "\x1b[39m"
RESETBACKGROUND = "\x1b[49m"
RESETCOLORS = "\x1b[39;49m"
UNDERLINE = lambda state: "\x1b[24m" if state else "\x1b[4m"
BOLD = lambda state: "\x1b[22m" if state else "\x1b[1m"
RESET = "\x1b[0m"


def HEX(context: int, hex: str) -> str:
    """Converts 3 or 6 digit hex into an rgb literal

    Args:
        context (int): Whether the hex is for the foreground or background
        hex (str): The hex code

    Raises:
        ValueError: If the hex code is not in the valid format

    Returns:
        str: Ansi RGB color
    """
    hex = hex.lstrip("#")
    l = len(hex)

    if l == 6:
        r, g, b = tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))
        return RGB(context, r, g, b)
    elif l == 3:
        hex = "".join(h + h for h in hex)
        r, g, b = tuple(int(hex[i : i + 2], 16) for i in (0, 2))
        return RGB(context, r, g, b)

    raise ValueError(f"Expected hex with length of 3 or 6")


def __RAINBOW(input: str) -> str:
    """Take a string input and make each character rainbow

    Args:
        input (str): The string to make into a rainbow

    Returns:
        str: Rainbow string
    """
    # red orange yellow green blue purple
    context = 30
    colors = [
        f"\x1b[{XTERM(context, 196)}m",
        f"\x1b[{XTERM(context, 202)}m",
        f"\x1b[{XTERM(context, 190)}m",
        f"\x1b[{XTERM(context, 41)}m",
        f"\x1b[{XTERM(context, 39)}m",
        f"\x1b[{XTERM(context, 92)}m",
    ]

    out = []
    for i, char in enumerate(input):
        out.append(colors[i % len(colors)] + char)
    out.append(RESETCOLORS)

    return "".join(out)


def __GRADIENT(value: str) -> str:
    """, or ; seprated gradient input. All but last value are the colors which are hex.
    Finally, the last input is the string to have the gradient applied too.

    Args:
        input (str): , or ; seperated gradient input

    Returns:
        str: Formatted string with the given gradient

    Note:
        Colors may only be hex codes
    """
    from re import match

    value = value.replace(";", ",").strip()
    content = value.split(",")

    colors = []
    string = ""

    # Parse the colors and the value to apply gradient too
    if len(content) >= 3:
        for i, val in enumerate(content):
            if val.strip().startswith("#"):
                colors.append(val.strip())
            else:
                if string == "":
                    string = val.strip()
                else:
                    raise MacroError(
                        value,
                        len(",".join(content[:i])) + 2,
                        "Already have a value to apply gradient too",
                    )
    else:
        raise MacroError(value, 1, "Gradient input must have 3 values")

    # Convert colors to ansi codes
    for i in range(len(colors)):
        if len(colors[i]) == 4 and match(r"#[a-fA-F0-9]{3}", colors[i]):
            colors[i] = f"\x1b[{HEX(30, colors[i])}m"
        elif len(colors[i]) == 7 and match(r"#[a-fA-F0-9]{6}", colors[i]):
            colors[i] = f"\x1b[{HEX(30, colors[i])}m"
        else:
            raise MacroError(
                colors[i],
                1,
                "Color hex must have 3 or 6 chars",
            )

    curr_color = 0
    split_at = len(string) // len(colors)
    times = len(string) // split_at
    output = [colors[curr_color]]
    print(split_at, times, len(colors))
    for i, char in enumerate(string):
        output.append(char)
        if i % split_at == 0 and i != 0 and curr_color < len(colors) - 1:
            curr_color += 1
            print(curr_color)
            output.append(colors[curr_color])

    output.append("\x1b[39;49m")
    return "".join(output)


@dataclass
class Context:
    """Context of foreground or background based on ansi codes"""

    FG: int = 30
    BG: int = 40
