"""TED includes a parser to get literal strings from TED markup, along with a pprint
function that outputs the literal string from a TED markup.

Raises:
    MacroMissingError: If there is an incorrect macro or color specifier
    MacroError: If there is a general formatting error with a macro
"""
from __future__ import annotations
from typing import Callable

from exception import *
from colors import *

__all__ = [
    "TED",
]


class TEDParser:
    def __init__(self):
        self.cache = {"*": BOLD.POP, "_": UNDERLINE.POP, "~": False}
        self._escaped = False
        self._capture = False
        self._captured = [None, []]
        self.attributes = []
        self.output = []

    def __parse_macro(self):
        self._index += 1
        start = self._index
        macro_content = []
        _macro_count = 1

        while self._index < len(self._markup) and _macro_count > 0:
            if self._markup[self._index] == "]" and not self._escaped:
                _macro_count -= 1
                if _macro_count == 0:
                    break
                else:
                    macro_content.append(self._markup[self._index])
            elif self._markup[self._index] == "\\" and not self._escaped:
                self._escaped = True
            elif self._markup[self._index] == "[" and not self._escaped:
                macro_content.append(self._markup[self._index])
                _macro_count += 1
            else:
                macro_content.append(self._markup[self._index])

            self._index += 1

        if _macro_count > 0:
            raise MacroError(
                self._markup,
                start - 1,
                "Macro must be closed with a non escaped \x1b[32m]",
            )
        else:
            macro_content = self.__parse_macro_content("".join(macro_content))

        self.output.append(macro_content)

    def __parse_color(self, color: str) -> str:
        # #ababab, 123;12,123, 2, red
        color = color[1:].strip()

        def get_color(content: str, context: int) -> str:
            from re import match

            if content.strip() == "":
                return RESETCOLORS

            if content.startswith("#"):
                if len(content) == 4 and match(r"#[a-fA-F0-9]{3}", content):
                    if context == Context.BOTH:
                        return BUILDFORMAT(
                            [HEX(Context.FG, content), HEX(Context.BG, content)]
                        )
                    else:
                        return BUILDFORMAT([HEX(context, content)])
                elif len(content) == 7 and match(r"#[a-fA-F0-9]{6}", content):
                    if context == Context.BOTH:
                        return BUILDFORMAT(
                            [HEX(Context.FG, content), HEX(Context.BG, content)]
                        )
                    else:
                        return BUILDFORMAT([HEX(context, content)])
            elif match(r"\d{1,3}[,;]\d{1,3}[,;]\d{1,3}", content):
                if context == Context.BOTH:
                    rgb = content.replace(";", ",").split(",")
                    return BUILDFORMAT(
                        [
                            RGB(Context.FG, rgb[0], rgb[1], rgb[2]),
                            RGB(Context.BG, rgb[0], rgb[1], rgb[2]),
                        ]
                    )
                else:
                    rgb = content.replace(";", ",").split(",")
                    return BUILDFORMAT([RGB(context, rgb[0], rgb[1], rgb[2])])
            elif match(r"\d{1,3}", content):
                if context == Context.BOTH:
                    return BUILDFORMAT(
                        [XTERM(Context.FG, content), XTERM(Context.BG, content)]
                    )
                else:
                    return BUILDFORMAT([XTERM(context, content)])
            else:
                if content.lower() in PREDEFINED.keys():
                    content = content.lower()
                    if context == Context.BOTH:
                        return BUILDFORMAT(
                            [
                                PREDEFINED[content](Context.FG),
                                PREDEFINED[content](Context.BG),
                            ]
                        )
                    else:
                        return BUILDFORMAT([PREDEFINED[content](context)])
                else:
                    raise MacroError(
                        self._markup,
                        self._index,
                        "Value must be in predefined or a different color type",
                    )

        if color.startswith(">"):
            return get_color(color[1:].strip(), Context.FG)
        elif color.startswith("<"):
            return get_color(color[1:].strip(), Context.BG)
        else:
            return get_color(color.strip(), Context.BOTH)

    def __parse_link(self, link: str) -> str:
        link = link[1:].strip()

        if len(link) == 0:
            if self.cache["~"]:
                self.cache["~"] = False
                return LINK.CLOSE
            else:
                return ""
        elif len(link) > 0:
            self.cache["~"] = True
            if self.cache["~"]:
                return LINK.CLOSE + LINK.OPEN(link)
            else:
                return LINK.OPEN(link)

    def __parse_macro_content(self, content: str) -> None:
        identifiers = ["@", "~", "^"]

        macros = []
        results = []

        caller: Callable = None
        scont = content.strip()

        _sub_index = 0

        if scont.startswith(tuple(identifiers)):
            while _sub_index < len(scont):
                char = scont[_sub_index]

                if char in identifiers and len(macros) > 0:
                    if len(macros[-1]) == 2:
                        macros[-1].append(_sub_index)
                        results.append(caller(content[macros[-1][1] : _sub_index]))
                if char == "@":
                    macros.append(["color", _sub_index])
                    caller = self.__parse_color
                elif char == "~":
                    macros.append(["link", _sub_index])
                    caller = self.__parse_link

                _sub_index += 1

            if len(macros) > 0 and len(macros[-1]) == 2:
                macros[-1].extend([_sub_index, content[macros[-1][1] : _sub_index]])
                results.append(caller(content[macros[-1][1] : _sub_index]))

        elif len(content) == 0:
            return RESET
        else:
            raise MacroError(
                self._markup,
                self._index - len(content),
                "Macro must begin with an identifier; \x1b[32m@\x1b[39m, \x1b[32m^\x1b[39m, \x1b[32m~",
            )

        return "".join(results)

    def __indentify_char(self):
        if self._markup[self._index] == "*" and not self._escaped:
            attr = BOLD.inverse(self.cache["*"])

            if BOLD.inverse(self.cache["*"]) in self.attributes:
                self.attributes.remove(BOLD.inverse(self.cache["*"]))
            else:
                self.attributes.append(attr)

            self.cache["*"] = attr
        elif self._markup[self._index] == "_" and not self._escaped:
            attr = UNDERLINE.inverse(self.cache["*"])

            if UNDERLINE.inverse(self.cache["*"]) in self.attributes:
                self.attributes.remove(UNDERLINE.inverse(self.cache["*"]))
            else:
                self.attributes.append(attr)

            self.cache["*"] = attr
        elif self._markup[self._index] == "[" and not self._escaped:
            self.__parse_macro()
        elif self._markup[self._index] == "\\" and not self._escaped:
            self._escaped = True
        else:
            if len(self.attributes) > 0:
                self.output.append(BUILDFORMAT(self.attributes))
                self.attributes = []
            else:
                self.output.append(self._markup[self._index])
            self._escaped = False

    def parse(self, string: str) -> str:
        """TED parser that translates the given TED markup string

        Args:
            string (str): TED markup string

        Returns:
            str: Translated version of the string
        """
        if True:
            import inspect

            frame = inspect.stack()[1]
            self._module = inspect.getmodule(frame[0])

        self._index = 0
        self._markup = string

        while self._index < len(self._markup):
            self.__indentify_char()
            self._index += 1

        end = "\x1b[0m"
        if self.cache["~"] is not None:
            end += LINK.CLOSE

        elif len(self._captured[1]) > 0:
            self.output.append("".join(self._captured[1]))

        return "".join(self.output) + end

    def pprint(self, *args) -> None:
        """Takes the given string and gives it to the TED parser, then prints the result.

        Args:
            markup (Union[str, list[str]]): TED markup string or list of strings
        """

        parsed = []
        for arg in args:
            if isinstance(arg, str):
                parsed.append(self.parse(arg))
                
TED = TEDParser()