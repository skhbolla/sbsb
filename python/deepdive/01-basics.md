# Type heirarchy 

> The following is only a subset of the python type heirarchy. There are more types

- Numbers
	- Integral
		- Integers
		- Booleans
	- Non-Integral
		- Floats
		- Complex
		- Decimals
		- Fractions
- Collections
	- Sequences
		- Mutable
			- Lists
		- Immutable
			- Tuples
			- Strings
	- Sets
		- Mutable
			- Sets
		- Immutable
			- Frozen sets
	- Mappings
		- Dictionaries
- Callables
	- User defined functions
	- Generators
	- Classes
	- Instance methods
	- Class instances (`__call__()`)
	- Built in functions (eg. `len()`, `open()`)
	- Built in methods (eg. `my_list.append(x)`)
- Singletons
	- None
	- NotImplemented
	- Ellipsis `...`

---

# Multi-Line Statements and Multi-Line Strings

## Multi Line Statements
 One of the most coveted features of Python is it's readability. Take below code
 for example:

 ```python
 x = test(a, #First argument
        b #Second argument
        )
 ```

In above example, python supported the use of 'implicit line break' i.e we did not
have to specify to python that we are splitting a logical line into multiple physical lines.


But there are many cases where python cannot implicitly understand this.. 
So we use the explicit line break using the `\ (backslash)` character.
Below is an example:

```python

# This will not work
if a
    and b
    and c:

# This is perfectly valid
if a \
    and b \
    and c:

# This will raise syntax error 
# The backslash tells the Python parser to ignore the newline character immediately following it. 
# Adding a comment puts text between the backslash and the newline, breaking the line continuation rule.
if a \
    and b \ #SomeComment
    and c:

#Also note that in above example, the indentation of before `and b` does not matter.
# This is because python strips out the preceeding new line character (because we used backslash).

```

## Multi Line String Literals
Multi Line String Literals are created using triple delimiters (single and double quotes)

```python

''' This is a multi-line
string'''

""" This is also
a multi-line string"""

# It is very important to be aware that multi line string literals retain
# non-visible characters. ie if your multi line string has a new line or a tab character,
# they will not be stripped out.

# Multi line strings are just regular strings.
# Even though we use multi line strings as comments (docstrings), it is very
# important to understand that they are NOT comments. They are just a regualr string

```

---

# Variable names

1. Identifier names are **case-sensitive**
2. Must start with a letter or and underscore, followed by digits, letters or underscores
3. cannot use reserved words

## Conventions

1. Identifiers starting with a single underscore, are used to indicate 'internal' and 'private' objects
2. Identifiers starting with double underscores are used to "mangle" class attributes
3. Identifiers starting and ending with underscores are used for system-defined names that have a special meaning to the interpreter

## PEP 8 Style Guide
- packages: short, all lower case, preferably no underscores
- modules: short, all lower case, can have underscores
- Classes: CapWords (no spaces, first letter of each word capitalized)
- functions: lowercase, underscores to seperate words (snake_case)
- variables: lowercase, underscores to seperate words (snake_case)
- CONSTANTS: all uppercase, words seperated by underscores

---

# Conditionals
