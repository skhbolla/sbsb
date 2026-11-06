---
title: "Why are pointers indexable ??" 
description: "c_pointers_are_indexable"
date: 2025-12-21
updated: 2025-12-21
tags: [""]
draft: true
---

**The Question:** We know that `int a[10]` creates a block of memory, and `int *p` just creates a variable holding an address. Yet, C allows us to use the exact same syntax—`a[2]` and `p[2]`—to access data. Why does C let us treat a simple pointer variable like an array?

**The Answer:** In C, **array indexing does not exist** at the machine level. The syntax `ptr[i]` is just a "human-friendly" abbreviation (syntactic sugar) that the compiler rewrite into **Pointer Arithmetic**.

---

### **1. The Secret Formula: `[]` is just Math**

When you type `ptr[2]`, the C compiler does not look for an "array object." It literally rewrites your code using this formula:

$$\text{ptr[i]} \Longleftrightarrow *(\text{ptr} + \text{i})$$

- **Step 1 (`ptr + i`):** "Take the address in `ptr` and move forward by `i` steps." (The size of the step depends on the type, e.g., 4 bytes for `int`).
- **Step 2 ():** "Dereference that new address to get the value."

**Implication:** Because `ptr[i]` is just math, you can legally write `i[ptr]`!

- `ptr[2]` $\rightarrow$ `(ptr + 2)`
- `2[ptr]` $\rightarrow$ `(2 + ptr)` (Addition is commutative!)
- _Result:_ Both work perfectly (though `2[ptr]` will get you fired from your job).

### **2. The "Array Decay" Connection**

This explains why `a[i]` works on arrays.

1. **Decay:** When you use the array name `a`, it decays into a pointer to the first element (`int *`).
2. **Rewrite:** The compiler sees `a[i]`.
3. **Math:** It converts it to `(a + i)`.

The Unifying Theory:

There is no difference between accessing an array and accessing a pointer because arrays are always accessed via pointers. The brackets [] are just a tool to make pointer arithmetic look cleaner.

### **3. Does this apply to ANY pointer?**

**Yes, with one critical exception.**

You can use `ptr[n]` on `char*`, `double*`, `struct User*`, etc.

The Exception: void *

You cannot do ptr[i] if ptr is a void *.

- **Reason:** To calculate `ptr + i`, the CPU needs to know the "Stride" (Size of the data type).
- **Void:** Has no size. The math `Address + (i * ???)` is impossible.

### **Summary**

- **`ptr[i]`** is NOT an array operation. It is a **Memory Offset** operation.
- It works on pointers because pointers hold the "Base Address," and the index provides the "Offset."
- It works on arrays because arrays **decay** into pointers to their Base Address immediately.