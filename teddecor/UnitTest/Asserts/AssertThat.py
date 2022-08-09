from __future__ import annotations

from typing import Any, Callable, Union, Dict

from ...TED.markup import TED
from ...Exceptions import RangedException


__all__ = ["assertThat", "Matcher", "Raises", "eq", "gt", "lt"]


def stringify(value: Union[tuple[Any], list[Any], Dict[str, Any]]) -> str:
    output = []
    if type(value) in (tuple, list):
        for elem in value:
            output.append(str(elem))
    elif isinstance(value, dict):
        for key, elem in value.items():
            output.append(f"{key}={elem}")

    return ", ".join(output)


def check_args(
    args: Union[list[Any], tuple[Any]],
    kwargs: Dict[str, Any],
    arg_count: int = 1,
    arg_and_kwarg: bool = False,
    vkwargs: list[str] = [],
) -> bool:
    params = [stringify(args), stringify(kwargs)]
    if "" in params:
        params.remove("")
    params = ", ".join(params)
    if not arg_and_kwarg and len(args) > 0 and len(kwargs) > 0:
        RangedException(
            TED.encode(f"_is({params})"),
            "Too many values to compare",
            5,
            5 + len(params),
            "Can not have args and kwargs at the same time",
        ).throw()
    elif len(args) > arg_count:
        RangedException(
            TED.encode(f"_is({params})"),
            "Too many values to compare",
            5,
            5 + len(params),
            "Too many arguments",
        ).throw()
    else:
        for key, value in kwargs.items():
            if key not in vkwargs:
                RangedException(
                    TED.encode(f"{key}={value}"),
                    "Too many values to compare",
                    0,
                    len(f"{key}"),
                    "Invalid keyword argument",
                ).throw()

    return True


def Matcher(func: Callable):
    """Wraps a matcher for assertThat.

    Args:
        func (Callable): The matcher function that will return a callable to match against the actual value in assertThat.

    Note:
        Matchers must return functions that raise AssertionError when a condition is not met.
    """

    def inner(*args, **kwargs):
        return func(*args, **kwargs)

    return inner


def assertThat(actual: Any, matcher: Matcher) -> None:
    """Passes the actual value into the matcher.

    Args:
        actual (Any): The value to pass to the matcher
        matcher (Matcher): Matcher function that checks a condition

    Raises:
        AssertionError: If the matcher's condition fails
    """
    matcher(actual)


@Matcher
def eq(*args, **kwargs) -> Callable:
    """Assert that the actual value is equal to the expected value.

    Returns:
        Callable: A matcher that checks if the actual is equal to the expected.
    """

    def equal(actual: Any):
        """Assert that the actual value is the same type and equal to the expected value.

        Args:
            actual (Any): Any value that is matched against the argument value.

        Raises:
            AssertionError: If the actual value is the incorrect type.
            AssertionError: If the actual value does not equal the expected.
        """

        expected: Any = args[0]
        """Expected value that actual should match"""

        if not isinstance(actual, type(expected)):
            raise AssertionError(f"Expected {type(expected)} but found {type(actual)}")
        elif actual != expected:
            raise AssertionError("Actual value is not equal to the expected value.")

    if check_args(args=args, kwargs=kwargs):
        return equal


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


@Matcher
def gt(*args, **kwargs) -> Callable:
    """Assert that the actual value is greater than the expected value.

    Returns:
        Callable: A matcher that checks if the actual is greater than the expected.
    """

    def greater_than(actual: Any):
        """Assert that the actual value is the same type and greater than the expected value.

        Args:
            actual (Any): Any value that is matched against the argument value.

        Raises:
            AssertionError: If the actual value is the incorrect type.
            AssertionError: If the actual value is less than the expected.
        """

        expected: Any = args[0]
        """Expected value that actual should match"""

        if not isinstance(actual, type(expected)):
            raise AssertionError(f"Expected {type(expected)} but found {type(actual)}")
        elif actual < expected:
            raise AssertionError("Actual value is less than the expected value.")

    if check_args(args=args, kwargs=kwargs):
        return greater_than


@Matcher
def lt(*args, **kwargs) -> Callable:
    """Assert that the actual value is less than the expected value.

    Returns:
        Callable: A matcher that checks if the actual is less than the expected.
    """

    def less_than(actual: Any):
        """Assert that the actual value is the same type and less than the expected value.

        Args:
            actual (Any): Any value that is matched against the argument value.

        Raises:
            AssertionError: If the actual value is the incorrect type.
            AssertionError: If the actual value is greater than the expected.
        """

        expected: Any = args[0]
        """Expected value that actual should match"""

        if not isinstance(actual, type(expected)):
            raise AssertionError(f"Expected {type(expected)} but found {type(actual)}")
        elif actual > expected:
            raise AssertionError("Actual value is greater than the expected value.")

    if check_args(args=args, kwargs=kwargs):
        return less_than
