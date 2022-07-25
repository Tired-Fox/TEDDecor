from shutil import ReadError
from tkinter import E
from teddecor.UnitTest import *


class CustomObject:
    def __init__(self, index: int):
        self._index = index

    @property
    def index(self):
        return self._index


class Assert_Equal(Test):
    @test
    def assert_equal_pass(self):
        assert Asserts.assert_equal("dog", "dog")

    @test
    def assert_equal_fail(self):
        try:
            Asserts.assert_equal("dog", "cat")
        except AssertionError as error:
            assert "Values are not equal" in str(error)

        try:
            Asserts.assert_equal("dog", "cat", message="Dog is not equal to cat")
        except AssertionError as error:
            assert "Dog is not equal to cat" in str(error)

    @test
    def assert_not_equal_pass(self):
        assert Asserts.assert_not_equal("dog", "cat")

    @test
    def assert_not_equal_fail(self):
        try:
            Asserts.assert_not_equal("dog", "dog")
        except AssertionError as error:
            assert "Values are equal" in str(error)

        try:
            Asserts.assert_not_equal("dog", "dog", "Not Equal")
        except AssertionError as error:
            assert "Not Equal" in str(error)


class Assert_Raises(Test):
    def raises_lookup_error(self):
        raise LookupError

    @test
    def assert_raise_pass(self):
        assert Asserts.assert_raises(self.raises_lookup_error, LookupError)

    @test
    def assert_raise_pass_any(self):
        assert Asserts.assert_raises(self.raises_lookup_error)

    @test
    def assert_raise_unexpected_exception(self):
        try:
            Asserts.assert_raises(self.raises_lookup_error, BufferError)
        except AssertionError as error:
            assert "Unexpected exception LookupError" in str(error)

        try:
            Asserts.assert_raises(
                BufferError, self.raises_lookup_error, "Custom Message"
            )
        except AssertionError as error:
            assert "Custom Message" in str(error)

    @test
    def assert_raise_no_exception(self):
        try:
            Asserts.assert_raises(LookupError, lambda *_: None)
        except AssertionError as error:
            assert "No exception raised" in str(error)

        try:
            Asserts.assert_raises(LookupError, lambda *_: None, "Custom Message")
        except AssertionError as error:
            assert "Custom Message" in str(error)

    @test
    def assert_raise_fail_any(self):
        try:
            Asserts.assert_raises(self.raises_lookup_error)
        except AssertionError as error:
            assert "No exception raised" in str(error)


class Assert_Within(Test):
    def __init__(self):
        super().__init__()
        self.content = "Hello World!"

    @test
    def assert_within_pass(self):
        Asserts.assert_within("Hello", self.content)

    @test
    def assert_within_fail(self):
        try:
            Asserts.assert_within("universe", self.content)
        except AssertionError as error:
            assert "'universe' is not within the given object" in str(error)

        try:
            Asserts.assert_within("universe", self.content, "Custom Message")
        except AssertionError as error:
            assert "Custom Message" in str(error)


class Assert_None(Test):
    @test
    def assert_none_pass(self):
        assert Asserts.assert_none(None)

    @test
    def assert_none_fail(self):
        try:
            Asserts.assert_none("dog")
        except AssertionError as error:
            assert "<class 'str'> is not NoneType" in str(error)

        try:
            Asserts.assert_none("universe", "Custom Message")
        except AssertionError as error:
            Asserts.assert_within("Custom Message", str(error))

    @test
    def assert_not_none_pass(self):
        assert Asserts.assert_not_none("dog")

    @test
    def assert_not_none_fail(self):
        try:
            Asserts.assert_not_none(None)
        except AssertionError as error:
            assert "None is NoneType" in str(error)

        try:
            Asserts.assert_not_none("universe", "Custom Message")
        except AssertionError as error:
            Asserts.assert_within("Custom Message", str(error))


from typing import Callable


class Assert_That(Test):
    def raises_lookup(self):
        raise LookupError

    def raises_nothing(self):
        return True

    @test
    def assert_eq_pass(self):
        assert isinstance(eq(12), Callable)
        assert assert_that(12, eq(12))

    @test
    def assert_eq_fail(self):
        try:
            assert_that(12, eq(10))
        except AssertionError as error:
            print(error)
            Asserts.assert_within("Values are not equal", str(error))

        try:
            assert_that(12, eq(10), "Numbers are not equal")
        except AssertionError as error:
            Asserts.assert_within("Numbers are not equal", str(error))

    @test
    def assert_neq_pass(self):
        assert isinstance(neq(12), Callable)
        assert assert_that(12, neq(10))

    @test
    def assert_neq_fail(self):
        try:
            assert_that(12, eq(12), "Numbers are equal")
        except AssertionError as error:
            Asserts.assert_within("Numbers are equal", str(error))

    @test
    def assert_none_pass(self):
        assert isinstance(none(), Callable)
        assert assert_that(None, none())

    @test
    def assert_none_fail(self):
        try:
            assert_that(12, none(), "Custom Message")
        except AssertionError as error:
            Asserts.assert_within("Custom Message", str(error))

    @test
    def assert_not_none_pass(self):
        assert isinstance(not_none(), Callable)
        assert assert_that(12, not_none())

    @test
    def assert_not_none_fail(self):
        try:
            assert_that(12, not_none(), "Custom Message")
        except AssertionError as error:
            Asserts.assert_within("Custom Message", str(error))

    @test
    def assert_raises_plass(self):
        assert isinstance(raises(), Callable)
        assert assert_that(self.raises_lookup, raises(LookupError))
        assert assert_that(self.raises_lookup, raises())

    @test
    def assert_raises_fail(self):
        try:
            assert_that(self.raises_lookup, raises(AssertionError), "Custom Message")
        except AssertionError as error:
            Asserts.assert_within("Custom Message", str(error))

        try:
            assert_that(self.raises_nothing, raises(), "Custom Message")
        except AssertionError as error:
            Asserts.assert_within("Custom Message", str(error))

    @test
    def assert_within_pass(self):
        assert isinstance(within(None), Callable)
        assert assert_that("dog", within(["dog", "cat"]))
        assert assert_that("dog", within("Can you play with the dog?"))

    @test
    def assert_within_fail(self):
        try:
            assert_that("dog", within(None), "Custom Message")
        except AssertionError as error:
            Asserts.assert_within("Custom Message", str(error))

    @test
    def assert_within_pass(self):
        assert isinstance(has(None), Callable)
        assert assert_that(["dog", "cat"], has("dog"))
        assert assert_that("Can you play with the dog?", has("dog"))

    @test
    def assert_within_fail(self):
        try:
            assert_that([], has("dog"), "Custom Message")
        except AssertionError as error:
            Asserts.assert_within("Custom Message", str(error))


if __name__ == "__main__":
    classes = [
        Assert_Equal(),
        Assert_Raises(),
        Assert_Within(),
        Assert_None(),
        Assert_That(),
    ]
    for klass in classes:
        klass.main()
        print("\n······························\n")
