---
title: "Why generic pointers even exist in C" 
description: generic_pointers_in_C
date: 2025-12-21
updated: 2025-12-21
tags: ""
draft: true
---

C does not allow assignments between pointers of different types. For example if we have a int *iptr , char *sptr ; the compiler will not allow assignments between iptr and sptr. This is exactly why we need generic pointers (void *) to bypass the C type system here.

This behavior of bypassing C’s type system for void pointers lets us implement “Generic logic” (polymorphism)

To understand why C even enforces type checking on pointer assignments.. read more:

Here are the **three physical reasons** why C forbids implicit pointer mixing.

---

### 1. The "Grab Size" Mismatch (What you suspected)

If you treat a `char*` (1 byte) as an `int*` (4 bytes), the CPU will read garbage.

**The Scenario:**

- You have a string `"A"` (ASCII 65). In memory: `0x41 0x00 ...`
- You force an `int*` to point to it.
- You dereference `iptr`.

The Consequence:

The CPU doesn't just read the 0x41. It blindly grabs 4 bytes (including 3 bytes of whatever random trash is next to your character) and combines them into a massive, nonsensical integer. You haven't just read the wrong data; you've read memory you don't own.

### 2. Alignment (The Hardware Crash)

This is the **"Systems Engineer" reason** that most high-level programmers don't know.

Hardware is picky. Most CPUs (especially ARM and RISC-V) require that types be stored at specific addresses.

- **Integers (4 bytes):** Must sit at addresses divisible by 4 (e.g., `0x1000`, `0x1004`).
- **Chars (1 byte):** Can sit anywhere (e.g., `0x1001`, `0x1002`).

The Crash:

If you have a char *c pointing to address 0x1001 (valid for char), and you assign it to int *i:

`char *c = (char *)0x1001; int *i = (int *)c; // BAD! *i = 5; // CRASH!`

On many CPUs, trying to write a 4-byte integer to address `0x1001` triggers a hardware exception called a **Bus Error (SIGBUS)**. The hardware literally cannot wire the bytes correctly if they aren't aligned.

### 3. Pointer Arithmetic (The Stride)

As we discussed, `ptr + 1` is multiplied by the type size.

If you cast an `int*` to a `char*`:

- **Original:** `iptr + 1` jumps 4 bytes.
- **New:** `sptr + 1` jumps 1 byte.

If you intended to iterate through an array of integers but accidentally used a char pointer, your loop will visit the _insides_ of the integers (the individual bytes) rather than the integers themselves.

### Summary

1. **Interpretation:** You will read too many or too few bytes.
2. **Arithmetic:** Your loops will break (`+1` stride changes).
3. **Alignment:** You might physically crash the CPU bus by accessing an odd address as a word.

This is why `void *` exists—it is a "Generic Pointer" that allows assignment but **forbids** dereferencing or arithmetic until you cast it back to a specific type, ensuring you confirm "I know what size and alignment this is."