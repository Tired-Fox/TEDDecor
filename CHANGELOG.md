### 1.2.0

#### Decorators

+ Add misc utility Decorators
+ A new pretty print, `pprint`, method that colors and formats data and prints it to `stdout`
+ The new decorators include:
  - `deprecated` prints a colored deprecation warning to `stdout`
  - `not_implemented` raises a `NotImplementedError` with a colored signature of the decorated method or class
  - `Time` Times how long it takes for a method to run.
  - `debug` pretty prints, with color, the data that enters a method and the data that is returned, also prints a colored method signature.

___

### 1.1.1

#### Logger

+ Fixed method chaining

___

### 1.1.1

#### Logger

+ Fixed flushing to file removing ansi and TED markup

___

### 1.1.0

#### Logger

+ Add custom logging
  * This allows for logging to file and to stdout
  * Custom labels
  * Custom messages
  * Custom logging levels
  * Method chaining
  * Global instance
  * Buffers until flushed

___

### 1.0.0

#### TED

+ Add TED markup parser
  * Parse
    * Hyperlinks
    * Precise colors; foreground, background, both
    * Custom functions - Custom functions manipulate the next plain text block
  * Print
  * Define custome functions
