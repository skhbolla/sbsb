---
title: "Python equality" 
description: "equality_in_python"
date: 2026-02-23
updated: 2026-02-23
tags: [""]
draft: true
---


# Understanding Equality in Python: `==`, `is`, `id()`, and the Object Model

If you truly understand how Python evaluates equality, you unlock clarity around:

- Why `a == b` behaves differently from `a is b`
- Why two identical lists aren’t the same object
- Why `id()` sometimes looks like a memory address
- Why overriding `__eq__` can break dictionaries
- Why small integers sometimes behave strangely

This guide walks through everything — from high-level concepts to CPython internals.

---

# 1. Two Types of Equality in Python

Python supports **two completely different notions of equality**:

|Concept|Operator|Meaning|
|---|---|---|
|Value equality|`==`|Are the values equal?|
|Identity equality|`is`|Are they the same object in memory?|

These are fundamentally different operations.

---

# 2. What Happens When You Use `==`?

When you write:

```python
a == b
```

Python translates this to:

```python
a.__eq__(b)
```

More precisely:

1. Call `type(a).__eq__(a, b)`
2. If that returns `NotImplemented`, try `type(b).__eq__(b, a)`
3. If still `NotImplemented`, fall back to identity comparison

So:

> `==` compares values, not memory addresses.

Unless a class does not override `__eq__`, in which case it defaults to identity comparison.

---

# 3. Built-in Types and Value Equality

Different built-in types implement `__eq__` differently.

## Integers

```python
a = 5
b = 5

a == b  # True
a is b  # Often True (small int caching)
```

`int.__eq__` compares numeric values.

---

## Lists

```python
a = [1, 2]
b = [1, 2]

a == b  # True
a is b  # False
```

`list.__eq__` compares elements recursively.

Even though values match, they are different objects in memory.

---

## Dictionaries

```python
d1 = {"a": 1}
d2 = {"a": 1}

d1 == d2  # True
d1 is d2  # False
```

Dictionary equality compares:

- Keys
- Corresponding values

It does NOT compare memory addresses.

---

# 4. What Does `is` Actually Do?

`is` checks **object identity**.

When you write:

```python
a is b
```

Python checks:

```python
id(a) == id(b)
```

It verifies whether both variables point to the same object in memory.

---

# 5. What Does `id()` Do?

```python
id(obj)
```

Returns a unique identifier for the object during its lifetime.

In **CPython**, this identifier is:

> The memory address of the object.

Example:

```python
a = [1, 2]
b = a

id(a) == id(b)  # True
```

Both variables reference the same object.

Important:

- `id()` uniqueness is guaranteed only during the object’s lifetime.
- After an object is destroyed, its memory may be reused.

---

# 6. The Python Object Model (CPython Internals)

In CPython, every object:

- Lives on the heap
- Has a reference count
- Has a pointer to its type

Conceptually:

```
Variables → references → heap objects
```

When you do:

```python
x = 10
```

This means:

```
x → pointer → int object(10)
```

Variables do NOT store values.

They store references to objects.

---

# 7. Default Equality Behavior

If a class does NOT implement `__eq__`, Python falls back to identity comparison.

Example:

```python
class A:
    pass

a = A()
b = A()

a == b  # False
```

Why?

Because default `object.__eq__` behaves like:

```python
def __eq__(self, other):
    return self is other
```

So default equality = identity.

---

# 8. Small Integer Caching (Why `is` Sometimes "Works")

CPython caches small integers from -5 to 256.

Example:

```python
a = 256
b = 256
a is b  # True

a = 1000
b = 1000
a is b  # Usually False
```

The first case works due to integer caching.

This is an implementation detail.

Never use `is` for value comparison.

---

# 9. Recursive Equality

For compound objects like:

- Lists
- Tuples
- Dicts

Equality is recursive.

Example:

```python
[1, [2, 3]] == [1, [2, 3]]
```

Python:

1. Compares outer lists
2. Compares first elements
3. Compares inner lists recursively

This is why equality remains intuitive even for nested structures.

---

# 10. Important: Mutability Is Irrelevant to Equality

Mutability affects whether an object can change.

It does NOT affect how equality is computed.

Example:

```python
(1, 2) == (1, 2)  # True
[1, 2] == [1, 2]  # True
```

One is immutable, one mutable — equality rules remain the same.

---

# 11. How `==` Interacts With `__hash__`

Very important rule:

> If two objects compare equal (`__eq__`), they MUST have the same hash.

If you override `__eq__` but not `__hash__`, Python disables hashing.

Example:

```python
class A:
    def __eq__(self, other):
        return True

a = A()
hash(a)  # TypeError
```

Why?

Because inconsistent hashing would break:

- dict
- set

Python enforces correctness by setting `__hash__ = None`.

---

# 12. Equality vs Identity — Summary

|Expression|Meaning|
|---|---|
|`a == b`|Call `__eq__`, compare values|
|`a is b`|Compare memory identity|
|`id(a)`|Unique identity (memory address in CPython)|

Mental model:

```
== → Ask the object: “Are your values equal?”
is → Ask Python: “Are these the same object?”
```

---

# 13. When Should You Use Each?

### Use `==`:

- Value comparisons
- Strings
- Lists
- Dicts
- Numbers

### Use `is`:

- Checking for `None`
- Checking sentinel objects
- Verifying identity semantics

Example:

```python
if x is None:
    ...
```

Never do:

```python
if x == None:
```

---

# 14. Performance Perspective

`is`:

- Extremely fast
- Just pointer comparison

`==`:

- Calls type-specific logic
- May recurse
- May involve hash lookups
- May call user-defined methods

For primitives, it’s still very fast.

---

# 15. Final Mental Model (The Core Truth)

Python variables:

- Do not contain values.
- They reference objects.

Equality:

- Is defined by the object’s `__eq__`.
- Is value-based for built-ins.
- Defaults to identity for custom classes.

Identity:

- Is about memory.
- Uses pointer comparison.
- Backed by `id()` in CPython.

---

# Closing Insight

Understanding equality deeply helps you:

- Write correct `__eq__` implementations
- Avoid subtle dict/set bugs
- Debug confusing identity behavior
- Understand Python at a systems level

---

If you’d like next, we can turn this into:

- A deeper post on `__hash__` and dictionary internals
- A CPython memory layout deep dive
- A “How dict equality works in C” breakdown
- Or a full object lifecycle & reference counting article

You’re asking the right questions — this is how you move from “Python user” to “Python engineer.”