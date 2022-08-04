"""Test Suite

A collection of tests that are to be run.
Can be either test classes or individual test cases.
"""
from __future__ import annotations
from inspect import isclass
from typing import Callable, Pattern, Union

from .Results import SuiteResult
from .Testing import Test, test, run

__all__ = ["TestSuite"]

# TODO: Change manual formatting to TED formatter
# PERF: Add Graph SVG output
class TestSuite:
    """Run the given test classes or filter with regex."""

    def __init__(
        self,
        name: str,
        tests: list[Union[Test, test]] = [],
    ):
        """Start with a list of Test classes or test functions. The function name patter can also be specified.
            Lastly you can specify whether a Test class outputs the result

        Args:
            tests (list[Union[Test, test]], optional): _description_. Defaults to None.
            regex (Pattern, optional): _description_. Defaults to None.
            output (bool, optional): _description_. Defaults to True.
        """
        self._name = name
        self._tests = tests

    @property
    def name(self) -> str:
        return self._name

    @property
    def tests(self) -> Union[list, None]:
        return self._tests

    @tests.setter
    def tests(self, tests: list[Test]):
        self._tests = tests

    @property
    def regex(self) -> Union[str, None]:
        return self._regex

    @regex.setter
    def regex(self, regex: str):
        self._regex = regex

    def append(self, obj: Union[Test, Callable]):
        if self._tests is None:
            self._tests = []

        self._tests.append(obj)

    def run(
        self,
        display: bool = True,
        regex: Pattern = None,
    ) -> SuiteResult:
        """Run all the provided test classes and cases.q

        Args:
            display (bool, optional): Whether to display anything. Defaults to True
            regex (Pattern, optional): Pattern of which tests should be run

        Returns:
            SuiteResult: Results object that can save and print the results
        """
        from re import match

        _results = SuiteResult(self.name)

        for test in self.tests:
            if isclass(test):
                _results.append(test().run(regex=regex, display=False))
            else:
                result = run(test, display=False)
                if regex is not None and match(regex, result.name):
                    _results.append(result)
                elif regex is None:
                    _results.append(result)

        if display:
            _results.write()

        return _results
