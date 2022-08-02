from teddecor.UnitTest import *

# Tests can be made as standalone cases
@test
def standalone():
    assert True


# Tests can also be grouped into classes.
# To mock and create data on setup for your tests to use, use the __init__ function
# And since the class only runs the tests with the `@test` decorator you can make as many helper functions
# as you want.
class Basics(Test):
    def __init__(self):
        # Initialize information for later
        self.message = "Hello World!"

    def getMessage(self) -> str:
        """This is a helper function which is ignored by the test run."""
        return self.message

    @test
    def example_1(self):
        """What it looks like if a test passes."""
        assert True

    @test
    def example_2(self):
        """What it looks like when a test fails."""
        assert False

    @test
    def example_3(self):
        """What it looks like to skip a test."""
        raise NotImplementedError


# Asserting something is true is the  most important part of a test.
# This library provides an easy to use and read way of writing test, or you can just use assert :)
class AssertThat(Test):
    def helper(self, num: int) -> bool:
        if num > 100:
            return False
        else:
            return True

    def raises_error(self, exception: Exception = Exception):
        raise exception("An error was found")

    @test
    def assertThat(self):
        # assertThat is the enforced way of writing test in this library
        # It makes test easy to read and give additional functionality to the user
        assertThat("The", eq("The"))

    @test
    def assertThat_custom_message(self):
        # There is an additional feature that allows you to provide your own error messag when an assert fails.
        # This message will show up in the test results.
        assertThat(3, none(), "assertThat custom error message")

    @test
    def assertThat_raises(self):
        # Something that is useful is checking if a function throws an error when called.
        # With assert that it is requested that the first parameter is some callable object which is called later.
        # In general assertThat should only be used for testing raise conditions when there is a single call.

        # The second parameter is raises() where if it has no parameters expects any exception
        # otherwise you can specify it.
        assertThat(self.raises_error, raises())

        # There is a provided wrap function that allows you to provide a function and parameters
        # which is called later when it checks the condition.
        assertThat(wrap(self.helper, None), raises(TypeError))

        # If you need to do more complex logic or feel that assertThat isn't a great format there
        # is the `with Raises(Exception):` format.
        # This way you only need to call the code you expect will raise an error inside the block.
        with Raises(TypeError):
            self.raises_error(TypeError)

    # Make sure to check out the documentation for a full list of provided functions like eq (equals)
    # and raises along with a guide on how to make your own.


if __name__ == "__main__":
    # Now for how to run your tests.
    # All run functions have a argument that specifies whether to display the results to stdout or not.
    # Default is True
    # Each run function also returns a Result object that gives additional data manipulation

    # You can use the provided run() function to run standalone test cases
    standalone_result = run(standalone, display=False)

    # You can print the results later or as many times as you want with the write function
    standalone_result.write()

    # All result objects also give you the option to save the data to a file in 3 different formats or any combination of them.
    # JSON, CSV, or TXT. Use ALL to output to all types
    standalone_result.save(ext=SaveType.TXT)

    # You can also run classes by creating an instance and running it's associated run function
    Basics().run()

    # Now for the test suite. This is an object that is set up with the __init__ function
    # Test suites group both standalone tests and test classes together
    suite = TestSuite(name="ExampleTests", tests=[Basics, AssertThat, standalone])

    # Don't forget you can chain things like run and save so you can compact the code
    suite = (
        TestSuite(name="ExampleTests", tests=[Basics, AssertThat, standalone])
        .run(regex="assertThat")
        .save()
    )

    # You can also the regex argument on test suites and test classes to specify specific tests to run.
    # The regex uses the re.match function

    # Now to run the code!!!
    # See how the output of running the run() function or calling write() looks. Also check out the new TXT and CSV files.

    # CLI tool coming soon!
