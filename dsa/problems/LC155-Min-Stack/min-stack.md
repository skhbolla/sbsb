---
type: tutorial
title: LC155 - Min Stack 
shortTitle: Min Stack
difficulty: Medium
date: 2026-03-23
author: Srikanth Bolla
tags: ["stack", "min-stack"]
---

# LeetCode 155 - Min Stack 
[External Link ↗](https://leetcode.com/problems/min-stack/description/)

## Description

Design a stack that supports **push, pop, top, and retrieving the minimum element** in **constant time**.

Implement the `MinStack` class:

* `MinStack()` initializes the stack object.
* void `push(int val)` pushes the element val onto the stack.
* void `pop()` removes the element on the top of the stack.
* int `top()` gets the top element of the stack.
* int `getMin()` retrieves the minimum element in the stack.

You must implement a solution with $O(1)$ time complexity for each function.

**Constraints:**  
* `-2^31 <= val <= 2^31 - 1`
* Methods pop, top and getMin operations will always be called on non-empty stacks.
* At most `3 * 10^4` calls will be made to `push`, `pop`, `top`, and `getMin`.

**Clarifications**  

* N/A

---

## 1. Bruteforce Approach 

### Intuition

The brute force approach focuses on **Space Optimization** at the **expense of Time Complexity**. By using a single dynamic array, we maintain the LIFO (Last-In-First-Out) properties of a stack perfectly, but we treat the "minimum" value as a transient property that must be recalculated upon every request rather than a state that is tracked.

We are obviously diregarding a constraint of the problem : "*All Operations must be* $O(1)$"

### Implementation
```python

class BruteForce:
    def __init__(self):
        self.data = []

    def push(self, val: int) -> None:
        self.data.append(val)

    def pop(self) -> None:
        self.data.pop()

    def top(self) -> int:
        return self.data[-1]

    def getMin(self) -> int:
        return min(self.data)

```

### Complexity Analysis

* **Time Complexity:** 
  * `push`, `pop`, `top`: $O(1)$ (Amortized $O(1)$ for push due to dynamic array resizing).
  * `getMin`: $O(n)$ because we must perform a linear scan of the entire underlying array to find the smallest element.
* **Space Complexity:** 
  * $O(n)$ to store the elements. Note : We usually say $O(n)$ rather than $O(1)$ because the data structure itself scales with the number of inputs, but it is $O(1)$ extra space relative to a standard stack.

### Low-Level Implications: 

* **CPU Cache (In)efficiency** : 
  * While a linear scan $O(n)$ is "slow," it's actually quite fast for small $n$ because arrays are stored in *contiguous memory*. The CPU can pre-fetch the next parts of the stack into the L1/L2 cache. However, as the stack grows into the millions, getMin() will eventually force a "cache miss," requiring the CPU to wait for data to be fetched from the much slower RAM.
  * Note that Python’s memory model introduces a specific overhead:
    * **The Pointer Indirection**: In Python, a list is a contiguous array of memory addresses (pointers), not the actual integer objects. While the block of pointers is stored contiguously in a way that the CPU can easily pre-fetch, the actual integer objects are scattered throughout the private heap.
    * **The "Double Hit" Cache Miss**: To find the minimum, the CPU must first fetch the pointer from the list (likely a cache hit) and then "dereference" it to find the actual value in the heap. As the stack grows into the millions, these heap lookups increasingly result in cache misses, forcing the CPU to stall while it fetches data from the much higher-latency RAM.
  * **The Bottom Line**: Even with the benefits of contiguous pointer storage, the brute force approach eventually hits a "memory wall" where the $O(n)$ scan becomes dominated by the hardware cost of jumping around the heap to find the values those pointers represent.

---

## 2. Two Stacks Approach

### Intuition

In a standard stack, when you `pop()`, you lose the current state. If that element was the minimum, you have no way of knowing what the minimum of the remaining stack is without re-scanning everything.

The Two-Stack approach solves this by treating the "minimum" as a property that is **captured and frozen at every level** of the stack.
* **The Main Stack** stores the actual data sequence.
* **The Min Stack** stores a running record of the "minimum so far."

By pushing to **both** stacks at the same time and popping from **both** stacks at the same time, you ensure they stay perfectly in sync. The top of the Min Stack is always the answer to: "*Of all the elements currently in the Main Stack, which one is the smallest?*"

**Implementation Strategy** 
* **Main Stack**: Operates like a normal LIFO stack.
* **Min Stack**: 
  * **When pushing** $x$: Push $x$ onto the Main Stack. For the Min Stack, push either $x$ or the current top of the Min Stack-whichever is smaller.
  * **When popping**: Pop from both stacks simultaneously. This ensures the Min Stack always stays "in sync" with the current state of the Main Stack.
  * `getMin()`: Simply return the top of the Min Stack.

### Implementation
```python
class TwoStacks:

    def __init__(self):
        self.valstack = []
        self.minstack = []

    def push(self, val: int) -> None:
        if not self.valstack:
            self.valstack.append(val)
            self.minstack.append(val)
        else:
            self.valstack.append(val)
            self.minstack.append(min(val, self.minstack[-1]))
            # replacing the min() method with a simple
            # if val < m: m = val 
            # would be faster at the bytecode level. 
            #But I deliberately use min() to keep code readable.

    def pop(self) -> None:
        self.valstack.pop()
        self.minstack.pop()

    def top(self) -> int:
        return self.valstack[-1]

    def getMin(self) -> int:
        return self.minstack[-1]

```

### Complexity Analysis

* **Time Complexity:** $O(1)$ for all operations (`push`, `pop`, `top`, `getMin`).
* **Space Complexity:** $O(2 * n) \equiv O(n)$ auxiliary space. In the worst case (if the input is strictly decreasing), we are storing exactly double the data compared to the brute force.

### Low-Level Implications: 

* **Pointer Aliasing and Memory** : In Python, if you push a value that is not the new minimum, the Min Stack will just store another pointer to the same integer object that is already at the top.
  * **Explanation** : In the push method, when `val > self.minstack[-1]`; the `min()` function returns the address of the existing minimum. The minstack simply appends a new pointer to the same memory address as the previous minimum element.
  * So we are not always allocating new integer objects (which are ~28 bytes in Python). We are only allocating a new 8-byte pointer in the list's underlying array. This makes the "double stack" approach much more memory-efficient in Python than in a language like C++ where you might be storing actual copies of the data.
  * **Implication**: You aren't actually creating $2n$ integer objects in memory. You are creating $n$ integer objects and $2n$ pointers. Since pointers are significantly smaller than integer objects, the actual memory "doubling" is less than it appears on paper. 


* **Instruction Pipeline Efficiency** : The `getMin()` call changes from a Looping/Branching pattern (in Brute Force approach) to a Direct Memory Access pattern (in Two-Stack approach).
  * **Implication**: Modern CPUs use "Out-of-Order Execution". A loop with a comparison (in Brute Force) creates a "dependency chain" where the CPU has to wait for one comparison to finish before starting the next. The Two-Stack approach allows the CPU to fetch the minimum in a single cycle, keeping the execution pipeline full and fast.


* **The "Two-Step" Dereference (Cache Misses)** : Because Python lists are arrays of pointers, calling `getMin()` involves **Double Indirection**.
  * The CPU fetches the pointer at `self.minstack[-1]`.
  * The CPU then follows that pointer to the actual heap location to read the integer value.
  * **The Risk**: While the `minstack` pointer array is contiguous in memory (good for the cache), the actual integer objects are scattered in the **Private Heap**. If your stack is massive (millions of elements), jumping from the list to the heap can cause a **Cache Miss**, forcing the CPU to wait for the slower RAM


* **Allocation Overhead** : Since Python `list` objects are dynamic arrays, they occasionally need to resize.
  * **Implication**: Python lists over-allocate memory to stay $O(1)$. When `valstack` reaches its capacity, it triggers a resize (moving all pointers to a new, larger block of memory). Since you are pushing to `minstack` at the exact same frequency, both lists will likely trigger these expensive "resizes" at roughly the same time, leading to occasional latency spikes during a `push`.


* **The "Function Call" Tax** : `min(val, self.minstack[-1])`
  * **Instruction Count**: `min()` is a built-in function call. This involves pushing a new frame to the call stack, looking up the global name min, and executing the logic.
  * **Optimization**: **Replacing min() with a simple if `val < m: m = val` is technically faster at the bytecode level** because it avoids the overhead of a function call and uses the CPU's local branching logic instead.
---

## 3. One Stack (Tuple) Approach

### Intuition

Instead of maintaining a second independent stack in a separate memory region—which forces Python to manage an additional dynamic array, we consolidate the state. We bundle each value with the current minimum into a single "package" (a tuple) before pushing it. This couples the data and its metadata into an **atomic unit**, ensuring the minimum is always physically attached to the value that defined it.

**Implementation Strategy**

* `Push(x)`:
  * Retrieve the current minimum by looking at the second element of the top tuple: `stack[-1][1]`. 
  * Determine the new minimum: `current_min = min(x, stack[-1][1])`.
  * Push the pair `(x, current_min)` as a single entry.
* `Pop()`: Call `stack.pop()`. Because the value and the minimum are bundled, removing the value automatically removes the "memory" of that minimum, reverting the stack to the previous tuple's state.
* `getMin()`: Return `stack[-1][1]`.

### Implementation
```python
class OneStackTuple:
    def __init__(self):
        self.stack = []

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append((val, val))
        else:
            m = min(val, self.stack[-1][1])
            self.stack.append((val,m))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]
```

### Complexity Analysis

* **Time Complexity:** $O(1)$ for all operations
* **Space Complexity:** $O(2 * n) \equiv O(n)$ Auxiliary space. We are still storing $2n$ values, just grouped differently. (Although the RSS will be worse than Two Stacks because of each tuple having it's own object overhead. *Read more in Low Level Implications Section*).

### Low-Level Implications: 

* **Improved Spatial Locality**: In the two-stack version, the "Value" and the "Min" could be in entirely different memory pages. In the tuple version, the pointer to the value and the pointer to the min are stored in contiguous slots within the tuple object.
  * **The Hardware Win**: When the CPU loads the tuple into the cache, both pieces of information (value and min) arrive together. This minimizes the risk of a second "cache miss" when you call `getMin()` immediately after `top()`.


* **List Overhead**: By eliminating the second list object, we reduce the overhead Python incurs from managing two separate dynamic arrays (each with its own resizing logic and capacity buffers). 


* **Tuple Overhead**: While we save on "List" overhead, Python now has to manage $n$ individual "Tuple" objects on the heap. Each tuple is its own immutable object with its own header and reference count, which can be "heavier" than storing raw pointers in two separate, contiguous lists.
  * **The "Weight"**: A 2-item tuple in Python typically takes 48–60 bytes of memory. Storing $n$ tuples is often physically "heavier" on the heap than storing $2n$ pointers in two simple lists.


* **Synchronization Safety**: This approach prevents the "out-of-sync" risk. In a two-stack model, a failed push to the second stack would corrupt the data structure; here, the value and the minimum are pushed as a single, inseparable reference.

---


## 4. One Stack (Encoding) Approach

### Intuition

The "dumb" one-stack approach (tuples) is $O(n)$ space because it stores two values at every level. To get to $O(1)$ extra space, we need a way to store the "old minimum" inside the stack only when it changes, without using a second slot.

We use a mathematical formula to "encode" the current value and the previous minimum into a single number. This encoded number acts as a marker. Whenever we see a number in the stack that is smaller than our current minimum, it’s a signal that says: "*Hey, the previous minimum is hidden inside this math!*"

**Implementation Strategy**

* **Variable**: Maintain a single integer `min_val`.
  
* **Push($x$)**: 
  * If the stack is empty: Push $x$ and set `min_val = x`.
  * If `x >= min_val`: Just push $x$.
  * If `x < min_val`: Push the encoded value: `2x - min_val`. Then update `min_val = x`.
  * **Logic**: Because `x < min_val`, the value `2x - min_val` will always be less than $x$. This ensures the encoded value is always smaller than the new minimum, serving as our "flag."
  
* **Pop()**:
  * If the top value `y >= min_val`: Just pop it.
  * If `y < min_val`: This was our marker! We must restore the previous minimum before removing it: `prev_min = 2 * min_val - y`. Then pop and set `min_val = prev_min`.
  
* **getMin()**:Return the `min_val` variable.

### Implementation
```python

class MinStack:
    def __init__(self):
        self.stack = []
        self.min_val = None

    def push(self, val: int) -> None:
        if not self.stack:
            self.stack.append(val)
            self.min_val = val
        else:
            if val < self.min_val:
                # Encode the previous min into the stack
                # The pushed value will be smaller than the new min_val
                self.stack.append(2 * val - self.min_val)
                self.min_val = val
            else:
                self.stack.append(val)

    def pop(self) -> None:
        if not self.stack:
            return
        
        top = self.stack.pop()
        
        # If the popped value is less than min_val, it's a marker
        # We must restore the previous minimum
        if top < self.min_val:
            self.min_val = 2 * self.min_val - top
        
        if not self.stack:
            self.min_val = None

    def top(self) -> int:
        top = self.stack[-1]
        # If the value in the stack is a marker (smaller than min_val),
        # it means the current min_val IS the actual top value.
        return self.min_val if top < self.min_val else top

    def getMin(self) -> int:
        return self.min_val

```

### Complexity Analysis

* **Time Complexity:** $O(1)$ for all operations.
* **Space Complexity:** $O(1)$ **Auxiliary space**. We use exactly one stack and one integer variable. We have eliminated the $O(n)$ pointer/tuple overhead entirely.

### Low-Level Implications: 

* **The Integer Underflow Trap** : This is the most critical low-level risk.
  * The Math: The formula `2x - min_val` can produce a number that exceeds the limits of a standard 32-bit or 64-bit integer.
  * In Python, this is "safe" because Python integers have arbitrary precision (they grow as large as needed). However, in C++ or Java, you would need to use long (64-bit) to store int (32-bit) calculations to prevent a crash. This makes the approach less portable.

* **Arithmetic vs. Memory Latency** : In the tuple approach, push involved a memory allocation. Here, push involves a multiplication and a subtraction.
  * **The Reality**: CPU arithmetic (ALU) is orders of magnitude faster than Memory Access (RAM). By doing math instead of storing extra pointers, we are reducing the "memory footprint," which keeps the stack better localized in the CPU's L1 Cache.
  
* **Logic Branching** : The `top()` operation is no longer a simple "return the last element."
  * **The Cost**: To return the correct `top()`, you must check if `stack[-1] < min_val`. If it is, you return `min_val` (because the actual value is the current minimum, and the stack only holds the encoded "marker"). This adds a conditional branch to every read, which can slightly slow down the pipeline compared to a direct memory read.

* **Zero Pointer Overhead** : We are storing $n$ elements using $n$ pointers. There are no extra pointers, no extra stacks, and no tuple wrappers. In a system with millions of operations, this is the most memory-efficient state possible.


---

> ***Disclaimer** : This post was drafted with the assistance of AI to refine the wording and technical flow. The AI served as a writing partner to help clarify the intuition and drawbacks of these algorithms for a better reading experience.*
