__all__ = ["MacroError"]

from os import get_terminal_size


def get_len(string: str) -> int:
    from re import sub

    string = sub(r"\x1b\[(\d{0,2};?)*m", "", string)
    return len(string)


class MacroError(Exception):
    """Takes a value, index, and a hint and points out where in the markup the error is

    Args:
        Exception (MacroError): Displays a general macro error
    """

    def __init__(self, value: str, index: int, hint: str):
        width = get_terminal_size().columns
        index = index % width - 1 if index > width else index
        arrow = "\x1b[31m↑\x1b[39m"
        if ((index + len(hint + arrow) + 1) > width) and (
            get_len(hint + arrow) + 1 < index
        ):
            self.error = (
                "\n\x1b[1mInvalid Macro:\n"
                + f"  {value}\n "
                + " " * (index - get_len(hint) + get_len(arrow))
                + f"{hint} {arrow}\x1b[0m"
            )
        else:
            self.error = (
                "\n\x1b[1mInvalid Macro:\n"
                + f"  {value}\n "
                + " " * (index + 1)
                + f"{arrow} {hint}\x1b[0m"
            )
        super().__init__(self.error)

    def __str__(self):
        return self.error
