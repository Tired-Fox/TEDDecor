from typing import Any, Callable, Union

from .Asserts import *
from .Asserts import assertGreaterThan
from .Asserts import assertLessThan


__all__ = [
    "assertThat",
    "eq",
    "gt",
    "lt",
    "neq",
    "none",
    "notNone",
    "has",
    "raises",
    "within",
    "has",
    "Raises",
]


class Raises:
    """Assert that the code ran inside the `with` keyword raises an exception."""

    def __init__(self, exception: Exception = Exception):
        self._exception = exception

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            if not isinstance(exc_val, self._exception):
                raise AssertionError(
                    f"Unexpected exception raised {exc_val.__class__}"
                ) from exc_val
            else:
                return True
        else:
            raise AssertionError("No exception raised")


def assertThat(value: Any, compare: Callable, message: str = "") -> Union[bool, None]:
    """A general assert that takes logical value, callable pairs that make the testing more readable.

    Args:
        value (Any): The value to assert equal to
        compare (Callable): The function type to apply. Equal to, not equal to, is null, is not null
        message (str): The user defined error message to display

    Returns:
        Union[bool, None]: True if assert passed

    Raises:
        AssertionError: When assert function fails
    """
    return compare(value, message)


def eq(value: Any) -> Callable:
    """Return a function that takes a second value and asserts that it is equal to the given value.

    Args:
        value (Any): The value to assert equal to

    Returns:
        Callable: Function that takes a second value that asserts equal to the given value

    Note:
        Used in `assert_that` and can be thought of, assert that value1 equals value2.
    """
    return lambda x, message: assertEqual(x, value, message)


def neq(value: Any) -> Callable:
    """Return a function that takes a second value and asserts that it is not equal to the given value.

    Args:
        value (Any): The value to assert not equal to

    Returns:
        Callable: Function that takes a second value that asserts not equal to the given value

    Note:
        Used in `assert_that` and can be thought of, assert that value1 does not equals value2.
    """
    return lambda x, message: assertNotEqual(x, value, message)


def gt(value: Any) -> Callable:
    """Return a function that takes a second value and asserts that it is not equal to the given value.

    Args:
        value (Any): The value to assert not equal to

    Returns:
        Callable: Function that takes a second value that asserts not equal to the given value

    Note:
        Used in `assert_that` and can be thought of, assert that value1 does not equals value2.
    """
    return lambda x, message: assertGreaterThan(x, value, message)


def lt(value: Any) -> Callable:
    """Return a function that takes a second value and asserts that it is not equal to the given value.

    Args:
        value (Any): The value to assert not equal to

    Returns:
        Callable: Function that takes a second value that asserts not equal to the given value

    Note:
        Used in `assert_that` and can be thought of, assert that value1 does not equals value2.
    """
    return lambda x, message: assertLessThan(x, value, message)


def none() -> Callable:
    """Return a function that takes a value and asserts that it is None.

    Returns:
        Callable: Function that takes a value and asserts that it is `None`

    Note:
        Used in `assert_that` and can be thought of, assert that value is None.
    """
    return lambda x, message: assertNone(x, message)


def notNone() -> Callable:
    """Return a function that takes a value and asserts that it is not None.

    Returns:
        Callable: Function that takes a value and asserts that it is not `None`

    Note:
        Used in `assert_that` and can be thought of, assert that value is not None
    """
    return lambda x, message: assertNotNone(x, message)


def raises(exception: Exception = None) -> Callable:
    """Return a function that takes a callable and asserts that it raises an exception

    Args:
        exception (Exception): The exception that is expected. Leave as None to expect any exception

    Returns:
        Callable: Function that takes a callable
    """
    return lambda x, message: assertRaises(x, exception, message)


def within(obj: Any) -> Callable:
    """Return a function that takes a value is supposed to be within an object.

    Args:
        obj (Any): The object that implements __iter__

    Returns:
        Callable: Function that takes any value
    """
    return lambda x, message: assertWithin(x, obj, message)


def has(value: Any) -> Callable:
    """Return a function that takes an iterable object and asserts if value is in it.

    Args:
        value (Any): The value that is in the iterable object

    Returns:
        Callable: Function that takes an object that implements __iter__
    """
    return lambda x, message: assertWithin(value, x, message)
