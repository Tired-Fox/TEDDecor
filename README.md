# TEDDecor
This is a easy to use library with testing, documentation, and docstring example tools. Dive in with minimal effort and get great resutls. 

## Testing

With testing it is as simple as importing the `UnitTest` module, `from teddecor.UnitTest import *` or `from teddecor import UnitTest`, then building a test class with test cases (functions).

Take this example test (`example.py`)

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
> You can not use the keyword `totals` as a function name by itself

**Results:**

<p align="center">
  <img src="images/example_test.png" alt="Example Test Results">
</p>

<p align="center" style="bold">
  Check out the documentation for more testing features!!!
<p>
