---
title: "How C tracks variable names"
description: "Sortof a misleading title.. But a good read!"
date: 2025-12-20
updated: 2025-12-20
tags: ""
draft: true
---



To answer your question directly: **C does not track variable names for heap memory.**

When you use `malloc`, the block of memory you get back has **no name, no symbol table entry, and no variable identifier**. It only has a numerical **Address**.

The "variable name" you use in your code (like `ptr`) is actually just a standard stack variable that happens to hold that number.

Here is the deep dive into how C bridges the gap between named variables and anonymous heap memory.

---

### 1. The Bridge: Stack Name → Heap Address

You must visualize this as a two-step chain.

- **Step 1 (The Anchor):** You have a named variable on the **Stack** (e.g., `int *ptr`). The compiler and symbol table manage this exactly like `int a = 10`. It is just an offset (e.g., `RBP-8`).
- **Step 2 (The Link):** The _value_ stored inside `RBP-8` is the memory address of the **Heap** block.

**The Code:**

C

`int *ptr = malloc(sizeof(int)); *ptr = 99;`

**The Internals (Step-by-Step):**

1. **`malloc` executes:** The allocator finds free space on the heap (let's say at address `0x5000`) and returns that number in the register `RAX`.
2. **The Link is forged:** The CPU writes that number into the stack variable.
    - `mov [rbp-8], rax` → Now the memory at `RBP-8` holds the value `0x5000`.
3. **Accessing the Heap (`ptr = 99`):** The CPU cannot access the heap directly by name. It must "cross the bridge."
    - **Fetch:** Read the address stored at `RBP-8` into a register (e.g., `RBX`). (`RBX` becomes `0x5000`).
    - **Dereference:** Write `99` to the memory address inside `RBX`. (`mov DWORD PTR [rbx], 99`).

---

### 2. Proof of Anonymity: The Memory Leak

The best way to prove that C doesn't track heap names is to look at a memory leak.

C

`void leak() { int *ptr = malloc(4); // ptr (stack) holds address 0x5000 (heap) ptr = NULL; // ptr (stack) now holds 0x0 }`

- **What happened?** You overwrote the "bridge" on the stack.
- **The Result:** The heap memory at `0x5000` is still reserved. It still contains data. But because the heap memory itself has no name, you have **zero way** to ever access it or free it again. It is "orphaned."
- If C tracked heap names, you could say "free the memory that `ptr` _used_ to point to." But you can't.

---

### 3. How does the Heap Manager track data? (Metadata)

If heap memory has no name, how does `free(ptr)` know how many bytes to delete?

You pass a pointer to `free`, but you don't pass the size.

C

`free(ptr); // How does it know to free 4 bytes vs 4000 bytes?`

**The Secret:** The heap allocator (like `glibc`'s ptmalloc) cheats. It stores **hidden metadata** _right before_ the address it gave you.

When you call `ptr = malloc(16)`, the allocator actually reserves (for example) 24 bytes:

- **Bytes 0-7 (Header):** Contains the size of the chunk (e.g., "24") and flags (e.g., "previous chunk is free").
- **Bytes 8-23 (User Data):** This is the address returned to you (`ptr`).

**When you call `free(ptr)`:**

1. The allocator takes your address (`ptr`).
2. It subtracts 8 bytes to look at the **Header**.
3. It reads the size recorded there.
4. It knows exactly how much memory to reclaim.

### Summary for the Systems Engineer

- **Variable Names:** Only exist for Stack and Global variables (via Symbol Table/Offsets).
- **Heap Memory:** Is completely anonymous.
- **The Connection:** A named Stack variable acts as a "handle" holding the numerical address of the anonymous Heap block.
- **Management:** The System tracks heap blocks not by name, but by **hidden headers** written directly into memory adjacent to your data.

### Next Step

This hidden metadata is the source of many famous security vulnerabilities (like the "Heap Overflow"). If you write past the end of your array on the heap, you overwrite the _next_ chunk's header, confusing `free()` and potentially letting you hijack the program.

Would you like to see how a **Heap Overflow** works at the byte level?