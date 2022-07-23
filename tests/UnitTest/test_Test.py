from teddecor.UnitTest import *


class TestTesting(Test):
    
    @test
    def test_pass(self):
        assert True

    @test
    def test_fail(self):
        assert False


class TestResults(Test):
    def __init__(self):
        super().__init__()
        self.result = TestTesting().main(False)

    @test
    def result_format(self):
        Asserts.assert_equal(type(self.result), dict)

    @test
    def result_content(self):
        Asserts.assert_equal(self.result, {
            "TestTesting" : {
                "test_pass": {
                    "result": "Passed",
                    "stack": ""
                    },
                "test_fail": {
                    "result": "Failed",
                    "stack": ["[test_Test.py:12] test_fail", "[Error Message] Assertion Failed"]
                    }
                }
            })

if __name__ == "__main__":
    TestResults().main()

