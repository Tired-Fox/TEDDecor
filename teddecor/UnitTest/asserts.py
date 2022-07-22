from typing import Any, Callable
from inspect import getframeinfo, stack

# TODO: Make all asserts yield when raising exceptions

def format_message(message: str, caller) -> str:
    """Takes an error message and formates it with color.

    Args:
        message (str): Message to format

    Returns:
        str: Formatted message
    """

    out = f"\x1b[1m[\x1b[33m{caller.function}\x1b[37m:\x1b[34m{caller.lineno}\x1b[37m]\x1b[0m \x1b[31m"
    out += message + "\x1b[0m"
    return out

# PERF: Replace errors with lested/grouped errors if python 10
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
        raise AssertionError(format_message(message, caller))

def assert_raises(exception: Exception, function: Callable, message: str = None):
    """Assert that a exceptions is raised within a callable piece of code

    Args:
        exception (Exception): Exception that is expected
        function (Callable): Callable piece of code
        message (str, optional): Error message. Defaults to None.

    Raises:
        AssertionError: Unexpected Exception
        AssertionError: No Exceptions
    """

    caller = getframeinfo(stack()[1][0])
        
    try:
        value = function()
        
    except exception as expected:
        return
    except Exception as error:
        raise AssertionError(format_message(
                                f"Unexpected exception {type(error).__name__}" if message is None else message, 
                                caller
                            )
        )
    raise AssertionError(format_message("No exception raised" if message is None else message, caller))

def assert_contains(search: str, content: str, message: str = None):
    """Assert that a search value is contained within a certain string.

    Args:
        search (str): Search value
        content (str): Content
        message (str, optional): Error message. Defaults to None.

    Raises:
        AssertionError: When the search is not contained within the content
    """

    caller = getframeinfo(stack()[1][0])

    if message is None:
        message = f"[{content}] does not contain [{search}]"

    if search not in content:
        raise AssertionError(format_message(message, caller))
