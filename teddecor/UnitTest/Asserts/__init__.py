"""Asserts

A logical, easy to read way of writing test assertions.

Currently includes assert_that, which takes a method of eq({value}),
neq({value}), null(), not_null(). This makes the test easily readable.

- ex. assert_that(12,       eq(12)). This reads as; assert that 12 is equal to 12.
- ex. assert_that(12,   not_null()). This reads as; assert that 12 is not null.
- ex. assert_that(None,     null()). This reads as; assert that 12 is null.
- ex. assert_that(12,      neq(10)). This reads as; assert that 12 is not equal to 10.
"""

from .AssertThat import *
from . import Asserts