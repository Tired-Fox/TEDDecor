from teddecor.UnitTest import *

class CustomObject():
    def __init__(self, index: int):
        self._index = index

    @property
    def index(self):
        return self._index

class Assert_Equal(UnitTest):
    @test
    def assert_equal_fail_default_message(self):
        try:
            asserts.assert_equal("dog", "cat")
        except AssertionError as error:
            assert "Left operand not equal to right operand" in str(error)
        
        try:
            asserts.assert_equal("dog", "cat", message="Dog is not equal to cat")
        except AssertionError as error:
            assert "Dog is not equal to cat" in str(error)

    @test
    def assert_equal_pass(self):
        co = CustomObject(10)
        asserts.assert_equal(co.index, 10)


class Assert_Raises(UnitTest):
    def raises_lookup_error(self):
            raise LookupError()

    @test
    def assert_raise_pass(self):
        def raises_lookup_error():
            raise LookupError()
        
        asserts.assert_raises(LookupError, self.raises_lookup_error)

    @test
    def assert_raise_unexpected_exception(self):
        try:
            asserts.assert_raises(BufferError, self.raises_lookup_error)
        except AssertionError as error:
            assert "Unexpected exception LookupError" in str(error)

        try:
            asserts.assert_raises(BufferError, self.raises_lookup_error, "Custom Message")
        except AssertionError as error:
            assert "Custom Message" in str(error)
            
   
    @test
    def assert_raise_no_exception(self):
        try:
            asserts.assert_raises(LookupError, lambda *_: None)
        except AssertionError as error:
            assert "No exception raised" in str(error)

        try:
            asserts.assert_raises(LookupError, lambda *_: None, "Custom Message")
        except AssertionError as error:
            assert "Custom Message" in str(error)


class Assert_Contains(UnitTest):
    def __init__(self):
        super().__init__()
        self.content = "Hello World!"

    @test
    def assert_contains_pass(self):
        asserts.assert_contains("Hello", self.content)

    @test
    def assert_contains_does_not_contain(self):
        try:
            asserts.assert_contains("universe", self.content)
        except AssertionError as error:
           assert "[Hello World!] does not contain [universe]" in str(error)

        try:
            asserts.assert_contains("universe", self.content, "Custom Message")
        except AssertionError as error:
           assert "Custom Message" in str(error)
           
    @test
    def assert_custom_message(self):
        try:
            asserts.assert_contains("universe", self.content, "Custom Message")
        except AssertionError as error:
            assert "Custom Message" in str(error)


if __name__ == "__main__":
    classes = [Assert_Equal(), Assert_Raises(), Assert_Contains()]
    for klass in classes:
        klass.main()
        print('\n······························\n')
