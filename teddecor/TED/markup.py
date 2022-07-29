"""TED includes a parser to get literal strings from TED markup, along with a pprint
function that outputs the literal string from a TED markup.

Raises:
    MacroMissingError: If there is an incorrect macro or color specifier
    MacroError: If there is a general formatting error with a macro
"""
from __future__ import annotations
from turtle import back

from .exception import *
from .colors import *

__all__ = [
    "parse",
    "pprint",
]


def __tokenizeMacro(index: int, start: int, string: str, content: str) -> str:
    content = content.strip()
    if content.startswith(("@", "~", "^")):
        if content.startswith("~"):
            return __parseLink(content[1:], string, start, index)
        elif content.startswith("^"):
            return __parseFunc(content[1:], string, start, index)
        else:
            return __parseColor(content, string, start)
    else:
        raise MacroMissingError(
            string,
            start,
            start + 1,
            "Macro must start with an identifier such as @, ~, or ^",
            "?",
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
                    string, start, index, "Macro must end with a \x1b[32m]", "]"
                )

    if closed == 0:
        return index, token
    else:
        raise MacroMissingError(
            string, start, index, "Macro must end with a \x1b[32m]", "]"
        )


def __parseColor(content: str, string: str, start: int) -> str:
    from re import match

    foreground = ""
    background = ""

    # start + 1 = beginning
    tokens = content.split("@")
    tokens.remove("")

    for token in tokens:
        if token.strip() == "":
            return RESETCOLORS
        if token.startswith(("F", "B")):
            type = token[0]
            content = token[1:].strip(" ")
            if type == "F":
                type = Context.FG
                if len(content) == 0:
                    return RESETFOREGROUND
            elif type == "B":
                type = Context.BG
                if len(content) == 0:
                    return RESETBACKGROUND

            if content.startswith("#"):
                if len(content) == 4 and match(r"#[a-fA-F0-9]{3}", content):
                    if type == Context.FG:
                        foreground = HEX(type, content)
                    else:
                        background = HEX(type, content)
                elif len(content) == 7 and match(r"#[a-fA-F0-9]{6}", content):
                    if type == Context.FG:
                        foreground = HEX(type, content)
                    else:
                        background = HEX(type, content)
            elif match(r"\d{1,3}[,;]\d{1,3}[,;]\d{1,3}", content):
                if type == Context.FG:
                    rgb = content.replace(";", ",").split(",")
                    foreground = RGB(type, rgb[0], rgb[1], rgb[2])
                else:
                    rgb = content.replace(";", ",").split(",")
                    background = RGB(type, rgb[0], rgb[1], rgb[2])
            elif match(r"\d{1,3}", content):
                if type == Context.FG:
                    foreground = XTERM(type, content)
                else:
                    background = XTERM(type, content)
            else:
                if content.lower() in PREDEFINED.keys():
                    content = content.lower()
                    if type == Context.FG:
                        foreground = PREDEFINED[content](type)
                    else:
                        background = PREDEFINED[content](type)
                else:
                    raise MacroError(
                        string,
                        start + 4,
                        parse(
                            "Value must be in predefined or a different color type, see [~https://tired-fox.github.io/TEDDecor/teddecor/TED/colors.html|Colors docs]"
                        ),
                    )
        else:
            raise MacroError(
                string,
                start + 2,
                "Must have color type if color is specified, F or B",
            )

    result = "\x1b["
    if foreground != "" and background != "":
        result += f"{foreground};{background}m"
    elif foreground != "":
        result += f"{foreground}m"
    elif background != "":
        result += f"{background}m"

    return result


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

    if string[index] == "]":
        return index, RESET
    else:
        index, content = __getMacroContent(index, string, start)
        result = __tokenizeMacro(index, start, string, content)

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
    """Takes the given string and gives it to the TED parser, then prints the result.

    Args:
        string (str): The TED markup string to pretty print
    """
    print(parse(string))
