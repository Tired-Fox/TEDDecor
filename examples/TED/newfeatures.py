from teddecor import TED

# You can nest macro's inside of eachother
# TED.pprint(
#     "[~https://tired-fox.github.io/TEDDecor/teddecor.html|[^rainbow|Documentation]]"
# )

# # You can place multiple colors in the same macro
# TED.pprint("[@F][@][@B]")
# TED.pprint("[@F 12;143;245 @B white]Some Compound macro")

# TED.pprint("[@F#123]Something")


# def return_purple_dog(value: str) -> str:
#     """Example method local to this module"""
#     return f"\x1b[38;5;63m{value} says *BARK*\x1b[39m"


# # If you have a function, local to the module that uses pprint, and it takes a string and returns a string
# # Then you can use your own function inside a macro
# TED.pprint("[^return_purple_dog|Dog]")

TED.pprint("[~example.com ^rainbow]Rainbow Link")
