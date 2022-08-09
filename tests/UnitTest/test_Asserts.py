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


from typing import Callable


class Assert_That(Test):
    @test
    def eq(self):
        assert isinstance(eq(12), Callable)
        assertThat(12, eq(12))
        try:
            assertThat(12, eq(11))
        except AssertionError as error:
            assert "Actual value is not equal to the expected value." in str(error)

    @test
    def gt(self):
        assert isinstance(gt(12), Callable)
        assertThat(12, gt(10))
        try:
            assertThat(12, gt(15))
        except AssertionError as error:
            assert "Actual value is less than the expected value." in str(error)

    @test
    def lt(self):
        assert isinstance(lt(12), Callable)
        assertThat(12, lt(15))
        try:
            assertThat(12, lt(15))
        except AssertionError as error:
            assert "Actual value is greater than the expected value." in str(error)


if __name__ == "__main__":
    TestSuite(
        name="Asserts",
        tests=[
            Assert_Equal,
            Assert_Raises,
            Assert_That,
        ],
    ).run().save(location="./Outputs", ext=SaveType.TXT)
