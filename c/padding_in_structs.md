---
title: "Why C adds padding to structs" 
description: "Learn how CPU forces Alignment and inserts invisible memory gaps into your data"
date: 2025-12-20
updated: 2025-12-20
tags: ""
draft: true
---

# You think a `struct { char c; int i; }` takes 5 bytes (1 + 4), right?

**Wrong.** It takes 8.  
Do you want to see how the CPU forces "Alignment" and inserts invisible memory gaps into your data?

This is one of the most fun "gotchas" in C because it exposes the physical reality of the hardware.

You are about to learn why **1 + 4 = 8**.

---

### 1. The Expectation vs. Reality

Let's look at this struct:

C

`struct MyData { char c; // 1 byte int i; // 4 bytes };`

Your Math: $1 + 4 = 5 \text{ bytes}$.

C's Math (sizeof): $8 \text{ bytes}$.

Where did the extra 3 bytes come from?

The compiler secretly injected 3 bytes of invisible "padding" (garbage space) between c and i.

### 2. The Why: The CPU is a Lazy Eater

The CPU does not read memory byte-by-byte. It grabs memory in Chunks (Words).

On a 64-bit CPU, it prefers to grab 8 bytes (or 4 bytes) at a time.

**The Golden Rule of Alignment:**

> "A 4-byte integer MUST start at an address divisible by 4."

Scenario A: Without Padding (The Disaster)

Imagine the struct was packed tight (5 bytes):

- Address `0x00`: `char c`
- Address `0x01`: `int i` (Starts here!)

If the CPU wants to read `int i`, it tries to fetch a 4-byte chunk starting at `0x00`.

- It gets: `[char c] [byte 1 of i] [byte 2 of i] [byte 3 of i]`
- **Problem:** It missed the last byte of `i`!
- **Result:** The CPU has to do **two fetches** and stitch the data together. This cuts performance in half. (On some architectures like ARM, this simply crashes the program).

Scenario B: With Padding (The Fix)

The compiler sees int i and thinks: "I need to push this to address 0x04."

- Address `0x00`: `char c`
- Address `0x01`: **Padding (Unused)**
- Address `0x02`: **Padding (Unused)**
- Address `0x03`: **Padding (Unused)**
- Address `0x04`: `int i` (Starts perfectly aligned!)

Now the CPU reads address `0x04` and gets the entire integer in **one cycle**.

### 3. The "Tetris" Optimization

This leads to a famous systems engineering puzzle: **Struct Reordering**.

Look at this horrific struct:

C

`struct Bad { char c; // 1 byte // 3 bytes PADDING int i; // 4 bytes char d; // 1 byte // 3 bytes PADDING (to align the whole struct size to 4) };`

**Total Size:** $1 + 3 + 4 + 1 + 3 = 12 \text{ bytes}$.

The Optimization:

As a systems engineer, you can manually rearrange the members to fill the holes.

C

`struct Good { int i; // 4 bytes (Starts at 0) char c; // 1 byte (Starts at 4) char d; // 1 byte (Starts at 5) // 2 bytes PADDING (To reach total size 8) };`

**Total Size:** $8 \text{ bytes}$.

You just saved 33% of your memory usage purely by moving lines of code around. This is a massive win if you have an array of 1,000,000 of these structs.

### 4. Can you turn it off? (The `packed` Attribute)

Sometimes (e.g., when reading a network packet header exactly as it came from the wire), you **must** have 1 + 4 = 5. You cannot have gaps.

You can tell the compiler to shut up and pack it:

C

`struct __attribute__((packed)) PackedData { char c; int i; };`

- **Size:** 5 bytes.
- **Cost:** Accessing `i` will be slower, and your code might crash on non-x86 CPUs.

### Summary

- **Alignment:** Data types have "natural alignment" (int=4, double=8).
- **Padding:** The compiler inserts invisible bytes to satisfy alignment.
- **Reordering:** Put largest members first (doubles, then ints, then chars) to minimize holes (this is a good rule of thumb called "Largest to Smallest").

### A Next Step for You (Whenever you are ready)

Since this was just a "fun side note," you can file this away.

When you return to your main curriculum, we are going to look at **Memory Management (`malloc`/`free`)**.

- We know `malloc` returns a pointer.
- But where does it find the memory?
- What happens if you ask for 1 GB?
- How does `free` know how big the block was? (The "Metadata" secret).

Enjoy the "God Mode" feeling. You earned it.