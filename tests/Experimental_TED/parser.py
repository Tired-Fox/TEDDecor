from __future__ import annotations
from typing import Iterator

from teddecor.TED.exception import MacroError
from tokens import Token, Color, Text, Bold, Underline, Formatter
from formatting import BOLD, UNDERLINE, RESET

__all__ = ["parse_macro"]

# TODO: Add optimization for formatting tokens


def split_macros(text: str) -> Iterator[str]:
    schars = ["@", "~", "!"]
    last, index = 0, 0
    while index < len(text):
        if index != 0:
            if text[index] in schars:
                yield text[last:index]
                last = index

        index += 1

    if last != index:
        yield text[last:]


def parse_macro(text: str) -> list[Token]:
    tokens = []
    for sub_macro in split_macros(text):
        sub_macro = sub_macro.strip()
        if sub_macro.startswith("@"):
            tokens.append(Color(sub_macro))
    return tokens


def optimize(tokens: list) -> list:
    format = Formatter()
    output = []
    for token in tokens:
        if isinstance(token, Color):
            format.color = token
        elif isinstance(token, Bold):
            format.bold = token
        elif isinstance(token, Underline):
            format.underline = token
        else:
            if not format.is_empty():
                output.append(format)
                format = Formatter()
            output.append(token)

    if not format.is_empty():
        output.append(format)

    return output


def parse(string: str):
    bold_state = BOLD.POP
    underline_state = UNDERLINE.POP
    text = []
    output = []
    escaped = False
    index = 0
    while index < len(string):
        char = string[index]
        if char == "*" and not escaped:
            if len(text) > 0:
                output.append(Text("".join(text)))
                text = []
            bold_state = BOLD.inverse(bold_state)
            output.append(Bold(bold_state))
        elif char == "_" and not escaped:
            if len(text) > 0:
                output.append(Text("".join(text)))
                text = []
            underline_state = UNDERLINE.inverse(underline_state)
            output.append(Underline(underline_state))
        elif char == "[" and not escaped:
            if len(text) > 0:
                output.append(Text("".join(text)))
                text = []

            start = index
            index += 1
            char = string[index]
            macro = []
            while char != "]":
                macro.append(char)
                index += 1
                if index == len(string):
                    raise MacroError(string, start, "Macro's must be closed")
                char = string[index]
            output.extend(parse_macro("".join(macro)))
        elif char == "\\" and not escaped:
            escaped = True
        else:
            text.append(char)
            escaped = False

        index += 1

    if len(text) > 0:
        output.append(Text("".join(text)))

    return "".join(str(token) for token in optimize(output)) + RESET
