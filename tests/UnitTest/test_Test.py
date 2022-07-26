from teddecor.UnitTest import *


class TestTesting(Test):
    @test
    def test_pass(self):
        assert True

    @test
    def test_fail(self):
        assert False

    @test
    def test_notimplemented(self):
        raise NotImplementedError


class TestResults(Test):
    def __init__(self):
        super().__init__()
        self.result = TestTesting().run(False)

    @test
    def result_format(self):
        Asserts.assertEqual(type(self.result), dict)

    @test
    def result_content(self):
        Asserts.assertEqual(
            self.result,
            {
                "TestTesting": {
                    "totals": (1, 1, 1),
                    "test_pass": {"result": "Passed", "info": ""},
                    "test_fail": {
                        "result": "Failed",
                        "info": [
                            "[test_Test.py:12] test_fail",
                            "[Error Message] Assertion Failed",
                        ],
                    },
                    "test_notimplemented": {
                        "result": "Skipped",
                        "info": "Not Implemented",
                    },
                }
            },
        )


if __name__ == "__main__":
    TestResults().run()
