from ast import Assert
from typing import Any, Callable, Union, Dict

from teddecor.Exceptions.base import RangedException
from teddecor import TED
from teddecor.UnitTest.Results import SaveType
from teddecor.UnitTest.Testing import run, test


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


@Matcher
def _is(*args, **kwargs) -> Callable:
    """Assert that the actual value is the value provided to this function.

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

        if type(actual) != type(expected):
            raise AssertionError(f"Expected {type(expected)} but found {type(actual)}")
        elif actual != expected:
            raise AssertionError(
                f"Values are not the same. Expected {expected} but found {actual}"
            )

    if check_args(args=args, kwargs=kwargs):
        return equal


def assertThat(actual: Any, matcher: Matcher) -> None:
    """Passes the actual value into the matcher.

    Args:
        actual (Any): The value to pass to the matcher
        matcher (Matcher): Matcher function that checks a condition

    Raises:
        AssertionError: If the matcher's condition fails
    """
    matcher(actual)


@test
def fail():
    assert False


if __name__ == "__main__":
    # assertThat(None, _is(12))
    run(fail).save(ext=SaveType.TXT)
    # print(TED.strip("\[[@F red]Error Message[@F]] \x1b[1m*Some error \\_message"))
