from teddecor import TED

# There are include macros that will do cool affects like make the passed text rainbow
TED.pprint("[^rainbow|Rainbow Text]")
# There is also an included macro for displaying hyperlinks
TED.pprint("[~https://tired-fox.github.io/TEDDecor/teddecor.html|Documentation]")
# There is currently also a macro for outputing a string literal
# For example if you have special escape character and want to print there literals then you can do
TED.pprint("[^repr|\x1b[0m]")

# Macros can be nested, but this is really only useful if you want to stype your hyperlinks atm
# Colors can be passed with many formats... the one below shows rgb which can be seperated with both `,` and `;`
TED.pprint(
    "[~https://github.com/Tired-Fox/TEDDecor|*TEDDecor [@F138,43,226]Github [@F220;20;60][@B255;255,255]page]"
)

# Here is passing colors as hex and xterm color codes. Hex must have a `#` in front of it
TED.pprint("[@F#83a748]HEX[@F] and [@F206]XTERM")

# Colors can also be passed in with default build in terminal color codes.
# These include black, red, green, yellow, blue, magenta, cyan, and white
TED.pprint("[@Fcyan]Predefined Color")

# The `@` is a color macro and the F or B immediatly following it is whether to apply it to the foreground or background
# You can use a [@F] or [@B] to reset the foreground and background colors respectively
# You can also use [@] to reset both foreground and background

# TED also has markdown syntax for underline and bold. Bold = * and underline = _ , with each only using one character.
# When a character is used it toggles the bold or underline state.
TED.pprint("Normal, _Underlined_, *Bold*, Normal, *Bold, _Bold and Underline")

# Notice how the Bold, Underline, colors and other formatting doen't need to closed or wrap the intended text.
# This is intentional as you specify when it should stop.
# If you want to reset everything, both color and style, then you can use `[]`.

TED.pprint("[@Fred]*I have a color and style[], and I don't")

# TED also has rich exceptions that are called when you don't close a macro, don't specify the macro type, or don't
# specify if a color is for the background or foreground

# # Additionally, if you want to display the special characters, `[`, `]`, `*`, and `_` you can use the `\` escape character.
# TED.pprint("\[@Fred] Is one way you can make the text red")

# Escaping `[` will also automatically escape the `]`. However, if you want to escape macros when they are nested you will need
# to escape both `[` and `]`. Use 3 backslashes `\\\` to fully escape as it consume one to escape the brack and you need to escape the escape character.
TED.pprint(
    "[~https://tired-fox.github.io/TEDDecor/teddecor.html|\\\[^rainbow|Documentation\\\]]"
)

# This is a literal block to show what will be output next
TED.pprint(
    "\[~https://tired-fox.github.io/TEDDecor/teddecor.html|\[^rainbow|Documentation\]\]"
)
# Now for the output
TED.pprint(
    "[~https://tired-fox.github.io/TEDDecor/teddecor.html|[^rainbow|Documentation]]"
)
