"""Results

TestResults, ClassResults, and SuiteResults all hold and translate the test result information
into a structure that is easy to use and has mutliple outputs.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Union
from unittest import result

from ..Util import CR

__all__ = ["TestResult", "ResultType"]


@dataclass
class ResultType:
    """Enum/Dataclass that describes the test run result.

    Attributes:
        SUCCESS (tuple[str, str]): Message and color for a successful test run
        FAILED (tuple[str, str]): Message and color for a failed test run
        SKIPPED (tuple[str, str]): Message and color for a skipped test run
    """

    SUCCESS: tuple[str, str, int] = ("Passed", "\x1b[1;32m", "✓")
    FAILED: tuple[str, str, int] = ("Failed", "\x1b[1;31m", "x")
    SKIPPED: tuple[str, str, int] = ("Skipped", "\x1b[1;33m", "↻")


class Result:
    """Base class for result types"""

    def __init__(self):
        self._counts = [0, 0, 0]

    def getCounts(self) -> tuple[int, int, int]:
        """Get counts for passed, failed, skipped.

        Returns:
            tuple: The values for passed, failed, skipped respectively
        """
        return tuple(self._counts)

    @property
    def name(self) -> str:
        return self._name

    def write(self, indent: int = 0):
        """Output the result(s) to the screen

        Args:
            indent (int, optional): The amount to indent the values. Defaults to 0.
        """
        for line in self.pretty(indent):
            print(line)

    def pretty(self) -> list:
        """Format the result(s) into a formatted list

        Returns:
            list: List of formatted result(s)
        """
        return []

    def dict(self) -> dict:
        return {}

    def csv(self, location: str) -> str:
        """Takes the location that the file is to be saved then changes directory.

        Args:
            location (str, optional): The location where the file will be saved. Defaults to None.

        Raises:
            FileNotFoundError: If the specified directory does not exist

        Returns:
            str: The current directory before changing

        Note:
            This is to be used with an inherited class
        """

        if location != "":
            from os import path

            if location.startswith("~"):
                from pathlib import Path

                location = str(Path.home()) + location[1:]

            if not path.isdir(location):
                raise FileNotFoundError(f"Directory '{location}' does not exist")
            else:
                return True

        return True


class TestResult(Result):
    def __init__(self, result: tuple[str, ResultType, Union[str, list]] = None):
        super().__init__()

        if result is not None:
            self._name = result[0]
            self._result = result[1]
            self._info = result[2]
        else:
            self._name = "Unknown"
            self._result = ResultType.SKIPPED
            self._info = "Unkown test"

        self._counts = [0, 0, 0]
        if result == ResultType.SUCCESS:
            self._counts[0] = 1
        elif result == ResultType.FAILED:
            self._counts[1] = 1
        elif result == ResultType.SKIPPED:
            self._counts[2] = 1

    @property
    def result(self) -> str:
        return self._result[0]

    @property
    def color(self) -> str:
        return self._result[1]

    @property
    def icon(self) -> str:
        return self._result[2]

    @property
    def info(self) -> Union[str, list]:
        return self._info

    def pretty(self, indent: int = 0) -> list:
        """Used to convert result into a string. Allows for additional indentationto be added.

        Args:
            indent (int, optional): Amount of indent to add in spaces. Defaults to 0.

        Returns:
            str: The formatted result as a string with indent

        Note:
            If you don't plan to add additional indent use the implement __str__ method.
            str(TestResult) or print(TestResult).
        """
        out = []
        out.append(
            " " * indent + f"[{self.color}{self.icon}\x1b[0m] <case> {self.name}"
        )
        if isinstance(self.info, list):
            for trace in self.info:
                out.append(" " * (indent + 4) + trace)
        else:
            out.append(self.info)

        return out

    def dict(self) -> dict:
        """Convert the test result into a dictionary

        Returns:
            dict: Dictionary format of the test result
        """
        return {self.fname: {"result": self._result, "info": self.info}}

    def csv(self, location: str = "") -> bool:
        """Will create a CSV file with the result information.

        Args:
            location (str): The location to put the file, defaults to current directory

        Returns:
            bool: Whether it successfully created the CSV file
        """

        if super().csv(location):
            with open(location + self.name + ".csv", "+w") as csv_file:
                csv_file.write("Test Case,result,info\n")
                csv_file.write(self.toCSV())
        else:
            return False

        return True

    def toCSV(self) -> str:
        info = "\n".join(self.info) if isinstance(self.info, list) else self.info
        return f"{self.name},{self.result},'{info}'"

    def __str__(self):
        out = f"{self.fname} (Case) ... {self.color}{self.result}\x1b[0m"
        if isinstance(self.info, list):
            for trace in self.info:
                out += "\n" + trace
        else:
            out += self.info

        return out


class ClassResult:
    pass
