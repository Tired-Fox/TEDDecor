from __future__ import annotations
import ast
from typing import Any, Union

from sys import path

path.insert(0, "./")
from exceptions import *


class Constant:
    """A python object of the ast.Constant with better functionality."""

    def __init__(self, constant: ast.Constant):
        """Initialize the object with a ast.Constant

        Args:
            constant (ast.Constant): The ast.Constant to parse apart

        Raises:
            InvalidInputType: If the given value is not ast.Constant
        """
        if not isinstance(constant, ast.Constant):
            raise InvalidInputType(constant, ast.Constant)
        else:
            self._value = constant.value

    @property
    def value(self) -> Any:
        """The value of the constant

        Returns:
            Any: The value of the constant
        """
        return self._value

    def __str__(self) -> str:
        return str(self._value)


class Name:
    """A python object of the ast.Name with better functionality."""

    def __init__(self, name: ast.Name):
        """Initialize the object with a ast.Name

        Args:
            name (ast.Name): The ast.Name to parse apart

        Raises:
            InvalidInputType: If the given value is not ast.Name
        """
        if not isinstance(name, ast.Name):
            raise InvalidInputType(name, ast.Name)
        else:
            self._value = name.id

    @property
    def value(self) -> Any:
        """The value of the Name

        Returns:
            Any: The value of the constant
        """
        return self._value

    def __str__(self) -> str:
        return str(self._value)


class Expr:
    """A python object of the ast.Name with better functionality."""

    def __init__(self, expr: ast.Expr):
        """Initialize the object with a ast.Expr

        Args:
            name (ast.Expr): The ast.Expr to parse apart

        Raises:
            InvalidInputType: If the given value is not ast.Expr
        """
        if not isinstance(expr, ast.Expr):
            raise InvalidInputType(expr, ast.Expr)
        else:
            self._value = expr.value

    @property
    def value(self) -> Any:
        """The value of the Expr

        Returns:
            Any: The value of the constant
        """
        return self._value

    def __str__(self) -> str:
        return str(self._value)


class Arg:
    """A python object of the ast.Name with better functionality."""

    def __init__(self, argument: ast.arg):
        """Initialize the object with a ast.arg

        Args:
            name (ast.arg): The ast.arg to parse apart

        Raises:
            InvalidInputType: If the given value is not ast.arg
        """
        if not isinstance(argument, ast.arg):
            raise InvalidInputType(argument, ast.arg)
        else:
            self._arg = argument.arg
            self._annotation = getattr(argument, "annotation", None)

    @property
    def arg(self) -> str:
        """The arguments name"""
        return self._arg

    @property
    def annotation(self) -> Union[Constant, None]:
        """The arguments type annotation"""
        return self._annotation

    def __str__(self) -> str:
        return f"{self._arg}: {self._annotation}"


#  args=arguments(
#     args=[
#       arg(
#         arg='dog',
#         annotation=Name(id='str', ctx=Load())),
#       arg(
#         arg='cat',
#         annotation=Name(id='str', ctx=Load()))],
#     vararg=arg(arg='args'),
#     kwarg=arg(arg='kwargs'),
#     defaults=[
#       Constant(value='')]),
# Arguments:
#     - args list(Arg)
#     - vararg (Arg)
#     - kwarg (Arg)
#     - defaults list(Constant)
#     Properties:
#         + args list(Arg)
#         + vararg (Arg)
#         + kwarg (Arg)
#     Funcs:
#         + __str__


class Arguments:
    """A collection of arguments created from ast.arguments."""

    def __init__(self, arguments: ast.arguments):
        """Parse ast.arguments into a data object

        Args:
            arguments (ast.arguments): The ast.arguments to parse

        Raises:
            InvalidInputType: If the parameter isn't an ast.arguments
        """
        if not isinstance(arguments, ast.arguments):
            raise InvalidInputType(arguments, ast.arguments)
        else:
            self._args = [Arg(arg) for arg in arguments.args]
            self._defaults = [Constant(const) for const in arguments.defaults]
            self._vararg = (
                Arg(getattr(arguments, "vararg", None))
                if getattr(arguments, "vararg", None) is not None
                else None
            )
            self._kwarg = (
                Arg(getattr(arguments, "kwarg", None))
                if getattr(arguments, "kwarg", None) is not None
                else None
            )

    @property
    def args(self) -> list:
        """The regular args"""
        return self._args

    @property
    def defaults(self) -> list:
        """List of defaults that are given to the arguments"""
        return self._defaults

    @property
    def vararg(self) -> Union[Arg, None]:
        """The name of the *args variable"""
        return self._vararg

    @property
    def kwarg(self) -> Union[Arg, None]:
        """The name of the **kwargs variable"""
        return self._kwarg

    def __str__(self) -> str:
        return ", ".join(self.args)


if __name__ == "__main__":
    print(Expr(None))
