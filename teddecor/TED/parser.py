from __future__ import annotations
from typing import Iterator

from .exception import MacroError
from .tokens import Token, Color, Text, Bold, Underline, Formatter, HLink
from .formatting import BOLD, UNDERLINE, RESET, LINK

__all__ = ["parse_macro"]


def split_macros(text: str) -> Iterator[str]:
    """Takes a macro, surrounded by brackets `[]` and splits the nested/chained macros.

    Args:
        text (str): The contents of the macro inside of brackets `[]`

    Yields:
        Iterator[str]: Iterates from each token to the next until entire macro is consumed
    """
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
    """Takes the chained, nested, or single macros and generates a token based on it's type.

    Args:
        text (str): The macro content inside of brackets `[]`

    Returns:
        list[Token]: The list of tokens created from the macro content inside of brackets `[]`
    """
    tokens = []
    for sub_macro in split_macros(text):
        sub_macro = sub_macro.strip()
        if sub_macro.startswith("@"):
            tokens.append(Color(sub_macro))
        elif sub_macro.startswith("~"):
            tokens.append(HLink(sub_macro))
    return tokens


def optimize(tokens: list) -> list:
    """Takes the generated tokens from the markup string and removes and combines tokens where possible.

    Example:
        Since there can be combinations such as fg, bg, bold, and underline they can be represented in two ways.
        * Unoptimized - `\\x1b[1m\\x1b[4m\\x1b[31m\\x1b[41m`
        * Optimized - `\\x1b[1;4;31;41m`


        Also, if many fg, bg, bold, and underline tokens are repeated they will be optimized.
        * `*Bold* *Still bold` translates to `\\x1b[1mBold still bold\\x1b[0m`
            * You can see that it removes unnecessary tokens as the affect is null.
        * `[@> red @> green]Green text` translates to `\\x1b[32mGreen text\\x1b[0m`
            * Here is an instance of overriding the colors. Order matters here, but since you are applying the foreground repeatedly only the last one will show up. So all previous declerations are removed.

    Args:
        tokens (list): The list of tokens generated from parsing the TED markup

    Returns:
        list: The optimized list of tokens. Bold, underline, fg, and bg tokens are combined into Formatter tokens
    """
    open_link = False
    formatter = Formatter()
    output = []
    for token in tokens:
        if isinstance(token, Color):
            formatter.color = token
        elif isinstance(token, Bold):
            formatter.bold = token
        elif isinstance(token, Underline):
            formatter.underline = token
        elif isinstance(token, HLink):
            if token.closing and open_link:
                open_link = False
                output.append(token)
            elif not token.closing and open_link:
                token.value = LINK.CLOSE + token.value
                output.append(token)
            else:
                open_link = True
                output.append(token)
        else:
            if not formatter.is_empty():
                output.append(formatter)
                formatter = Formatter()
            output.append(token)

    if not formatter.is_empty():
        output.append(formatter)
    if open_link:
        output.append(HLink("~"))

    return output


def parse(string: str):
    """Splits the TED markup string into tokens. If `*` or `_` are found then a Bold or Underline token will be generated respectively.
    If `[` is found then it marches to the end of the macro, `]`, and then parses it. All special characters can be escaped with `\\`

    Args:
        text (str): The TED markup string that will be parsed

    Raises:
        MacroError: If a macro is not closed

    Returns:
        str: The translated ansi representation of the given sting
    """

    bold_state = BOLD.POP
    """BOLD: The current state/value of being bold. Either is bold, or is not bold."""

    underline_state = UNDERLINE.POP
    """UNDERLINE: The current state/value of being underlined. Either is underlined, or is not underlined."""

    text: list = []
    """The chunks of text between special tokens."""

    output: list = []
    """Final output of the parse."""

    escaped: bool = False
    """Indicates whether to escape the next character or not."""

    index: int = 0
    """Current index of walking through the markup string."""

    def consume_macro(index: int):
        """Starts from start of the macro and grabs characters until at the end of the macro.

        Args:
            index (int): The current index in the string

        Raises:
            MacroError: If at the end of the markup string and the macro isn't closed

        Returns:
            int: Index after moving to the end of the macro
        """
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

        return index

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
            index = consume_macro(index)
        elif char == "\\" and not escaped:
            escaped = True
        else:
            text.append(char)
            escaped = False

        index += 1

    if len(text) > 0:
        output.append(Text("".join(text)))
        text = []

    return "".join(str(token) for token in optimize(output)) + RESET
