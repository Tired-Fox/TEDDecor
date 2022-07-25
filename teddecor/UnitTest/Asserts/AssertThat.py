from typing import Any, Callable, Union

from .Asserts import *


__all__ = [
    "assert_that",
    "eq",
    "neq",
    "none",
    "not_none",
    "has",
    "raises",
    "haskey",
    "hasvalue",
    "haspair",
]


def assert_that(value: Any, compare: Callable, message: str = "") -> Union[bool, None]:
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
    return lambda x, message: assert_equal(x, value, message)


def neq(value: Any) -> Callable:
    """Return a function that takes a second value and asserts that it is not equal to the given value.

    Args:
        value (Any): The value to assert not equal to

    Returns:
        Callable: Function that takes a second value that asserts not equal to the given value

    Note:
        Used in `assert_that` and can be thought of, assert that value1 does not equals value2.
    """
    return lambda x, message: assert_not_equal(x, value, message)


def none() -> Callable:
    """Return a function that takes a value and asserts that it is None.

    Returns:
        Callable: Function that takes a value and asserts that it is `None`

    Note:
        Used in `assert_that` and can be thought of, assert that value is None.
    """
    return lambda x, message: assert_none(x, message)


def not_none() -> Callable:
    """Return a function that takes a value and asserts that it is not None.

    Returns:
        Callable: Function that takes a value and asserts that it is not `None`

    Note:
        Used in `assert_that` and can be thought of, assert that value is not None
    """
    return lambda x, message: assert_not_none(x, message)


def raises(exception: Exception = None) -> Callable:
    """Return a function that takes a callable and asserts that it raises an exception

    Args:
        exception (Exception): The exception that is expected. Leave as None to expect any exception

    Returns:
        Callable: Function that takes a callable
    """
    return lambda x, message: assert_raises(x, exception, message)


def within(obj: Any) -> Callable:
    """Return a function that takes a value is supposed to be within an object.

    Args:
        obj (Any): The object that implements __iter__

    Returns:
        Callable: Function that takes any value
    """
    return lambda x, message: assert_within(x, obj, message)


def has(value: Any) -> Callable:
    """Return a function that takes an iterable object and asserts if value is in it.

    Args:
        value (Any): The value that is in the iterable object

    Returns:
        Callable: Function that takes an object that implements __iter__
    """
    return lambda x, message: assert_within(value, x, message)
