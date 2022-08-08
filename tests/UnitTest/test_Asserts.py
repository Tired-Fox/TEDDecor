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
        assert Asserts.assertEqual("dog", "dog")

    @test
    def assert_equal_fail(self):
        try:
            Asserts.assertEqual("dog", "cat")
        except AssertionError as error:
            assert "Values are not equal" in str(error)

        try:
            Asserts.assertEqual("dog", "cat", message="Dog is not equal to cat")
        except AssertionError as error:
            assert "Dog is not equal to cat" in str(error)

    @test
    def assert_not_equal_pass(self):
        assert Asserts.assertNotEqual("dog", "cat")

    @test
    def assert_not_equal_fail(self):
        try:
            Asserts.assertNotEqual("dog", "dog")
        except AssertionError as error:
            assert "Values are equal" in str(error)

        try:
            Asserts.assertNotEqual("dog", "dog", "Not Equal")
        except AssertionError as error:
            assert "Not Equal" in str(error)


class Assert_Raises(Test):
    def raises_lookup_error(self):
        raise LookupError

    def raise_exception(self, exception: Exception):
        raise exception

    @test
    def assert_raise_pass(self):
        assert Asserts.assertRaises(self.raises_lookup_error, LookupError)

    @test
    def assert_raise_pass_any(self):
        assert Asserts.assertRaises(self.raises_lookup_error)

    @test
    def assert_raise_unexpected_exception(self):
        try:
            Asserts.assertRaises(self.raises_lookup_error, BufferError)
        except AssertionError as error:
            assert "Unexpected exception LookupError" in str(error)

        try:
            Asserts.assertRaises(
                BufferError, self.raises_lookup_error, "Custom Message"
            )
        except AssertionError as error:
            assert "Custom Message" in str(error)

    @test
    def assert_raise_no_exception(self):
        try:
            Asserts.assertRaises(LookupError, lambda *_: None)
        except AssertionError as error:
            assert "No exception raised" in str(error)

        try:
            Asserts.assertRaises(LookupError, lambda *_: None, "Custom Message")
        except AssertionError as error:
            assert "Custom Message" in str(error)

    @test
    def assert_raise_fail_any(self):
        try:
            Asserts.assertRaises(self.raises_lookup_error)
        except AssertionError as error:
            assert "No exception raised" in str(error)

    @test
    def with_raises(self):
        with Raises():
            self.raise_exception(TypeError)

        with Raises():
            raise AssertionError

        with Raises(TypeError):
            raise TypeError
        try:
            with Raises(TypeError):
                raise AssertionError
        except AssertionError as error:
            assert "Unexpected exception raised" in str(error)

        try:
            with Raises():
                pass
        except AssertionError as error:
            assert "No exception raised" in str(error)


class Assert_Within(Test):
    def __init__(self):
        super().__init__()
        self.content = "Hello World!"

    @test
    def assert_within_pass(self):
        Asserts.assertWithin("Hello", self.content)

    @test
    def assert_within_fail(self):
        try:
            Asserts.assertWithin("universe", self.content)
        except AssertionError as error:
            assert "'universe' is not within the given object" in str(error)

        try:
            Asserts.assertWithin("universe", self.content, "Custom Message")
        except AssertionError as error:
            assert "Custom Message" in str(error)


class Assert_None(Test):
    @test
    def assert_none_pass(self):
        assert Asserts.assertNone(None)

    @test
    def assert_none_fail(self):
        try:
            Asserts.assertNone("dog")
        except AssertionError as error:
            assert "<class 'str'> is not NoneType" in str(error)

        try:
            Asserts.assertNone("universe", "Custom Message")
        except AssertionError as error:
            Asserts.assertWithin("Custom Message", str(error))

    @test
    def assert_not_none_pass(self):
        assert Asserts.assertNotNone("dog")

    @test
    def assert_not_none_fail(self):
        try:
            Asserts.assertNotNone(None)
        except AssertionError as error:
            assert "None is NoneType" in str(error)

        try:
            Asserts.assertNotNone("universe", "Custom Message")
        except AssertionError as error:
            Asserts.assertWithin("Custom Message", str(error))


from typing import Callable


class Assert_That(Test):
    def raises_lookup(self):
        raise LookupError

    def raises_nothing(self):
        return True

    @test
    def eq_pass(self):
        assert isinstance(eq(12), Callable)
        assert assertThat(12, eq(12))

    @test
    def eq_fail(self):
        try:
            assertThat(12, eq(10))
        except AssertionError as error:
            Asserts.assertWithin("Values are not equal", str(error))

        try:
            assertThat(12, eq(10), "Numbers are not equal")
        except AssertionError as error:
            Asserts.assertWithin("Numbers are not equal", str(error))

    @test
    def neq_pass(self):
        assert isinstance(neq(12), Callable)
        assert assertThat(12, neq(10))

    @test
    def neq_fail(self):
        try:
            assertThat(12, eq(12), "Numbers are equal")
        except AssertionError as error:
            Asserts.assertWithin("Numbers are equal", str(error))

    @test
    def none_pass(self):
        assert isinstance(none(), Callable)
        assert assertThat(None, none())

    @test
    def none_fail(self):
        try:
            assertThat(12, none(), "Custom Message")
        except AssertionError as error:
            Asserts.assertWithin("Custom Message", str(error))

    @test
    def not_none_pass(self):
        assert isinstance(notNone(), Callable)
        assert assertThat(12, notNone())

    @test
    def not_none_fail(self):
        try:
            assertThat(12, notNone(), "Custom Message")
        except AssertionError as error:
            Asserts.assertWithin("Custom Message", str(error))

    @test
    def raises_plass(self):
        assert isinstance(raises(), Callable)
        assert assertThat(self.raises_lookup, raises(LookupError))
        assert assertThat(self.raises_lookup, raises())

    @test
    def raises_fail(self):
        try:
            assertThat(self.raises_lookup, raises(AssertionError), "Custom Message")
        except AssertionError as error:
            Asserts.assertWithin("Custom Message", str(error))

        try:
            assertThat(self.raises_nothing, raises(), "Custom Message")
        except AssertionError as error:
            Asserts.assertWithin("Custom Message", str(error))

    @test
    def within_pass(self):
        assert isinstance(within(None), Callable)
        assert assertThat("dog", within(["dog", "cat"]))
        assert assertThat("dog", within("Can you play with the dog?"))

    @test
    def within_fail(self):
        try:
            assertThat("dog", within(None), "Custom Message")
        except AssertionError as error:
            Asserts.assertWithin("Custom Message", str(error))

    @test
    def has_pass(self):
        assert isinstance(has(None), Callable)
        assert assertThat(["dog", "cat"], has("dog"))
        assert assertThat("Can you play with the dog?", has("dog"))

    @test
    def has_fail(self):
        try:
            assertThat([], has("dog"), "Custom Message")
        except AssertionError as error:
            Asserts.assertWithin("Custom Message", str(error))


if __name__ == "__main__":
    TestSuite(
        name="Asserts",
        tests=[
            Assert_Equal,
            Assert_Raises,
            Assert_Within,
            Assert_None,
            Assert_That,
            is_true,
        ],
    ).run().save(location="./Outputs", ext=SaveType.TXT)

    run(is_fail)
