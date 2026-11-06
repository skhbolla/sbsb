---
title: "How does free() know how big the block was?"
description: "Learn the underlying mechanics of the allocator"
date: 2025-12-20
updated: 2025-12-20
tags: ""
draft: true
---



# how does free() know how big the block was? (The "Metadata" secret).

---

This is the ultimate "Systems Engineer" secret.

You know how you call `malloc(32)` and get a pointer, and then later you just call `free(ptr)` without telling it "32"?

The Secret: The allocator lied to you.

When you asked for 32 bytes, it actually grabbed (for example) 40 bytes from the OS. It used the extra 8 bytes to write a secret note to itself right before the address it gave you.

This secret note is called the **Chunk Header** (or Metadata).

---

### 1. The "Hidden Header" Layout

Imagine memory as a long tape. You ask for space for an integer array.

**Your Code:**

C

`char *ptr = malloc(16);`

The Physical RAM (The Lie):

The allocator finds a free spot. Let's say at address 0x5000.

It does not give you 0x5000. It writes the size at 0x5000 and gives you 0x5008.

**The Layout:**

- **Address `0x5000` (Hidden):** `[ SIZE: 16 | IS_FREE: 0 ]` (This is the Header)
- **Address `0x5008` (Returned to You):** `[ Your Data Starts Here... ]`
- **Address `0x5018`:** `[ Next Chunk's Header... ]`

To you, `ptr` is `0x5008`. You think your memory starts there. You have no idea that 8 bytes behind you, the system is storing critical bookkeeping data.

---

### 2. How `free(ptr)` Works

When you hand that pointer back to `free`:

C

`free(ptr); // ptr is 0x5008`

The `free` function performs a simple pointer subtraction trick:

1. **Rewind:** It calculates `Metadata_Address = ptr - sizeof(Header)`.
    - `0x5008 - 8 = 0x5000`.
2. **Read:** It looks at address `0x5000`.
3. **Decode:** It reads the number stored there ("16").
4. **Reclaim:** It now knows exactly how many bytes to mark as "Available" in its internal list.

**The Internal Logic (Pseudocode):**

C

`void free(void _ptr) {  
// 1. Step back to find the hidden tag  
ChunkHeader _header = (ChunkHeader_)((char_)ptr - 8);

```
// 2. Read the size
int size = header->size; 

// 3. Mark that entire block (header + size) as free
AddToFreeList(header, size);
```

}`

---

### 3. The "Systems" Danger: Heap Corruption

This design is efficient, but it creates one of the most dangerous vulnerabilities in software history: **Heap Overflow**.

If you write **past** the end of your array, you don't just crash. You overwrite the _next_ chunk's header.

**The Scenario:**

1. You have `ptr1` (16 bytes) and `ptr2` (16 bytes) sitting next to each other in memory.
2. You accidentally write 24 bytes into `ptr1`.
3. You blow past `ptr1`'s space and overwrite the **Header of `ptr2`**.
4. You change `ptr2`'s size from "16" to "10,000" (or some garbage number).

The Explosion:

When you later call free(ptr2), the allocator looks at the corrupted header.

- "Oh, this block is 10,000 bytes long? Okay, I'll mark 10,000 bytes as free."
- It effectively deletes valid data used by other parts of your program.
- **Result:** Impossible-to-debug crashes, or worse, a hacker controls the "size" variable to trick the OS into giving them shell access.

### Summary

- **`malloc`** allocates `Requested_Size + Header_Size`.
- **`ptr`** points to the payload, jumping over the header.
- **`free`** looks backwards (`ptr - offset`) to find the size.
- **Heap Corruption** happens when you overwrite these hidden headers.

### Next Step

This "Hidden Header" mechanism is just half the battle. When you `free()` a block, it doesn't disappear; it goes onto a **Free List** (a recycling bin).

Allocators use incredible tricks to manage these lists efficiently.

Would you like to see how the Free List works? (Hint: When a block is free, the allocator uses the inside of your old data to store pointers to the next free block—it cannibalizes your dead variables!).