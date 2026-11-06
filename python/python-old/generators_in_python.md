---
title: "Generators in Python" 
description: "The Complete Guide to Generators in Python"
date: 2025-09-04
updated: 2025-09-04
tags: [""]
draft: true
---

---

# 🌀 Generators in Python: The Complete Guide to Keywords, Expressions, and Features

When you write a comprehension in Python using square brackets `[]`, you get a **list**. But when you wrap it in parentheses `()`, you don’t get a tuple — you get a **generator**.

That little design choice opens the door to one of Python’s most elegant and powerful features: **lazy iteration with generators**.

In this post, we’ll cover:

- Why `( )` produces a generator instead of a tuple
- The keywords tied to generator behavior
- Generator expressions and object methods
- Built-in functions and modules that play well with generators
- **Practical examples of generator functions and how iteration actually works under the hood**

---

## 📦 Why Do Parentheses Create a Generator?

Python supports several comprehension syntaxes:

```python
[x for x in iterable]        # list
{x for x in iterable}        # set
{k: v for k, v in iterable}  # dict
(x for x in iterable)        # generator

```

Notice what’s missing? **Tuples.**

There’s no tuple comprehension in Python. If you want a tuple, you wrap the generator in `tuple()`:

```python
t = tuple(x*x for x in range(5))
print(t)  # (0, 1, 4, 9, 16)

```

This was a deliberate design decision. Instead of making `( )` just another eager container, Python gave it a special role: **a lazy generator expression**.

---

## 🔑 Keywords That Power Generators

Generators exist thanks to a few small but mighty keywords:

1. **`yield`**
    
    Turns a function into a generator function. Each `yield` pauses execution and returns a value.
    
    ```python
    def counter(n):
        for i in range(n):
            yield i
    
    g = counter(3)
    print(next(g))  # 0
    print(next(g))  # 1
    print(next(g))  # 2
    # next(g) now raises StopIteration
    
    ```
    
2. **`yield from`** (PEP 380)
    
    Delegates part of a generator to another generator or iterable.
    
    ```python
    def nested():
        yield from range(3)
    
    print(list(nested()))  # [0, 1, 2]
    
    ```
    
3. **`async` + `yield`**
    
    Introduce **asynchronous generators** (PEP 525).
    
    ```python
    async def agen():
        for i in range(3):
            yield i
    
    ```
    
4. **`await`**
    
    Used with async generators to pause execution until a value is available.
    

---

## 🌀 Generator Expressions

Generator expressions look a lot like list comprehensions, but wrapped in parentheses:

```python
g = (x*x for x in range(5))
print(next(g))  # 0
print(next(g))  # 1

```

They return a **generator object** — a lazy iterator you can consume one element at a time.

---

## ⚙️ Controlling a Generator Manually

Generators are not black boxes — you can interact with them:

### Basic iteration

```python
def squares(n):
    for i in range(n):
        yield i * i

g = squares(3)
print(next(g))  # 0
print(next(g))  # 1
print(next(g))  # 4

```

### Sending values back in

```python
def echo():
    received = None
    while True:
        received = yield received
        print(f"Generator got: {received}")

g = echo()
print(next(g))       # start generator → None
print(g.send("Hi"))  # resume and send "Hi"
print(g.send("Bye")) # resume and send "Bye"

```

### Throwing exceptions

```python
def simple():
    try:
        yield 1
        yield 2
    except ValueError:
        yield "Error handled"

g = simple()
print(next(g))         # 1
print(g.throw(ValueError))  # "Error handled"

```

---

## 🛑 How Iteration Really Works: `StopIteration`

Every generator implements the **iterator protocol**:

- It has a `__next__()` method.
- Each `yield` produces a value.
- When there are no more `yield`s, the generator raises **`StopIteration`**.

Example:

```python
def tiny():
    yield "A"
    yield "B"

g = tiny()
print(next(g))  # "A"
print(next(g))  # "B"
print(next(g))  # raises StopIteration

```

That’s exactly how `for` loops and functions like `list()` work internally:

```python
print(list(tiny()))  # ["A", "B"]

```

👉 Behind the scenes, `list()` just keeps calling `next(g)` until it sees a `StopIteration`. At that point, it stops.

---

## 📦 Built-in Functions & Friends of Generators

Generators integrate deeply with Python’s ecosystem. Some friends:

- **Built-ins**: `iter()`, `next()`, `sum()`, `all()`, `any()`, `max()`, `min()`
- **The `itertools` module**: advanced generator helpers like `count`, `cycle`, `chain`, etc.
- **Context managers**: `contextlib.contextmanager` uses generators under the hood.

Because they’re just iterators, generators play nicely with everything that consumes an iterable.

---

## 🧩 Putting It All Together

Here’s the landscape of generators in Python:

- **Keywords**: `yield`, `yield from`, `async`, `await`
- **Expressions**: `(expr for item in iterable)` → generator expressions
- **Methods**: `next()`, `.send()`, `.throw()`, `.close()`
- **Built-ins**: `iter`, `sum`, `all`, `itertools`, `contextlib`, etc.
- **Protocol**: Generators stop when they raise `StopIteration`

---

## ✅ Final Thoughts

Generators are one of the most Pythonic tools for writing **clean, memory-efficient, and elegant code**.

Instead of building massive lists or sets in memory, you can just **generate values on demand** and pass them through Python’s iterable ecosystem.

So the next time you catch yourself writing `[expr for x in iterable]`, ask:

➡️ Do I need the whole list right now? Or could I make it a generator instead?

---

Would you like me to also add a **section comparing generators vs iterators** (i.e., what makes a generator a special kind of iterator), or should I keep it focused just on generators?