from teddecor import TED


def hello_world(string: str) -> str:
    return "Hello World"


if __name__ == "__main__":
    TED.define(name="hw", callback=hello_world)
    TED.print("[^hw]Dog goes moo")
