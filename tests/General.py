from teddecor.Exceptions import HintedException, MissingValueException

if __name__ == "__main__":
    value = input("Enter an number greater than 9 and has length of at least 2: ")
    if value.startswith("-"):
        HintedException(
            value, 0, "Value must be positive", message="Negative Number"
        ).throw()
    elif int(value) < 10:
        MissingValueException(
            value, len(value), "[@ red] ", message="Value must be of length 2"
        ).throw()
