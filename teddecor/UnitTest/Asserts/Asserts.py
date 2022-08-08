"""Assert that something is true or false

This module provides more descriptive and usefull asserts for things like equal, not null, contains, etc.
"""

from __future__ import annotations
from shutil import ExecError
from typing import Any, Callable, Union

__all__ = [
    "assertEqual",
    "assertNotEqual",
    "assertRaises",
    "assertWithin",
    "assertNone",
    "assertNotNone",
]

# PERF: Replace errors with lested/grouped errors if python 3.11
def assertEqual(left: Any, right: Any, message: str = "") -> Union[bool, None]:
    """Assert that the left operand (First parameter) is equal to the right operand (Second Parameter).

    Args:
        left (Any): Left Operand
        right (Any): Right Operand
        message (str, optional): User defind error messaage when left != right.
                                    Defaults to "Left operand not equal to right operand".

    Raises:
        AssertionError: When left operand type doesn't equal right operands type
        AssertionError: When left operand doesn't equal right operand
    """

    if left != right:
        if message == "":
            message = "Values are not equal"
        raise AssertionError(message)

    return True


def assertGreaterThan(left: Any, right: Any, message: str = "") -> Union[bool, None]:
    """Assert that the left operand (First parameter) is greater than the right operand (Second Parameter).

    Args:
        left (Any): Left Operand
        right (Any): Right Operand
        message (str, optional): User defind error messaage when left != right.
                                    Defaults to "Left operand not equal to right operand".

    Raises:
        AssertionError: When left operand is less than the right operand
    """

    if left < right:
        if message == "":
            message = "Value is less than not greater than"
        raise AssertionError(message)

    return True


def assertLessThan(left: Any, right: Any, message: str = "") -> Union[bool, None]:
    """Assert that the left operand (First parameter) is less than the right operand (Second Parameter).

    Args:
        left (Any): Left Operand
        right (Any): Right Operand
        message (str, optional): User defind error messaage when left != right.
                                    Defaults to "Left operand not equal to right operand".

    Raises:
        AssertionError: When left operand is greater than the right operands
    """

    if left > right:
        if message == "":
            message = "Value is greater than not less than"
        raise AssertionError(message)

    return True


def assertNotEqual(left: Any, right: Any, message: str = "") -> Union[bool, None]:
    """Assert that the left operand (First parameter) is not equal to the right operand (Second Parameter).

    Args:
        left (Any): Left Operand
        right (Any): Right Operand
        message (str, optional): User defind error messaage when left != right.
                                    Defaults to "Left operand not equal to right operand".

    Raises:
        AssertionError: When left operand type doesn't equal right operands type
        AssertionError: When left operand doesn't equal right operand
    """

    if left == right:
        if message == "":
            message = "Values are equal"
        raise AssertionError(message)

    return True


def assertRaises(
    function: Callable, exception: Exception = None, message: str = ""
) -> Union[bool, None]:
    """Assert that a exceptions is raised within a callable piece of code

    Args:
        exception (Exception, optional): Exception that is expected. Default None
        function (Callable): Callable piece of code
        message (str, optional): Error message. Defaults to None.

    Raises:
        AssertionError: Unexpected Exception
        AssertionError: No Exceptions

    Note:
        If exception is not passed it will assume that it should expect any exception.
    """

    if exception is not None:
        try:
            _ = function()
        except exception:
            return True
        except Exception as error:
            if message == "":
                message = f"Unexpected exception {type(error).__name__}"
            raise AssertionError(message) from error
    else:
        try:
            _ = function()
        except Exception:
            return True

    if message == "":
        message = "No exception raised"

    raise AssertionError(message)


def assertWithin(search: Any, obj: Any, message: str = "") -> Union[bool, None]:
    """Assert that a search value is contained within a certain string.

    Args:
        search (str, Any): Search value
        obj (str, list): Object to identify if search is within
        message (str, optional): Error message. Defaults to None.

    Raises:
        AssertionError: When the search is not contained within the object

    Note:
        This assert runs `value not in object` so it only works if object
        implements __iter__.
    """

    if message == "":
        message = f"'{search}' is not within the given object"

    try:
        if search not in obj:
            raise AssertionError(message)
    except Exception as error:
        raise AssertionError(message) from error

    return True


def assertNone(value: Any, message: str = "") -> Union[bool, None]:
    """Assert that a value is None.

    Args:
        value (Any): Value that should be None
        message (str, optional): Error message. Defaults to None.

    Raises:
        AssertionError: When the value is not None
    """

    if message == "":
        message = f"{type(value)} is not NoneType"

    if value is not None:
        raise AssertionError(message)

    return True


def assertNotNone(value: Any, message: str = "") -> Union[bool, None]:
    """Assert that a value is not None.

    Args:
        value (Any): Value that shouldn't be None
        message (str, optional): Error message. Defaults to None.

    Raises:
        AssertionError: When the value is None
    """

    if message == "":
        message = f"{value} is NoneType"

    if value is None:
        raise AssertionError(message)

    return True
