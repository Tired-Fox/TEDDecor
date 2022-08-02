class Raises:
    """Assert that the code run inside the `with` keyword raises an exception."""

    def __init__(self, exception: Exception = Exception):
        self._exception = exception

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val is not None:
            if not isinstance(exc_val, self._exception):
                raise AssertionError(
                    f"Unexpected exception raised {exc_val.__class__}"
                ) from exc_val
        else:
            raise AssertionError("No exception raised")


if __name__ == "__main__":
    with Raises(AssertionError):
        pass
