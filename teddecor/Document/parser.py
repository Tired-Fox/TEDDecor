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


TED.pprint(f"[@F green]{ast.get_docstring(module)}\n\n")

# print(ast.dump(module, indent=2))
for klass in getClasses(module):
    from os import system

    system("cls")
    TED.pprint(Klass(klass).pretty())
    input()

for func in getFunctions(module):
    from os import system

    system("cls")
    TED.pprint(Func(func).pretty())
    input()
