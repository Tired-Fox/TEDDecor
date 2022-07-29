"""TED

TED is the name for the inline markup language for this library. This allows the user to customize strings and prettyprint different information to stdout.

Includes:

* parse -> returns formatted strings
* pprint -> parse TED markup strings and display them to stdout
* More to come...

Syntax:

Brackets `[]` indicate a macro. Macros can do 1 of three things; Assign a foreground/background color,
create a hyperlink, and call a builtin function. All macros will ignore extra whitespace and focus on the identifiers; `@`, `~`, and `^`.

1. Colors
    * Colors start with a leading identifier `@`. To indicate foreground or background use the specifier `F` and `B` respectively.
    Following the `@` and the specifier you can then enter the color. 
        * This can be a predifined color such as; black, red, green, yellow, blue, magenta, cyan, white. `[@F black]`.
        * It can be a hex code `#ead1a8`. `[@F #ead1a8]`.
        * It can be a XTerm code 0-256. `[@F 9]`.
        * Lastely, it can be an rgb color where the 3 numbers can be seperated by a `,` or a `;`. `[@F 114;12,212].
    * Colors can be reset with `[@F]` or `[@B]` to reset foreground or background respectively or `[@]` can be use to reset both.
    * Foreground and background can be specified in the same macro `[@F 1 @B 2], but they can not be reset in the same macro `[@F @B]`, use `[@]` instead.
    * While the macro will ignore white space and you can do something like `[@F#ead1a8@B3]` it is preferred to use whitespace for readability `[@F #ead1a8 @B 3]`.

2. Hyperlinks
    * Hyperlinks start with a leading identifier `~`.
    * Hyperlinks have two modes; raw link mode and pretty link mode.
        * Raw link mode is where the specified url is displayed as the hyperlink. 
            * `[~https://example.com]` -> `https://example.com`.
        * Pretty link mode is where the specified TED markup is used as the display for the hyperlinke. This means you can nest macros inside of a hyperlink.
            * `[~https://example.com|example]` -> `example`.
            * `[~https://example.com|[@F red]example]`.
            * `[~https://exmaple.com|[^rainbow|example]]`.
            
3. Builtin functions
    * Builtin functions start with the identifier `^`. They are also structure as `[^func|string]`, where func is the built in function and string is the value to pass to it.
    * The `|` is required and the string can be blank as `""` will be passed to the function.
    * The builtin function takes the given string processes it and returns the resulting string.
    * Examples:
        * `[^rainbow|rainbow text]` will return the string with a rainbow foreground color.
        * `[^repr|string]` will return the repr of the string. Good for displaying TED markup without processing it, and for displaying escape characters.

TED also follows some inspiration from markdown where `*` means toggle bold and `_` means to toggle underline.
To reset all attributes, color and formatting, use the empty brackets `[]`.
"""
from .TED import *
