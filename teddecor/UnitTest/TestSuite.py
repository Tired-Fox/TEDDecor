"""Test Suite

A collection of tests that are to be run.
Can be either test classes or individual test cases.
"""
from __future__ import annotations
from inspect import isclass
from typing import Pattern, Union

from .Results import SuiteResult
from .Testing import Test, test, runTest

__all__ = ["TestSuite"]

# TODO: Change manual formatting to TED formatter
# PERF: Add Graph SVG output
class TestSuite:
    """Run the given test classes or filter with regex."""

    def __init__(
        self,
        name: str,
        tests: list[Union[Test, test]] = None,
        regex: Pattern = None,
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
        self._regex = regex

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

    def run(
        self,
        display: bool = True,
    ) -> TestSuite:
        """Run all the provided test classes and cases.q

        Args:
            display (bool, optional): Whether to display anything. Defaults to True.
            class_results (bool, optional): Whether to show individul class results. Defaults to True.
            case_results (bool, optional): Whether to show individual case results. Defaults to True.

        Returns:
            dict: Dictionary of results
        """
        from re import match

        _results = SuiteResult(self.name)

        for test in self.tests:
            if isclass(test):
                _results.append(test().run(regex=self.regex, display=False))
            else:
                result = runTest(test, display=False)
                if self.regex is not None and match(self.regex, result.name):
                    _results.append(result)
                elif self.regex is None:
                    _results.append(result)

        if display:
            _results.write()

        return _results
