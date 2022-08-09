### 1.2.0
#### New

+ Pretty Exceptions
+ Colored and clickable tracebacks
  * For both exceptions and failed tests
+ Test now have verbosity filtering.
  * This means by default running tests will show the overall score
  * Additional filters can be added to add additional information
    * This information includes, passed, failed, skipped, and only totals.
    * The filters can be mixed an matched to meet a users needs


#### Modified

+ Optimized readability
  * Includes json, verbose terminal out, exceptions, etc...
+ Rewrote assertThat module
  * Now uses a `Matcher` decorator for the second argument.
  * Can customize what the matcher accepts
  * Return the result and the message for checking the match/condition
  * assertThat will throw an AssertionError if matcher fails

#### Removed
- Testing and Temporary files

___

### 1.1.0

#### New

+ Add TEDTest CLI tool
  * Auto detects tests and runs them
  * Has same functionality as a TestSuite

___

### 1.0.0

#### New

+ Add Testing
  * Test Suite
  * Test Classes
  * Test Cases
  * Save results to file
  * Display results to terminal
  * Filter tests with regex
+ Add TED markup parser
  * Parse
    * Hyperlinks
    * Precise colors; foreground, background, both
    * Custom functions - Custom functions manipulate the next plain text block
  * Print
  * Define custome functions
