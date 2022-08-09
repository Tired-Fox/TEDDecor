from __future__ import annotations

from typing import Any, Callable, Union, Dict

from ...TED.markup import TED
from ...Exceptions import RangedException


__all__ = ["assertThat", "Matcher", "Raises", "eq", "gt", "lt", "empty"]


def stringify(value: Union[tuple[Any], list[Any], Dict[str, Any]]) -> str:
    output = []
    if type(value) in (tuple, list):
        for elem in value:
            output.append(str(elem))
    elif isinstance(value, dict):
        for key, elem in value.items():
            output.append(f"{key}={elem}")

    return ", ".join(output)


def get_expected(args, kwargs) -> Any:
    """Gets the expected value from either the first argument or the corresponding
    `expect` or `expected` keyword arguments.

    Args:
        args (list[Any]): The list of arguments.
        kwargs (Dict[str, Any]): Dictionary of keyword arguments.

    Returns:
        Any: The expected value.
    """
    if "expect" in kwargs or "expected" in kwargs:
        return kwargs["expected"] if "expected" in kwargs else kwargs["expect"]
    else:
        return args[0]


def check_args(
    args: Union[list[Any], tuple[Any]],
    kwargs: Dict[str, Any],
    name: str,
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
            TED.encode(f"{name}({params})"),
            "Too many values to compare",
            len(name) + 1,
            len(name) + 1 + len(params),
            "Can not have args and kwargs at the same time",
        ).throw()
    elif len(args) > arg_count:
        RangedException(
            TED.encode(f"{name}({params})"),
            "Too many values to compare",
            len(name) + 1,
            len(name) + 1 + len(params),
            "Too many arguments",
        ).throw()
    elif len(kwargs) > arg_count:
        RangedException(
            TED.encode(f"{name}({params})"),
            "Too many values to compare",
            len(name) + 1,
            len(name) + 1 + len(params),
            "Too many arguments",
        ).throw()
    elif len(kwargs.keys()) > 0:
        argkwargs = [stringify(args)]
        for key, value in kwargs.items():
            argkwargs.append(f"{key}={value}")
            if key not in vkwargs:
                if "" in argkwargs:
                    argkwargs.remove("")
                start = (
                    len(name) + 1 + len(", ".join(argkwargs)) - len(f"{key}={value}")
                )
                RangedException(
                    TED.encode(f"{name}({', '.join(argkwargs)})"),
                    "Too many values to compare",
                    start,
                    start + len(key),
                    "Invalid keyword argument",
                ).throw()

    return True


def Matcher(arg_count: int = 1, arg_and_kwarg: bool = False, vkwargs: list[str] = []):
    """Wraps a matcher function and validates the arguments before returning the matcher function.

    Args:
        arg_count (int, optional): The number of arguments the matcher can take. Defaults to 1.
        arg_and_kwarg (bool, optional): Whether both args and kwargs can be passed at the same time. Defaults to False.
        vkwargs (list[str], optional): The valid kwargs that can be passed. Defaults to [].

    Returns:
        Callable: The matcher function that will be called by assertThat.
    """

    valid_kwargs = ["expected", "expect"].extend(vkwargs)

    def match_wrapper(func: Callable):
        """Wrapper that takes the decorated function.

        Args:
            func (Callable): The function that will generate the matcher function.

        Returns:
            Callable: The matcher function that will be called by assertThat.
        """

        def match_inner(*args, **kwargs):
            """Wrapper that takes the arguments passed to the matcher on initialization and validates them.

            Returns:
                Callable: The matcher function that will be called by assertThat.
            """
            check_args(
                args, kwargs, func.__name__, arg_count, arg_and_kwarg, valid_kwargs
            )
            return func(*args, **kwargs)

        return match_inner

    return match_wrapper


def assertThat(actual: Any, matcher: Matcher, cmessage: str = None) -> None:
    """Passes the actual value into the matcher.

    Args:
        actual (Any): The value to pass to the matcher
        matcher (Matcher): Matcher function that checks a condition

    Raises:
        AssertionError: If the matcher's condition fails
    """

    result, message = matcher(actual)

    if cmessage is not None:
        message = cmessage

    if not result:
        raise AssertionError(message)


@Matcher()
def eq(*args, **kwargs) -> Callable:
    """Assert that the actual value is equal to the expected value.

    Returns:
        Callable: A matcher that checks if the actual is equal to the expected.
    """

    def equal(actual: Any) -> tuple[bool, str]:
        """Assert that the actual value is the same type and equal to the expected value.

        Args:
            actual (Any): Any value that is matched against the argument value.

        Raises:
            AssertionError: If the actual value is the incorrect type.
            AssertionError: If the actual value does not equal the expected.

        Return:
            tuple[bool, str]: The success and the associated message
        """

        expected: Any = get_expected(args, kwargs)
        """Expected value that actual should match"""

        if not isinstance(actual, type(expected)):
            return False, f"Expected {type(expected)} but found {type(actual)}"
        elif actual != expected:
            return False, "Actual value is not equal to the expected value."

        return True, None

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


@Matcher()
def gt(*args, **kwargs) -> Callable:
    """Assert that the actual value is greater than the expected value.

    Returns:
        Callable: A matcher that checks if the actual is greater than the expected.
    """

    def greater_than(actual: Any) -> tuple[bool, str]:
        """Assert that the actual value is the same type and greater than the expected value.

        Args:
            actual (Any): Any value that is matched against the argument value.

        Raises:
            AssertionError: If the actual value is the incorrect type.
            AssertionError: If the actual value is less than the expected.

        Return:
            tuple[bool, str]: The success and the associated message
        """

        expected: Any = get_expected(args, kwargs)
        """Expected value that actual should match"""

        if not isinstance(actual, type(expected)):
            return False, f"Expected {type(expected)} but found {type(actual)}"
        elif actual < expected:
            return False, "Actual value is less than the expected value."

        return True, None

    return greater_than


@Matcher()
def lt(*args, **kwargs) -> Callable:
    """Assert that the actual value is less than the expected value.

    Returns:
        Callable: A matcher that checks if the actual is less than the expected.
    """

    def less_than(actual: Any) -> tuple[bool, str]:
        """Assert that the actual value is the same type and less than the expected value.

        Args:
            actual (Any): Any value that is matched against the argument value.

        Raises:
            AssertionError: If the actual value is the incorrect type.
            AssertionError: If the actual value is greater than the expected.

        Return:
            tuple[bool, str]: The success and the associated message
        """

        expected: Any = get_expected(args, kwargs)
        """Expected value that actual should match"""

        if not isinstance(actual, type(expected)):
            return False, f"Expected {type(expected)} but found {type(actual)}"
        elif actual > expected:
            return False, "Actual value is greater than the expected value."

        return True, None

    return less_than


@Matcher(arg_count=0)
def empty() -> Callable:
    """Assert that the actual value is less than the expected value.

    Returns:
        Callable: A matcher that checks if the actual is less than the expected.
    """

    def is_empty(actual: Any) -> tuple[bool, str]:
        """Assert that the actual value is the same type and less than the expected value.

        Args:
            actual (Any): Any value that is matched against the argument value.

        Raises:
            AssertionError: If the actual value is the incorrect type.
            AssertionError: If the actual value is greater than the expected.

        Return:
            tuple[bool, str]: The success and the associated message
        """

        if actual is not None:
            if hasattr(actual, "__len__"):
                if len(actual) < 1:
                    return False, "Value is not empty"
            else:
                return False, "Value must implement __len__ to check if it is empty"

        return True, None

    return is_empty
