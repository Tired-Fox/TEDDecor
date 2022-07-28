from dataclasses import dataclass

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
    "black": lambda c: f"\x1b[{c + 0}m",
    "red": lambda c: f"\x1b[{c + 1}m",
    "green": lambda c: f"\x1b[{c + 2}m",
    "yellow": lambda c: f"\x1b[{c + 3}m",
    "blue": lambda c: f"\x1b[{c + 4}m",
    "magenta": lambda c: f"\x1b[{c + 5}m",
    "cyan": lambda c: f"\x1b[{c + 6}m",
    "white": lambda c: f"\x1b[{c + 7}m",
}
MACROS = {
    "rainbow": lambda string: RAINBOW(string),
    "repr": lambda string: REPR(string),
}
RGB = lambda c, r, g, b: f"\x1b[{c + 8};2;{r};{g};{b}m"
XTERM = lambda c, v: f"\x1b[{c + 8};5;{v}m"
RESETFOREGROUND = "\x1b[39m"
RESETBACKGROUND = "\x1b[49m"
RESETCOLORS = "\x1b[39;49m"
UNDERLINE = lambda state: "\x1b[24m" if state else "\x1b[4m"
BOLD = lambda state: "\x1b[22m" if state else "\x1b[1m"
RESET = "\x1b[0m"


def RAINBOW(input: str) -> str:
    """Take a string input and make each character rainbow

    Args:
        input (str): The string to make into a rainbow

    Returns:
        str: Rainbow string
    """
    # red orange yellow green blue purple
    context = 30
    colors = [
        XTERM(context, 196),
        XTERM(context, 202),
        XTERM(context, 190),
        XTERM(context, 41),
        XTERM(context, 39),
        XTERM(context, 92),
    ]

    out = []
    for i, char in enumerate(input):
        out.append(colors[i % len(colors)] + char)
    out.append(RESETCOLORS)

    return "".join(out)


def REPR(string: str) -> str:
    """Translates a string into it's literal format

    Args:
        string (str): String to get the literal from

    Returns:
        str: Literal representation of the inpu
    """
    return repr(string)


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
        r, g, b = tuple(int(hex[i : i + 2], 16) for i in (0, 2, 4))
        return RGB(context, r, g, b)

    raise ValueError(f"Expected hex with length of 3 or 6")


@dataclass
class Context:
    """Context of foreground or background based on ansi codes"""

    FG: int = 30
    BG: int = 40
