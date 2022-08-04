from teddecor.UnitTest import *


class NonTestClass:
    pass


class IsTestClass(Test):
    @test
    def example(self):
        pass


def NonTestFunc():
    pass


@test
def IsTestFunc():
    pass
