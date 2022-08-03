"""TED includes a parser to get literal strings from TED markup, along with a pprint
function that outputs the literal string from a TED markup.

Raises:
    MacroMissingError: If there is an incorrect macro or color specifier
    MacroError: If there is a general formatting error with a macro
"""
from __future__ import annotations

from parser import parse

__all__ = [
    "TED",
]


class TEDParser:
    def parse(self, text: str) -> str:
        return parse(text)

    def print(self, *args) -> None:
        parsed = []
        for arg in args:
            parsed.append(self.parse(arg))

        print(*parsed)

    @staticmethod
    def encode(text: str) -> str:
        schars = ["*", "_", "["]
        for char in schars:
            text = f"\{char}".join(text.split(char))
        return text


TED = TEDParser()

if __name__ == "__main__":
    TED.print("[@> red @< blue @> green]*Something** bold*")
