"""TEDDecor
Inline markown parsing and printing

This is a easy to use library that gives a user access to colored text, bold text,
underlined text, hyperlinks and much more.
"""

__version__ = "1.2.0"
from .TED import TED
from .logger import LL, Log, Logger
from .pprint import p_value, pprint
from . import decorators
