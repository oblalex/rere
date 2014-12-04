# `rere`: regex redone

```python
from rere import *

money_regex = Exactly('$') + Digit*2 + (Exactly('.') + Digit*2).zero_or_one

money_regex.match('$23.95') # ==> MatchObject(...)
```

Isn't this better than `re.compile('\\$\\d\\d(\\.\\d\\d)?')`?

## Installation

Run the following command to install:

    pip install rere

This may require root (`sudo`).

Python 2.7+ and 3.3+ are supported.

## Usage

To get started using `rere`, you need to know the logic of the regular
expression pattern that you wish to build. To learn more about regular
expressions and their usage, please visit [Wikipedia: Regular
Expression](http://en.wikipedia.org/wiki/Regular_expression).

Once you know what sort of pattern you wish to match strings against, you can
use `rere` to automatically generate the string patterns that you wish to use.
Additionally, there is functionality built in to `rere` to call Python's
built-in `re` library to do the matching for you (`match()` or
`match_prefix`).

See above for the example.

## API

### Regex Components

The following components can be used individually, or added together (with `+`)
create compound regexes.

#### `Exactly`

```python
Exactly(string)
```

-   `string`: the string that is exactly what you want to match against

Use exactly to describe a part of a regex that you wish to be the exact
string of your choosing.

For example, if you want to match for the exact string, 'cat',

```python
regex = Exactly('cat')
regex.match('cat') # ==> MatchObject(...)
regex.match('Cat') # ==> None
regex.prefix_match('catapult') # ==> MatchObject(...)
regex.prefix_match('bobcat') # ==> None
```

`Exactly` takes care of any required escaping, so you can do things like:

```python
regex = Exactly('$2.00\n')
regex.match('$2.00\n') # ==> MatchObject(...)
````

(If you had to write a raw regex for the above, it might look something
like `re.compile('\\$2\\.00\\\n')`. Ew.)

#### `AnyChar`

```python
AnyChar
```

Use `AnyChar` when you want to match any single character (special or
otherwise, including newlines).

```python
regex = Exactly('hello') + AnyChar
regex.match('hello!') # ==> MatchObject(...)
regex.match('hello1') # ==> MatchObject(...)
regex.match('hello!!') # ==> None
regex.match('hello\n') # ==> MatchObject(...)
```

#### `Digit`

```python
Digit
```

Use `Digit` when you want to match any single digit (from 0 to 9).

```python
regex = Exactly('hello') + Digit
regex.match('hello!') # ==> None
regex.match('hello1') # ==> MatchObject(...)
regex.match('hello09') # ==> None
```

#### `Letter`

```python
Letter
```

Use `Letter` when you want to match any English letter (case insensitive).

```python
regex = Exactly('hello') + Letter
regex.match('helloB') # ==> MatchObject(...)
regex.match('hellob') # ==> MatchObject(...)
regex.match('hello9') # ==> None
regex.match('hello\n') # ==> None
regex.match('helloBb') # ==> None
```
#### `Whitespace`

```python
Whitespace
```

Use `Whitespace` when you want to match whitespace (`[ \t\n\r\f\v]`).

```python
regex = Exactly('hi') + Whitespace
regex.match('hi ') # ==> MatchObject(...)
regex.match('hi\n') # ==> MatchObject(...)
regex.match('hi b') # ==> None
```

#### `Anything`

```python
Anything
```

Use `Anything` when you want to match absolutely anything (special or
otherwise, including newlines). The empty string will also be matched.

```python
regex = Exactly('hello') + Anything
regex.match('hello!') # ==> MatchObject(...)
regex.match('hello!!') # ==> MatchObject(...)
regex.match('hello\n') # ==> MatchObject(...)
regex.match('Hellohello') # ==> None
```

#### `StringStart`

```python
StringStart
```

Use `StringStart` when you want to match beginning of string.

```python
regex = StringStart + Exactly(r'pony') + Anything
regex.match('pony') # ==> MatchObject(...)
regex.match('pony is a little horse') # ==> MatchObject(...)
regex.match('') # ==> None
regex.match(' pony ') # ==> None
```

#### `StringEnd`

```python
StringEnd
```

Use `StringEnd` when you want to match end of string.

```python
regex = Anything + Exactly(r'zebra') + StringEnd
regex.match('zebra') # ==> MatchObject(...)
regex.match('striped as zebra') # ==> MatchObject(...)
regex.match('') # ==> None
regex.match(' zebra ') # ==> None
```

#### Word boundaries

```python
WordStart
WordEnd
```

Use `WordStart` and `WordEnd` when you want to match word boundaries.

```python
regex = Anything + WordStart + Exactly('is') + WordEnd + Anything
regex.match('This island is beautiful.') # ==> MatchObject(...)
regex.match('This island was beautiful.') # ==> None
```

#### `RawRegex`

```python
RawRegex(pattern)
```

-   `pattern`: a string containing a raw regex (using the syntax from `re`)

Simply match the provided regular expression. This allows you to use legacy
regexes within `rere` expressions.

For example, if you have an existing regex for phone numbers (like
`r"\(\d\d\d\) \d\d\d-\d\d\d\d"`), and you want to match one or more of
them:

```python
regex = RawRegex(r"\(\d\d\d\) \d\d\d-\d\d\d\d").one_or_more
```

### Combining Components

All regex components implement several common functions. They can be combined
and nested in many ways, such as:

```python
regex = (Exactly('cat') + Exactly('dog').zero_or_one).one_or_more
regex.match('catcatdogcatdogcatdog') # ==> MatchObject(...)
regex.match('catdogdog') # ==> None
```

#### `regex.zero_or_one`

Use the `zero_or_one` property to describe how many repetitions of a string are
required to match the pattern, in this case, only zero or one.

```python
regex = Exactly('ab').zero_or_one
regex.match('aba') # ==> None
regex.match('ab') # ==> MatchObject(...)
regex.match('') # ==> MatchObject(...)
```

#### `regex.zero_or_more`

Use the `zero_or_more` property to describe how many repetitions of a string are
required to match the pattern, in this case, any number (zero or more).

```python
regex = Exactly('ab').zero_or_more
regex.match('ababab') # ==> MatchObject(...)
regex.match('ab') # ==> MatchObject(...)
regex.match('') # ==> MatchObject(...)
regex.match('aba') # ==> None
```

#### `regex.one_or_more`

Use the `one_or_more` function to describe how many repetitions of a string are
required to match the pattern, in this case, at least one.

```python
regex = Exactly('ab').one_or_more
regex.match('ababab') # ==> MatchObject(...)
regex.match('ab') # ==> MatchObject(...)
regex.match('') # ==> None
regex.match('aba') # ==> None
```

#### `regex.as_group`

```python
regex.as_group(name)
```

-   `name`: the name of your group

You can assign a your regex part to a group. This allows those who want to
use re's group functionality an easy way of working with it.

For example, say you want to group dollars and cents separately for a money
regex.

```python
regex = (Exactly('$') + Digit.one_or_more.as_group('dollars') +
         Exactly('.') + (Digit * 2).as_group('cents'))
match = regex.match('$24.13')
match.groupdict() # ==> {'dollars': '24', 'cents': '13'}
```

#### Addition (`+`)

You can form a regex from separate parts and combine them together with the
`+` sign.

```python
regex = Exactly('cat') + Exactly('dog')
regex.match('catdog') # ==> MatchObject(...)
```

#### Multiplication (`*`)

If you want a part (or a full) regex to be repeated a specified number of times,
use the `*` sign.

```python
regex = Exactly('cat') * 2
regex.match('catcat') # ==> MatchObject(...)
```

You can specify minimal number of repetitions:

```python
regex = Exactly('cat') * (2, )
regex.match('cat') # ==> None
regex.match('catcat') # ==> MatchObject(...)
regex.match('catcatcat') # ==> MatchObject(...)
```

And you can also specify maximal number of repetitions:

```python
regex = Exactly('cat') * (2, 3)
regex.match('cat') # ==> None
regex.match('catcat') # ==> MatchObject(...)
regex.match('catcatcat') # ==> MatchObject(...)
regex.match('catcatcatcat') # ==> None
```


#### Or (`|`)

If need "Either or" logic for your regex, use `|`.

```python
regex = Exactly('cat') | Exactly('dog')
regex.match('cat') # ==> MatchObject(...)
regex.match('dog') # ==> MatchObject(...)
regex.match('fish') # ==> None
```
