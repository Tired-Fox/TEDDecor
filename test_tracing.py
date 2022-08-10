import traceback
from inspect import stack


def one():
    print("one")


def two():
    print("two")


def three():
    print("three")


if __name__ == "__main__":
    print([frame.function for frame in stack()])
    one()
    print(stack())
    two()
    print(stack())
    three()
    print(stack())
