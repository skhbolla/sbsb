---
title: Curious Stuff in Python
description: Some things I find interesting in Python
date: 2026-07-13
updated: 2026-07-13
tags:
draft: true
---

# Global small integer caching

## **Deep Dive: Why `a = 500` and `b = 500` Might Share the Same ID in Python**

If you have ever tested object IDs in Python, you might have noticed a strange quirk. For small numbers, two variables always share the same memory location. For larger numbers, they sometimes share an ID, and sometimes they do not.

Here is a complete breakdown of how Python optimizes integer memory under the hood, and why running a script gives you completely different results than typing it line-by-line into a terminal.

---
## **The Code: Expectation vs. Reality**

Let's look at two blocks of code and see how Python actually handles them.

```python
# --- BLOCK 1: Small Integers ---a =1b =1

print(id(a) == id(b))# ALWAYS outputs: True
```

**Why this happens:** This is **Global Small Integer Caching**. When Python starts up, it automatically creates and loads an array of integer objects for the range **`-5` to `256`** into memory. Because these numbers are used constantly (for loops, indices, etc.), Python passes you a reference to the existing global object instead of wasting memory creating a new one.

```python
# --- BLOCK 2: Larger Integers ---x =500y =500

print(id(x) == id(y))# Interactive Terminal (REPL): False# Running as a Script (.py file): True
```

**Why this happens:** This is where the common misconception lies. Many developers assume Python does _no_ optimization outside the `-5` to `256` range. However, Python uses a secondary optimization technique called **Code Object Constant Folding** (or block-level optimization).

---

## **Understanding the Two Optimizations**

To understand why the output changes based on _how_ you run your code, you have to look at Python's two distinct caching mechanisms:

## **1. Small Integer Cache (Global Scope)**

- **The Range:** `[-5, 256]`
- **How it works:** These objects are hardcoded singletons created at startup. No matter where, when, or how you assign a variable to `1`, it will always point to that exact same pre-allocated memory address.
- **Immutability:** Because integers are immutable, if you later change `b = 2`, the variable `b` simply breaks its link to `1` and points to the pre-existing `2` object. Variable `a` remains safely pointed at `1`.

## **2. Constant Folding (Local Block Scope)**

- **The Range:** Any identical immutable literal (large integers, floats, strings).
- **How it works:** When Python compiles a complete block of code (like an entire `.py` file, a module, or a single function), the compiler analyzes the code before running it. If it notices that the identical constant `500` is used multiple times within that single code block, it creates **just one** integer object in the block's internal constants array (`co_consts`). Both `x` and `y` are then pointed to this single local object to save memory.

---

## **Why the Interactive Terminal (REPL) Lies to You**

When you type code line-by-line directly into a standard Python terminal prompt, **each individual line is treated as its own completely isolated code block**.

1. You type `x = 500` $\rightarrow$ Python compiles this line, creates a new object for 500, and executes it.
2. You type `y = 500` $\rightarrow$ Python compiles this new line blindly, has no memory of the previous compilation context, creates a _second_ object for 500, and executes it.

Because they were compiled at separate times, they get separate IDs. However, if you paste those exact same lines into a script file and run it, the compiler sees both lines simultaneously, triggers constant folding, and assigns them the **same ID**.

---

## **Cheat Sheet Summary**

| Integer Value           | Line-by-Line Terminal (REPL)   | Inside a Script (`.py` file) | Optimization Mechanism             |
| ----------------------- | ------------------------------ | ---------------------------- | ---------------------------------- |
| **`-5` to `256`**       | 🟩 **Same ID** (`True`)        | 🟩 **Same ID** (`True`)      | **Global Integer Cache**           |
| **Outside `[-5, 256]`** | 🟥 **Different IDs** (`False`) | 🟩 **Same ID** (`True`)      | **Constant Folding (Block Scope)** |

---

If you'd like, I can show you how to use Python's built-in **`dis` (disassembler) module** to peek into the compiler's bytecode and **see the hidden constants array** yourself. Would you like to check that out?

# Short Circuited Evaluation

Short-circuited evaluation : When using ‘and’ and ‘or’ boolean operators, we dont necessarily have to caluculate both operands to complete the operation.. For example ‘a and b’ will return false if a is false, irrespective of what b is.. so python is smart enough to short circuit this operation by not evaluating b at all if a is false… Similarly for or , if a is true , the operation short circuits to true irrespective of b

## **Understanding Short-Circuit Evaluation in Python**

Short-circuit evaluation is a smart efficiency feature built into Python's logical operators. It allows Python to skip running parts of your code when the final outcome of an expression is already guaranteed.

---

## **The Core Concept**

When evaluating expressions containing `and` or `or`, Python reads from left to right. As soon as it has enough information to determine the final truth value, it stops executing the rest of the expression immediately.

```python
# Setup variables to demonstrate a potential crash condition
numerator = 12
denominator = 0

# MAIN THEME: Short-circuiting stops evaluation at the first condition
# 1. Python evaluates: (denominator != 0) -> This is False.
# 2. Because of 'and', the whole expression must now be False.
# 3. Python short-circuits: It completely ignores the division on the right which would otherwise cause zero division error.
is_valid_ratio = (denominator != 0) and (numerator / denominator > 1)

print(is_valid_ratio)  # Outputs: False (and zero errors!)
```

---

## **How the Two Operators Short-Circuit**

## **1. The `and` Operator (The False Breakout)**

- An `and` expression requires **all** parts to be `True`.
- If Python encounters a single `False`, the whole expression is ruined.
- **Short-Circuit Action**: The moment a `False` value is found, Python halts and ignores everything to the right. [10, 11, 12, 13]

## **2. The `or` Operator (The True Breakout)**

- An `or` expression only requires **one** part to be `True`.
- If Python encounters a single `True`, the success of the expression is locked in.
- **Short-Circuit Action**: The moment a `True` value is found, Python halts and ignores everything to the right. [14, 15, 16]

---

## **Intent and Benefits of this Behavior**

- **Inline Guarding**: It lets you place a safety check (like checking for `None`, empty lists, or zeros) right next to the operation that would otherwise crash your code. [17]
- **Performance Boost**: It saves processing power by skipping heavy database queries or complex function calls if the initial conditions fail. [18]
- **Cleaner Code**: It eliminates the need for deeply nested, multi-line `if/else` blocks, keeping your scripts compact and readable. [19, 20]

# Underscores in numbers
Python allows underscores in integers and floats : 1_23_00 is a valid integer , 1_23_0.12_3 is a valid float.

# Tuples don’t need ( )

Python tuples don’t need ( ) i.e python treats ( 1, 2.0, [3,4] ) same as 1, 2.0, [3,4]

# Slices create shallow copies

Python slices create shallow copies of sequences… this could result in shared reference bugs if elements of sequence are mutable.

```python title=slices.py
# Setup the initial list with mixed types
l = [[1,2] , [3,4], 5,6]
s = l[0:3] # Slice = [[1,2] , [3,4], 5]

print("--- INITIAL STATE ---")
print(l, s)
print(id(l[0]), id(s[0])) # Same id: both point to the exact same list object [1,2]
print(id(l[1]), id(s[1])) # Same id: both point to the exact same list object [3,4]

# ---------------------------------------------------------------------
# CASE 1: MUTATION (Modifying the object inside the slot)
# ---------------------------------------------------------------------
# We go THROUGH the pointer s[0] to mutate the internal data of that inner list.
# We are NOT changing where s[0] points. We are changing what s[0] points AT.
s[0][0] = 100

print("\n--- AFTER MUTATION ---")
print(l, s) 
# Results in l = [[100,2] , [3,4], 5,6]
# Results in s = [[100,2] , [3,4], 5]
# Note: l[0] was altered too! Because s[0] and l[0] share the exact same object reference,
# modifying the contents of that object reflects everywhere.

# ---------------------------------------------------------------------
# CASE 2: REASSIGNMENT (Overwriting the pointer/slot itself)
# ---------------------------------------------------------------------
# We use a single index assignment operation. 
# This completely cuts the old connection and points the slot to a brand new object.
# Python does not care if the old object was mutable ([3,4]) or immutable (5).
s[1] = [300, 400] # Reassigning a mutable object slot
s[2] = 500        # Reassigning an immutable object slot

print("\n--- AFTER REASSIGNMENT ---")
print(l, s)
# Results in l = [[100,2] , [3,4], 5,6]
# Results in s = [[100,2] , [300,400], 500]
# Note: l did NOT change here! l[1] still points to [3,4] and l[2] still points to 5.
# Reassignment breaks the shared reference bug entirely because it replaces the label.

```


# strip methods are un-intuitive

==All Python strip methods (`strip()`, `lstrip()`, `rstrip()`) treat arguments as sets of individual characters, not as exact substrings or words==. They remove any matching character until hitting an outsider.

```python
s = 'abc_text_cba'

print(s.lstrip('abc'))  # Output: '_text_cba' (Removes left a, b, c) not the substring 'abc'
print(s.rstrip('abc'))  # Output: 'abc_text_'  (Removes right a, b, c) not the substring 'abc'
print(s.strip('abc'))   # Output: '_text_'   (Removes both sides)
```

To target an exact word or sequence without losing neighboring characters, use explicit substring methods:

```python
s = 'abc_text_cba'

print(s.removeprefix('abc'))  # Output: '_text_cba'
print(s.removesuffix('cba'))  # Output: 'abc_text_'
```