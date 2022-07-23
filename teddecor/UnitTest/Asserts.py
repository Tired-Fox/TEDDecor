"""Assert that something is true or false

This module provides more descriptive and usefull asserts for things like equal, not null, contains, etc.
"""

from typing import Any, Callable
from inspect import getframeinfo, stack

__all__ = [
    "assert_equal",
    "assert_raises",
    "assert_contains"
]

# PERF: Replace errors with lested/grouped errors if python 3.11
def assert_equal(left: Any, right: Any, message: str = "Left operand not equal to right operand"):
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
    caller = getframeinfo(stack()[1][0])
    if left != right:
        raise AssertionError(message)

    return True


def assert_raises(exception, function: Callable, message: str = ""):
    """Assert that a exceptions is raised within a callable piece of code

    Args:
        exception (Exception): Exception that is expected
        function (Callable): Callable piece of code
        message (str, optional): Error message. Defaults to None.

    Raises:
        AssertionError: Unexpected Exception
        AssertionError: No Exceptions
    """

    try:
        function()
    except exception:
        return True
    except Exception as error:
        if message == "":
           message = f"Unexpected exception {type(error).__name__}" 
        raise AssertionError(message)

    if message == "":
        message = "No exception raised"
    raise AssertionError(message)


def assert_contains(search: str, content: str, message: str = ""):
    """Assert that a search value is contained within a certain string.

    Args:
        search (str): Search value
        content (str): Content
        message (str, optional): Error message. Defaults to None.

    Raises:
        AssertionError: When the search is not contained within the content
    """

    if message == "":
        message = f"[{content}] does not contain [{search}]"

    if search not in content:
        raise AssertionError(message)

    return True
