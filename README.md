# TEDDecor
This is a easy to use library with testing, documentation, and docstring example tools. Dive in with minimal effort and get great resutls. 

## Testing

With testing, it is as simple as importing the `UnitTest` module, `from teddecor.UnitTest import *` or `from teddecor import UnitTest`, then building a test class with test cases (functions).

Below are a few generic levels of testing which can be mixed together however you want.

1. Use the provided `runTest` function to run a single method with the `@test` decorator
    ```python
    @test
    def test_case():
        assert True

    if __name__ == "__main__":
        runTest(test_case)
    ```

2. Use the provided `Test` class to group test cases (functions) with the `@test` decorator.
   * This meant to group test that are focuses on a specific functionality
    ```python
    class TestClass(Test):
        @test
        def test_case(self):
            assert True

    if __name__ == "__main__":
        TestClass().run()
    ```

3. Use the provided `TestSuite` class to group test classes and test cases together
   * This is meant to group a more general idea. Like the tests for a app can be split into backend and front end. Where both backend and frontend are their own test suite. Then inside the suites you get more focuses.
    ```python
    class BackendInput(Test):
        @test
        def user_input(self):
            assert True
        
        @test
        def file_input(self):
            assert True

    @test
    def app_response():
        raise NotImplementedError

    if __name__ == "__main__":
        TestSuite(
            name="Backend"
            tests=[
                BackendInput,
                app_response,
            ]
        ).run()
    ```

   *  As you can see in the above example, you can use `raise NotImplementedError` to skip a test which also gives the message of `Not Implemented`
  
Below is an example test (`example.py`)

```python
from teddecor.UnitTest import *

class Example(Test):
  @test
  def test_pass(self):
    assert True

if __name__ == "__main__":
  Example().main()
```

The above example shows that you need to have a class that inherits from `UnitTest.Test`. Then when you run the `main()` function from an instance of that class,
you get the results printed out. The `main()` function will run any method in the class that has the `@test` decorator.

> NOTE:
> You can not use the keyword `totals` as a function name by itself inside of test suites and classes

**Results:**

<p align="center">
  <img src="images/example_test.png" alt="Example Test Results">
</p>

Since this package is used to test itself, feel free to look through the files in the repo's `tests/` folder to see **examples** and **outputs** of testing.

<p align="center" style="bold">
  To see more testing features like, mocking, setup, result save file types, etc... see the <a href="https://tired-fox.github.io/TEDDecor/teddecor.html" title="Docs" target="_blank">documentation</a>.
<p>
