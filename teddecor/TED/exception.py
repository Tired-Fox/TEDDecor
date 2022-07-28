__all__ = [
    "MacroError",
    "MacroMissingError",
]


class MacroError(Exception):
    """Takes a value, index, and a hint and points out where in the markup the error is

    Args:
        Exception (MacroError): Displays a general macro error
    """

    def __init__(self, value: str, index: int, hint: str):
        self.error = (
            "\n\x1b[1mInvalid Macro:\n"
            + f"  {value}\n "
            + " " * index
            + f"\x1b[31m↑ {hint}\x1b[0m"
        )
        super().__init__(self.error)

    def __str__(self):
        return self.error


class MacroMissingError(Exception):
    """Takes a value, start pos of macro, current error index, hint, and what is missing.
    It then takes this information and displays what is missing and hints to why

    Args:
        Exception (_type_): _description_
    """

    def __init__(self, value: str, start: int, end: int, hint: str, inject: str):
        self.error = (
            "\n\x1b[0m\x1b[1mInvalid Macro:\n"
            + f"  {value[:end]}\x1b[31m{inject}\x1b[39m{value[end:]}\n  "
            + " " * (end - start)
            + f"\x1b[34m↑\x1b[39m {hint}\x1b[0m"
        )
        super().__init__(self.error)

    def __str__(self):
        return self.error
