---
title: "Slice Behaviour" 
description: "slicing_behavior"
date: 2026-07-09
updated: 2026-07-09
tags: [""]
draft: true
---

When you use a slice like `l[0:3]`, Python always does the exact same first step: it creates a `slice(0, 3, None)` object. This object contains nothing but three numbers: start, stop, and step.

The split in behavior happens entirely based on whether you are **reading** or **assigning**.

## **1. The Reading Mechanics (`x = l[0:3]`)**

When Python sees you are reading, it passes that `slice` object to the list's internal lookup method (`__getitem__`).

1. The list looks at the numbers `0` and `3`.
2. The list requests a brand-new block of memory for a new list container.
3. The list copies the memory addresses of the items at indices 0, 1, and 2 into that new container.
4. It returns that new list to you.

## **2. The Assignment Mechanics (`l[0:3] = 'ab'`)**

When Python sees an equals sign, it routes the operation to a completely different internal method (`__setitem__`). The `slice` object is used purely as a set of coordinate instructions.

1. The list looks at the numbers `0` and `3` to locate the target index range.
2. It evaluates the right-hand side (`'ab'`) and extracts its individual elements (`'a'` and `'b'`).
3. It deletes the elements currently sitting in positions 0, 1, and 2 of the original list array.
4. It shifts any remaining elements in the list (like elements at index 3 or higher) to make precise room for the new data.
5. It writes the memory addresses of `'a'` and `'b'` directly into those empty slots inside the original list array.

## **Summary**

> The slice itself never changes into a list or a window. It is always just a passive set of index coordinates. The **list structure handles** reading by allocating new memory, and handles assignment by executing an in-place array manipulation at the coordinates provided.

<aside>  
💡

**Extended slices** (like `l[::2] = 'ab'`) require an exact length match, whereas standard slices do not. Continue reading to find out why?

</aside>

An extended slice is a slice that includes a **third argument**: the **step** (or stride). [1, 2]

While a regular slice looks like `l[start:stop]`, an extended slice looks like `l[start:stop:step]`.

Internally, this changes the slicing mechanics because the indices are no longer contiguous.

---

## **1. Syntax to Internal Object**

When you use a second colon, Python populates the third field of the `slice` object:

- `l[0:6:2]` becomes `slice(0, 6, 2)`.
- This tells the list to look at indices `0`, `2`, and `4` (skipping every second element). [3, 4]

---

## **2. Reading Mechanics**

When reading (`x = l[0:6:2]`), the list allocates a new list container and copies the items from those non-contiguous positions.

A common example of an extended slice is reversing a list: `l[::-1]`. This sets the step to `-1`, telling the internal loop to walk backward through the entire array indices and copy them into a new list. [5, 6]

---

## **3. Assignment Mechanics (The Strict Rule)**

When assigning to an extended slice (e.g., `l[0:6:2] = 'abc'`), CPython enforces a strict rule: **The number of items on the right-hand side must exactly match the number of slots being replaced.**

Because the targeted indices are scattered (non-contiguous), Python cannot shift a solid block of memory to grow or shrink the list. It can only do direct replacements. [7]

## **Example of a Success**

```python
l = [10,20,30,40,50,60]# Targets 3 specific indices: 0, 2, and 4
l[0:6:2] = ['a','b','c']

print(l)# Output: ['a', 20, 'b', 40, 'c', 60]# Indices 0, 2, and 4 were overwritten in place.
```

## **Example of a Failure**

```python
l = [10,20,30,40,50,60]# Targets 3 indices, but provides only 2 items
l[0:6:2] = ['a','b']# Raises: ValueError: attempt to assign sequence of size 2 to extended slice of size 3
```

---

## **Summary**

An extended slice just adds a **step** parameter to the `slice` coordinate object. For reading, it collects items at intervals. For writing, it acts as a precise mask targeting specific, non-contiguous memory slots, which is why the replacement data must fit the target slots perfectly.

If you are interested, we can look at how **negative steps** alter the boundary rules for `start` and `stop` indices, or how **omitting** indices entirely defaults the slice object's properties. Which direction should we go? [8, 9, 10]