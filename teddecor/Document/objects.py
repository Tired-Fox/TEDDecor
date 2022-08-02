from __future__ import annotations
import ast
from typing import Any, Union

from sys import path

path.insert(0, "./")
from exceptions import *

__all__ = ["Constant", "Expr", "Name", "Arg", "Arguments", "Func", "Klass"]


class AstObj:
    def ParseAstObject(self, node) -> Union[Constant, Name, Tuple, Subscript, None]:
        if node is not None:
            if isinstance(node, ast.Constant):
                return Constant(node)
            elif isinstance(node, ast.Name):
                return Name(node)
            elif isinstance(node, ast.Tuple):
                return Tuple(node)
            elif isinstance(node, ast.Subscript):
                return Subscript(node)
            elif isinstance(node, ast.Attribute):
                return Attribute(node)

        return None


class Attribute(AstObj):
    def __init__(self, attribute: ast.Attribute):
        if not isinstance(attribute, ast.Attribute):
            raise InvalidInputType(attribute, ast.Attribute)
        else:
            self._value = self.ParseAstObject(attribute.value)
            self._attr = attribute.attr

    @property
    def value(self) -> Any:
        return self._value

    @property
    def attr(self) -> str:
        return self._attr

    def pretty(self, markup: str = "[@F white]") -> str:
        """Return the pretty string format of the object"""
        return f"{markup} {self}[@]"

    def __str__(self) -> str:
        return f"{self.value}.{self.attr}"


class Tuple(AstObj):
    def __init__(self, tuple: ast.Tuple) -> None:
        if not isinstance(tuple, ast.Tuple):
            raise InvalidInputType(tuple, ast.Tuple)
        else:
            self.__parse_elts(tuple.elts)

    @property
    def elts(self) -> list:
        """Tuple's elements"""
        return self._elts

    def __parse_elts(self, elts: list) -> list:
        """Parse the tuple's elts into it's corresponding objects

        Args:
            elts (list): The list of elts to parse

        Returns:
            list: The parsed elts
        """
        self._elts = []
        for elt in elts:
            self._elts.append(self.ParseAstObject(elt))

    def pretty(self, markup: str = "[@F white]") -> str:
        """Return the pretty string format of the object"""
        return f"{markup} {self}[@]"

    def __str__(self) -> str:
        return ", ".join(str(elt) for elt in self._elts)


class Subscript(AstObj):
    def __init__(self, subscript: ast.Subscript) -> None:
        if not isinstance(subscript, ast.Subscript):
            raise InvalidInputType(subscript, ast.Subscript)
        else:
            self._value = Name(subscript.value)
            self._slice = self.ParseAstObject(subscript.slice)

    @property
    def value(self) -> Name:
        """Subscript's value"""
        return self._value

    @property
    def slice(self) -> Union[Tuple, Name]:
        """Subscript's slice"""
        return self._slice

    def pretty(self, markup: str = "[@F white]") -> str:
        """Return the pretty string format of the object"""
        return f"{markup} {self}[@]"

    def __str__(self) -> str:
        return f"{self.value}\[{self.slice}]"


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
            self._value = Constant(expr.value)

    @property
    def value(self) -> Any:
        """The value of the Expr

        Returns:
            Any: The value of the constant
        """
        return self._value

    def __str__(self) -> str:
        return str(self._value)


class Arg(AstObj):
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
            self._annotation = self.ParseAstObject(
                getattr(argument, "annotation", None)
            )

    @property
    def arg(self) -> str:
        """The arguments name"""
        return self._arg

    @property
    def annotation(self) -> Union[Constant, None]:
        """The arguments type annotation"""
        return self._annotation

    def pretty(self) -> str:
        return f"[@F cyan]{self._arg}[@F]: [@F yellow]{self._annotation}[@F]"

    def __str__(self) -> str:
        return f"{self._arg}: {self._annotation}"


class Arguments(AstObj):
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
            self._defaults = [self.ParseAstObject(node) for node in arguments.defaults]
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

    def pretty(self) -> str:
        return ", ".join(arg.pretty() for arg in self.args)

    def __str__(self) -> str:
        return ", ".join(str(arg) for arg in self.args)


class Func(AstObj):
    """A parsed ast.FunctionDef object with relavent information."""

    def __init__(self, function: ast.FunctionDef):
        """Take an ast.FunctionDef object and parse it into a data object

        Args:
            function (ast.FunctionDef): The FunctionDef to parse

        Raises:
            InvalidInputType: If not an ast.FunctionDef
        """
        if not isinstance(function, ast.FunctionDef):
            raise InvalidInputType(function, ast.FunctionDef)
        else:
            self._name = function.name
            self._arguments = Arguments(function.args)
            self._docs = ast.get_docstring(function)
            self.__FilterBody(function.body)
            self._decorators = [Name(decor) for decor in function.decorator_list]
            self._returns = self.ParseAstObject(getattr(function, "returns", None))

    def __FilterBody(self, body: list) -> list:
        # functions
        self._body = []
        for node in body:
            if isinstance(node, ast.FunctionDef):
                self._body.append(Func(node))

    @property
    def name(self):
        """Name of the function"""
        return self._name

    @property
    def arguments(self):
        """Functions arguments"""
        return self._arguments

    @property
    def docs(self):
        """Functions docstring"""
        return self._docs

    @property
    def body(self):
        """Functions body"""
        return self._body

    @property
    def decorators(self):
        """Functions decorators"""
        return self._decorators

    @property
    def returns(self):
        """Functions return type"""
        return self._returns

    def pretty(self, indent: int = 0) -> list:
        spacing = " " * indent
        out = [
            spacing
            + f"*[@F #EBBC4E]def [@F magenta][^esc|{self.name}][@F]({self.arguments.pretty()}[@F])"
        ]
        if self.returns is not None:
            out[0] += f" → [@F yellow]{self.returns}"

        if self.docs is not None:
            for line in str(self.docs).split("\n"):
                out.append(f"{spacing}[@F green][^esc|" + line + "]")

        if len(self.body) > 0:
            out.extend(f.pretty(indent=4) for f in self.body)

        return out

    def str(self, indent: int = 0) -> str:
        spacing = " " * indent
        out = f"{spacing}def {self.name}({self.arguments})"
        if self.returns is not None:
            out += f" → {self.returns}"

        if self.docs is not None:
            doc = f"{spacing}" + f"\n{spacing}".join(str(self.docs).split("\n"))
            out += f"\n{doc}\n"

        if len(self.body) > 0:
            out += "\n".join(f.str(indent=4) for f in self.body)
        return out

    def __str__(self) -> str:
        return self.str()


# Klass:
#     - name (str)
#     - bases list(Name)
#     - body list(ast.Node)
#     - decorators list(Name)


class Klass:
    def __init__(self, klass: ast.ClassDef):
        if not isinstance(klass, ast.ClassDef):
            raise InvalidInputType(klass, ast.ClassDef)
        else:
            self._name = klass.name
            self._bases = [Name(base) for base in klass.bases]
            self.__FilterBody(klass.body)
            self._decorators = [Name(decor) for decor in klass.decorator_list]
            self._docs = ast.get_docstring(klass)

    @property
    def name(self):
        """Name of the function"""
        return self._name

    @property
    def bases(self):
        """Class bases"""
        return self._bases

    @property
    def docs(self):
        """Klass docstring"""
        return self._docs

    @property
    def body(self):
        """Klass body"""
        return self._body

    @property
    def decorators(self):
        """Klass decorators"""
        return self._decorators

    def __FilterBody(self, body: list) -> list:
        # functions
        self._body = []
        for node in body:
            if isinstance(node, ast.FunctionDef):
                self._body.append(Func(node))

    def pretty(self, indent: int = 0) -> list:
        spacing = " " * indent
        out = [
            spacing
            + f"[@F #EBBC4E]*class [@F magenta][^esc|{self.name}][@F]({'[@F], [@F yellow]'.join(str(base) for base in self.bases)}[@F])"
        ]

        if self.docs is not None:
            for line in str(self.docs).split("\n"):
                out.append(f"{spacing}[@F green][^esc|" + line + "]")

        if len(self.body) > 0:
            for f in self.body:
                out.extend(f.pretty(indent=4))
        return out

    def str(self, indent: int = 0) -> str:
        spacing = " " * indent
        out = (
            spacing
            + f"class {self.name}({', '.join(str(base) for base in self.bases)})"
        )

        if self.docs is not None:
            doc = (
                f"{spacing}[^repr|"
                + f"\n{spacing}".join(str(self.docs).split("\n"))
                + "]"
            )
            out += f"\n{doc}\n"

        if len(self.body) > 0:
            out += "\n".join(f.str(indent=4) for f in self.body)
        return out

    def __str__(self) -> str:
        return self.str()
