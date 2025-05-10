# RegexFSM Project

## Overview

This project implements a simple regular expression finite state machine (FSM) in Python. It supports basic regex features such as:
- Single characters (e.g., `a`, `b`, `1`)
- Dot (`.`) for any character
- Character classes (e.g., `[a-zA-Z0-9]`)
- Star (`*`) for zero or more repetitions
- Plus (`+`) for one or more repetitions

## Main Components

- `regex.py`: Contains the FSM implementation, including state classes and the main `RegexFSM` class.
- `test_regex.py`: Contains unit tests for various regex patterns and edge cases.

## Usage

To use the FSM, create a `RegexFSM` object with a pattern and call `check_string`:

```python
from regex import RegexFSM

regex = RegexFSM("a*4.+hi")
print(regex.check_string("aaaaaa4uhi"))  # True
print(regex.check_string("4uhi"))        # True
print(regex.check_string("meow"))        # False
```

## Features

- Supports ASCII letters and digits.
- Handles character classes and ranges (e.g., `[a-z]`).
- Implements `*` and `+` quantifiers.
- Accepts dot (`.`) as a wildcard.
- Raises errors for unsupported characters or malformed patterns.

## Testing

Unit tests are provided in `test_regex.py` and cover:
- Simple patterns
- Dot and plus quantifiers
- Character classes and ranges
- Edge cases (empty strings, unsupported characters, malformed patterns)

Run tests with:

```
python -m unittest test_regex.py
```

## Example Patterns

| Pattern         | Description                        | Example Match      |
|-----------------|------------------------------------|--------------------|
| `a*`            | Zero or more `a`                   | `""`, `"aaa"`      |
| `a+`            | One or more `a`                    | `"a"`, `"aaaa"`    |
| `.`             | Any single character               | `"b"`, `"1"`       |
| `[a-zA-Z0-9]`   | Any ASCII letter or digit          | `"a"`, `"Z"`, `"5"`|
| `[a-z]*4*`      | Letters a-z and/or digit 4, any #  | `"aaaa444"`, `"4"` |

## Limitations

- Only supports a subset of regex syntax.
- Does not support nested groups, alternation (`|`), or advanced features.
