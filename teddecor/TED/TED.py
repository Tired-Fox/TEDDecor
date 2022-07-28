"""TED includes a parser to get literal strings from TED markup, along with a pprint
function that outputs the literal string from a TED markup.

Raises:
    MacroSpecifierError: If there is an incorrect macro or color specifier
    MacroError: If there is a general formatting error with a macro
"""
from __future__ import annotations

from .exception import *
from .colors import *

__all__ = [
    "parse",
    "pprint",
]


def __getMacroType(index: int, char: str, string: str) -> str:
    if char != " ":
        if char == "@":
            return "@"
        elif char == "~":
            return "~"
        elif char == "^":
            return "^"
        elif char != ["@", "~", "^"]:
            raise MacroError(
                string,
                index + 1,
                "Must be macro type, @ or ~",
            )


def __getMacroContent(index: int, string: str, start: int) -> tuple[int, str]:
    token = ""
    closed = 1
    _escaped = False
    while closed:
        if string[index] == "]" and not _escaped:
            closed -= 1
            if closed:
                token += string[index]
        elif string[index] == "\x1b":
            token += string[index]
            _escaped = True
        elif string[index] == "\\" and not _escaped:
            _escaped = True
        elif string[index] == "[" and not _escaped:
            closed += 1
            token += string[index]
        else:
            token += string[index]
            _escaped = False

        if closed:
            index += 1
            if index == len(string):
                raise MacroMissingError(
                    string, start, index, "Macro must end with \x1b[32m", "]"
                )

    if closed == 0:
        return index, token
    else:
        raise MacroMissingError(
            string, start, index, "Macro must end with \x1b[32m]", "]"
        )


def __parseColor(token: str, string: str, start: int) -> str:
    from re import match

    if token.strip() == "":
        return RESETCOLORS
    if token.startswith(("F", "B")):
        type = token[0]
        token = token[1:].strip(" ")
        if type == "F":
            type = Context.FG
            if len(token) == 0:
                return RESETFOREGROUND
        elif type == "B":
            type = Context.BG
            if len(token) == 0:
                return RESETBACKGROUND

        if token.startswith("#"):
            if len(token) == 4 and match(r"#[a-fA-F0-9]{3}", token):
                return HEX(type, token)
            elif len(token) == 7 and match(r"#[a-fA-F0-9]{6}", token):
                return HEX(type, token)
        elif match(r"\d{1,3}[,;]\d{1,3}[,;]\d{1,3}", token):
            rgb = token.replace(";", ",").split(",")
            return RGB(type, rgb[0], rgb[1], rgb[2])
        elif match(r"\d{1,3}", token):
            return XTERM(type, token)
        else:
            if token.lower() in PREDEFINED.keys():
                return PREDEFINED[token](type)
            else:
                raise MacroError(
                    string,
                    start + 4,
                    "Color must be hex, rgb (r;g;b), xterm, or in the list of predefined",
                )
    else:
        raise MacroError(
            string,
            start + 2,
            "Must have color type if color is specified, F or B",
        )
    return ""


def __parseLink(token: str, string: str, start: int, index: int) -> str:
    token = token.split("|", 1)
    if len(token) == 2:
        if token[1] == "":
            raise MacroMissingError(
                string,
                start,
                index,
                "\x1b[32m string\x1b[39m is required if \x1b[32m| \x1b[39mis provided",
                " string",
            )
        else:
            return f"\x1b]8;;{token[0]}\x1b\\{parse(token[1])}\x1b]8;;\x1b\\"
    else:
        return f"\x1b]8;;{token[0]}\x1b\\{parse(token[0])}\x1b]8;;\x1b\\"


def __parseFunc(token: str, string: str, start: int, index: int) -> str:
    token = token.split("|", 1)
    token[0] = token[0].lower()
    if token[0] in MACROS.keys():
        if len(token) == 2:
            return MACROS[token[0]](token[1])
        else:
            try:
                return MACROS[token[0]]()
            except Exception:
                raise MacroMissingError(
                    string, start, index, "Macro must have \x1b[32m| string", "| string"
                )
    else:
        raise MacroError(
            string,
            start + 3,
            "Not a valid macro",
        )

    return ""


def __parseMacro(index: int, string: str) -> str:
    start = index
    index += 1
    result = ""

    if string[index] == "]":
        return index, RESET
    else:
        type = __getMacroType(index, string[index], string)
        index += 1

        index, token = __getMacroContent(index, string, start)

        if type == "@":
            result = __parseColor(token, string, start)
        elif type == "~":
            result = __parseLink(token, string, start, index)
        elif type == "^":
            result = __parseFunc(token, string, start, index)

        return index, result


def parse(string: str) -> str:
    """TED parser that translates the given TED markup string

    Args:
        string (str): TED markup string

    Returns:
        str: Translated version of the string
    """
    _underlined = False
    _bold = False
    _escaped = False

    out = []

    i = 0
    while i < len(string):
        if string[i] in ["_", "*", "["] and _escaped == False:
            if string[i] == "_":
                out.append(UNDERLINE(_underlined))
                _underlined = not _underlined
            elif string[i] == "*":
                out.append(BOLD(_bold))
                _bold = not _bold
            elif string[i] == "[" and not _escaped:
                index, value = __parseMacro(i, string)
                i = index
                if value != "":
                    out.append(value)
        elif string[i] == "\x1b":
            out.append(string[i])
            _escaped = True
        elif string[i] == "\\" and not _escaped:
            _escaped = True
        else:
            out.append(string[i])
            _escaped = False
        i += 1

    out.append(RESET)
    return "".join(out)


def pprint(string: str) -> None:
    """Takes the given string, sends it through the TED parser then prints the result

    Args:
        string (str): The TED markup string to pretty print
    """
    print(parse(string))
