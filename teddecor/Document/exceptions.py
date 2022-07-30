from sys import path

path.insert(0, "../")
from TED import *

__all__ = ["InvalidInputType", "InvalidInputValue"]


class InvalidInputType(Exception):
    """Thrown when the input has an invalid type.

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, value, expected):
        self.error = parse(
            "\n*Invalid Input Type:\n"
            + f"  Got [@F red]{type(value)}[@F] but expected [@F green]{expected}"
        )
        super().__init__(self.error)

    def __str__(self):
        return self.error


class InvalidInputValue(Exception):
    """Thrown when the input has an invalid value.

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, value, hint):
        self.error = (
            parse("\n*Invalid Input Value:\n" + f"  {value}\n")
            + f"  ↑ [@F yellow]{hint}"
        )
        super().__init__(self.error)

    def __str__(self):
        return self.error


# class InvalidInput(Exception):
#     def __init__(self):
#         self.error
#         super().__init__(self.error)
#
#     def __str__(self):
#         return self.error
