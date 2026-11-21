# Important note on Tuples before discussing Unpacking

## What is a tuple ?

> A tuple in Python is a built-in collection data type 
> used to store multiple items in an ordered, unchangeable (immutable) sequence

What defines a tuple in python is not `()` but the `,`

Therefore, `1,2,3` is also a tuple.
We just use `()` to make the tuple clearer.

**What about creating a tuple with a single element ??**

`(1)` -> Will not work as intended.. It will create a `int` object instead.

```python

t = (1)
print(type(t))

```

So, use either `1,` or `(1, )` -> Create a tuple

**How to create an empty tuple ?**

Use `()` -> Creates a empty tuple

---

# Packed Values

> Packed values are **values that are bundled together in some way**

- Tuples, lists are obvious
- Strings are considered a packed value (because they are a bundle of characters)
- Sets and dictionaries are also packed values.

**In fact, any iterable can be considered a packed value**

## Unpacking Packed Values

> Unpacking is the act of splitting packed values into individual variables
> contained ina list or tuple.

```python

a,b,c = 'str'
print(a, b, c)

```

In above example, we **unpacked the characters of the string
into a tuple of 3 variables**O

take another example:

```python

a, b, c = [1,2,3]


```

Another example:

```python

a, b, c = 10, 20, 'hello'

```

> NOTE: DOES THIS PROCESS OF UNPACKING REMIND YOU OF SOMETHING ?
> Observe that the unpacking of the individual variables is based on
> the **relative positions** of each element.

> **This is exactly how positional arguments are assigned to parameters in a function.**


### Quick note on unpacking Sets and Dictionaries

```python

d = {'key1': 1, 'key2': 2, 'key3': 3}

a, b, c = d
print(a,b,c)

```

**When unpacking sets and dictionaries, the KEYS are unpacked, not the values.**

Also, note that sets are unordered collections (dict used to be unordered, but after 
v3.7 all dicts are ordered by default).
Hence, when dealing with unordered collections, you CAN NOT depend on the order
of unpacking.

**INTERESTING READ** : [[tuple_unpacking_and_passByObjectReference]]

---

