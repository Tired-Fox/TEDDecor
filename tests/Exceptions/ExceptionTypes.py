from teddecor.UnitTest import *
from teddecor.Exceptions import *


class BaseType(Test):
    @test
    def message_default(self) -> None:
        result = BaseException()
        assertThat(result.message, eq("An unknown error occured"))

    @test
    def message_custom(self) -> None:
        result = BaseException(message="This is a base exception")
        assertThat(result.message, eq("This is a base exception"))

    @test
    def stack(self) -> None:
        result = BaseException()
        assertThat(len(result.stack), gt(1))


class HintingType(Test):
    @test
    def message_default(self) -> None:
        result = HintedException("Some Value", 1, "Some hint")
        assertThat(result.message, eq("Error with specific value"))

    @test
    def message_custom(self) -> None:
        result = HintedException("Some Value", 1, "Some hint", message="Custom Message")
        assertThat(result.message, eq("Custom Message"))

    @test
    def stack(self) -> None:
        result = HintedException("Some Value", 1, "Some hint")
        assertThat(len(result.stack), gt(1))

    @test
    def value(self) -> None:
        result = HintedException("Some Value", 1, "Some hint")
        assertThat(result.value, eq("Some Value"))

    @test
    def hint(self) -> None:
        result = HintedException("Some Value", 1, "Some hint")
        assertThat(result.hint, eq("Some hint"))

    @test
    def index(self) -> None:
        result = HintedException("Some Value", 1, "Some hint")
        assertThat(result.index, eq(1))


class MissingValueType(Test):
    @test
    def message_default(self) -> None:
        result = MissingValueException("Is this practical", 18, "?")
        assertThat(result.message, eq("Missing Value"))

    @test
    def message_custom(self) -> None:
        result = MissingValueException(
            "Is this practical", 18, "?", message="Custom Message"
        )
        assertThat(result.message, eq("Custom Message"))

    @test
    def stack(self) -> None:
        result = MissingValueException("Is this practical", 18, "?")
        assertThat(len(result.stack), gt(1))

    @test
    def value(self) -> None:
        result = MissingValueException("Is this practical", 18, "?")
        assertThat(result.value, eq("Is this practical"))

    @test
    def missing(self) -> None:
        result = MissingValueException("Is this practical", 18, "?")
        assertThat(result.missing, eq("?"))

    @test
    def index(self) -> None:
        result = MissingValueException("Is this practical", 18, "?")
        assertThat(result.index, eq(18))
