from __future__ import annotations

import ast
import os

with open("test_colors.py", "r") as fd:
    file_content = fd.read()

module = ast.parse(file_content)


def getFunctions(node) -> list:
    return [obj for obj in node.body if isinstance(obj, ast.FunctionDef)]


def getClasses(node) -> list:
    return [obj for obj in node.body if isinstance(obj, ast.ClassDef)]


# print(ast.dump(module, indent=4))
if isinstance(module.body[0], ast.Expr):
    print(module.body[0].value.value)

docstring = {"doc": ""}
classes = {"classes": []}
functions = {"functions": []}

docs = {"module": {"classes": [], "functions": []}}

for func in getFunctions(module):
    print(ast.dump(func, indent=2))

# print(ast.dump(getClasses(module)[0], indent=2))
# for klass in :
#     print()
