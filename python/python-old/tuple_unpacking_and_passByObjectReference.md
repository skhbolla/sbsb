---
title: Tuple Unpacking and Pass-By-Object-Reference
description: Tuple Unpacking and Pass-By-Object-Reference
date: 2025-09-04
updated: 2025-09-04
tags: ["python", "tuples"]
draft: true
---


# Python Under the Hood: Tuple Unpacking and Pass-by-Object-Reference

When writing Python, you’ll often stumble on little quirks that look magical at first glance:

```python
x, y = y, x   # clean swap!

```

or the way functions behave differently depending on whether you pass a list or an integer:

```python
def mutate(lst):
    lst.append(42)

a = [1, 2]
mutate(a)
print(a)   # [1, 2, 42]  (changed!)

def reassign(x):
    x += 1

b = 5
reassign(b)
print(b)   # 5  (unchanged!)

```

What’s going on here? Let’s break it down.

---

## 1. Tuple Unpacking in Assignment

In Python, multiple assignment like this:

```python
x, y = y, x

```

looks like some special syntax — but under the hood it’s just **tuple packing + unpacking**.

### Step-by-step

1. The right-hand side `y, x` is **packed into a tuple**:
    
    ```python
    (y, x)
    
    ```
    
2. The left-hand side `x, y` is a tuple pattern that **unpacks** the values.
    
3. Both evaluations happen before any assignment is applied, so no overwriting occurs.
    

You can think of it as:

```python
_temp = (y, x)   # tuple packing
x, y = _temp     # tuple unpacking

```

This is why the swap works — the original values are safely stored in a temporary tuple before assignments happen.

---

### Why sequential assignment fails

If you wrote:

```python
x = y
y = x

```

then the first line overwrites `x` with `y`, and by the time you hit the second line, the original value of `x` is lost. That’s why you get `(20, 20)` instead of `(20, 10)`.

Tuple unpacking avoids this problem by evaluating everything first, then assigning.

---

## 2. Python’s Pass-by-Object-Reference Model

In many languages, you’ll hear about _pass-by-value_ vs _pass-by-reference_.

Python does neither. Instead, it uses something often called **pass-by-object-reference** (or _call by sharing_).

Here’s what it means:

- When you pass a variable into a function, you’re passing the **object reference**, not the object itself.
- Inside the function, the parameter becomes a new name bound to the **same object**.
- Whether the caller “sees” a change depends on whether the object is mutable or immutable.

---

### Example with a mutable object

```python
def mutate_list(mylist):
    mylist.append(99)

nums = [1, 2, 3]
mutate_list(nums)
print(nums)  # [1, 2, 3, 99]

```

Here, `nums` and `mylist` both point to the same list object.

Mutating the list affects both.

---

### Example with an immutable object

```python
def add_one(x):
    x += 1

n = 10
add_one(n)
print(n)  # 10

```

Integers are immutable.

When you do `x += 1`, Python creates a **new int object** and rebinds `x` to it.

`n` in the caller is still pointing to the original `10`.

---

### Key takeaway

- **Mutable objects** (lists, dicts, sets, custom classes): functions can change them in place.
- **Immutable objects** (ints, strings, tuples): functions cannot change them; reassignment just rebinds the local name.

---

## 3. How They Connect

Tuple unpacking and pass-by-object-reference both highlight **how Python treats names and objects**.

- Tuple unpacking works because names (`x`, `y`) are just **labels bound to objects**. You can freely rebind them after evaluation.
- Pass-by-object-reference works because function parameters are just **new labels bound to the same objects**. Whether changes “stick” depends on object mutability.

In both cases, Python keeps the model simple: **names are references to objects**, and assignment just rebinds names.

---

## 4. Practical Tips

- Use tuple unpacking (`a, b = b, a`) for safe swaps or parallel assignments. It’s clean, Pythonic, and avoids overwrite bugs.
- Be mindful of mutability when passing objects to functions:
    - If you want to avoid side effects, pass a copy (`mylist[:]` or `copy.deepcopy`).
    - If you want side effects, rely on the mutability of the object.
- Remember: assignment in Python never copies data; it only binds names to objects.

---

### Final Thought

The magic disappears once you realize the core rule:

> Variables in Python are just names pointing to objects. Assignment only rebinds the name.

From swapping variables with tuple unpacking to understanding why your list mutated inside a function — it all follows from this one principle.

---

Would you like me to also make this into a **visual version** (diagrams showing names → objects → mutations) so it feels more like a polished blog/tutorial?