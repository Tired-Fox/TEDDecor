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
        self.result_class = TestTesting().run(False)
        self.result_func = run(TestTesting().test_pass, display=False)

    @test
    def result_format(self):
        assertThat(type(self.result_class), eq(ClassResult))
        assertThat(type(self.result_func), eq(TestResult))

    @test
    def result_content(self):
        pass


if __name__ == "__main__":
    TestSuite(name="TestSuite", tests=[TestTesting, TestResults],).run(
        regex=r"result"
    ).save(location="./Outputs", type=SaveType.TXT)

    TestResults().run(regex=".*format").save(location="./Outputs", ext=SaveType.TXT)
