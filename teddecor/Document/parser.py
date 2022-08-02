from __future__ import annotations
import ast

from objects import *


def getFunctions(node) -> list:
    return [obj for obj in node.body if isinstance(obj, ast.FunctionDef)]


def getClasses(node) -> list:
    return [obj for obj in node.body if isinstance(obj, ast.ClassDef)]


with open("Results.py", "r") as fd:
    file_content = fd.read()

module = ast.parse(file_content)


from teddecor import TED

objects = [ast.get_docstring(module)]

for klass in getClasses(module):
    objects.append(Klass(klass))

for func in getFunctions(module):
    objects.append(Func(func))

print(objects)
