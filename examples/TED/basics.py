from teddecor import TED

# There are include macros that will do cool affects like make the passed text rainbow
TED.pprint("[^rainbow]Rainbow Text")
# There is also an included macro for displaying hyperlinks
TED.pprint("[~https://tired-fox.github.io/TEDDecor/teddecor.html]Documentation")
# There is currently also a macro for outputing a string literal
# For example if you have special escape character and want to print there literals then you can do
TED.pprint("[^repr]\x1b[0m")

# You can also define your own macros. These are functions that will manipulate the next test block
# They must take a string as a parameter and return a string as an output. If it doesn't return a string the function won't have an effect.
def hello_world(string: str) -> str:
    return "Hello World"


# You let TED know about the function before you can call it.
# You give the function a name which you use to call it in a macro then you pass the callable function.
TED.define("hw", hello_world)
TED.print("[^hw]Cat goes moo")

# Macros can be nested, but this is really only useful if you want to stype your hyperlinks atm
# Colors can be passed with many formats... the one below shows rgb which can be seperated with both `,` and `;`
TED.pprint(
    "[~https://github.com/Tired-Fox/TEDDecor]*TEDDecor[@>138,43,226]Github [@>220;20;60 @<255;255,255]page"
)

# Here is passing colors as hex and xterm color codes. Hex must have a `#` in front of it
TED.pprint("[@> #83a748]HEX[@>] and [@>206]XTERM")

# Colors can also be passed in with default build in terminal color codes.
# These include black, red, green, yellow, blue, magenta, cyan, and white
TED.pprint("[@> cyan]Predefined Color")

# The `@` is a color macro and the `>` or `<` immediatly following it is whether to apply it to the foreground or background
# You can use a [@>] or [@<] to reset the foreground and background colors respectively
# You can also use [@] to reset both foreground and background

# TED also has markdown syntax for underline and bold. Bold = * and underline = _ , with each only using one character.
# When a character is used it toggles the bold or underline state.
TED.pprint("Normal, _Underlined_, *Bold*, Normal, *Bold, _Bold and Underline")

# Notice how the Bold, Underline, colors and other formatting doen't need to closed or wrap the intended text.
# This is intentional as you specify when it should stop.
# If you want to reset everything, both color and style, then you can use `[]`.

TED.pprint("[@>red]*I have a color and style[], and I don't")

# TED also has rich exceptions that are called when you don't close a macro, don't specify the macro type, or don't
# specify if a color is for the background or foreground

# # Additionally, if you want to display the special characters, `[`, `]`, `*`, and `_` you can use the `\` escape character.
# TED.pprint("\[@Fred] Is one way you can make the text red")

# Escaping `[` will also automatically escape the `]`.
TED.pprint(
    "[~https://tired-fox.github.io/TEDDecor/teddecor.html]\[^rainbow]Documentation"
)
# If you have a long string that you want to escape you can use `TED.encode`
TED.pprint(
    TED.encode(
        "[] _This wil be * a literal where_ you see __ the markdown * characters"
    )
)

# This is a literal block to show what will be output next using `\`
TED.pprint(
    "\[~https://tired-fox.github.io/TEDDecor/teddecor.html ^rainbow]Documentation"
)
# Now for the output
TED.pprint(
    "[~https://tired-fox.github.io/TEDDecor/teddecor.html ^rainbow]Documentation"
)
