"""TED includes a parser to get literal strings from TED markup, along with a pprint
function that outputs the literal string from a TED markup.

Raises:
    MacroMissingError: If there is an incorrect macro or color specifier
    MacroError: If there is a general formatting error with a macro
"""
from __future__ import annotations

from .parser import parse

__all__ = [
    "TED",
]


class TEDParser:
    """Main class exposed by the library to give access the markup utility functions."""

    def parse(self, text: str) -> str:
        """Parses a TED markup string and returns the translated ansi equivilent.

        Args:
            text (str): The TED markup string

        Returns:
            str: The ansi translated string
        """
        return parse(text)

    def print(self, *args) -> None:
        """Works similare to the buildin print function.
        Takes all arguments and passes them through the parser.
        When finished it will print the results to the screen with a space inbetween the args.

        Args:
            *args (Any): Any argument that is a string or has a __str__ implementation
        """
        parsed = []
        for arg in args:
            parsed.append(self.parse(str(arg)))

        print(*parsed)

    @staticmethod
    def encode(text: str) -> str:
        """Utility to automatically escape/encode special markup characters.

        Args:
            text (str): The string to encode/escape

        Returns:
            str: The escaped/encoded version of the given string
        """
        schars = ["*", "_", "["]
        for char in schars:
            text = f"\{char}".join(text.split(char))
        return text


TED = TEDParser()
