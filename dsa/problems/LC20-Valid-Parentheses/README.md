---
type: tutorial
title: LC20 - Valid Parantheses
shortTitle: Valid Parantheses
difficulty: Easy
date: 2026-03-18
author: Srikanth Bolla
tags: ["stack"] 
---

# LeetCode 20 - Valid Parentheses 
[External Link ↗](https://leetcode.com/problems/valid-parentheses/description/)

## Description

Given a string s containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid.

An input string is valid if:

* Open brackets must be closed by the same type of brackets.
* Open brackets must be closed in the correct order.
* Every close bracket has a corresponding open bracket of the same type.



**Constraints:**  
* `1 <= s.length <= 10^4`
* s consists of parentheses only `()[]{}`.


**Clarifications**  

* N/A

---

## 1. Bruteforce Approach

### Intuition

Iterate through the string and keep removing valid pairs `() , [] , {}` . If by the end you are left with an empty string , return `True` . Otherwise return `False`.

### Implementation
```python
def bruteforce(self, s: str) -> bool:
        while '()' in s or '[]' in s or '{}' in s:
            s = s.replace('()' , '')
            s = s.replace('[]' , '')
            s = s.replace('{}' , '')
        return s == ''
```

### Complexity Analysis

* **Time Complexity:** $O(n^2)$
  * In the worst case e.g., ((((())))) , we perform $n/2$ iterations, and in each iteration, the `.replace()` scan takes $O(n)$ time.
* **Space Complexity:** $O(n^2)$ or $O(n)$ depending on the language's string immutability/handling, as new strings are created during replacement.
  * Python strings are immutable , so it creates new strings during replacement. But in the real world, the old versions of strings are garbage collected so we would never really use $n^2$ space, but the theoretical memory pressure (assumes no garbage collection at all) should still be calculated as $$(n-2) + (n-4) + (n-6) + \dots + 0 \approx \frac{n^2}{4} \approx n^2 $$


### Low-Level Implications

* **Heap Fragmentation & Allocation Pressure**: 
  * In languages like Python, Java, or C#, strings are immutable. When you run s = s.replace("()", ""), the computer doesn't just erase two characters. It allocates a brand-new memory slot for a slightly smaller string and copies the surviving characters into it.
  * As the loop runs $n/2$ times, you are creating hundreds or thousands of "temporary" strings that become "garbage" almost immediately. When the system runs out of available memory, the Garbage Collector kicks in. In many implementations, this triggers a "Stop-the-World" event:
    * The JVM or Python Runtime literally freezes all program execution.
    * It scans the memory (the Heap) to find which strings are no longer used.
    * It clears them out and often "compacts" the remaining memory to close the gaps.
    * The code sits idle during this time, leading to "stuttering" or high latency that wouldn't exist if it weren't churning through memory.
  
* **The "Scan-and-Shift" Penalty**: Every time the code calls .replace("()"), the CPU must perform a linear scan to find the substring. Once found, it doesn't just "delete" the characters; it must copy all subsequent characters into the new memory allocation to fill the gap.This results in massive Data Movement. For a string of length $n$, we are physically moving roughly $n^2/4$ characters across the data bus between the CPU and RAM.
  * To understand why so much data moves, imagine a string of 100 characters.
  * First Replace: You find () at the start. To "remove" it, you must copy the remaining 98 characters into a new memory location.
  * Second Replace: You find the next pair. You copy the remaining 96 characters into a new memory location.
  * Third Replace: You copy 94 characters...If you sum this up: $98 + 96 + 94 + ... + 0$. 
    * This is an arithmetic progression. The formula for the sum is roughly $\frac{1}{2} \times (\text{number of steps}) \times (\text{average characters moved})$.With $n/2$ steps and an average of $n/2$ characters moved per step, you get $\frac{n}{2} \times \frac{n}{2} = \frac{n^2}{4}$.
  * Even for a string of just 10,000 characters, you aren't just processing 10,000 bytes; the CPU is physically pumping millions of bytes across the Data Bus (the "highway" between the CPU and RAM) just to perform simple deletions.
  
* **Cache Inefficiency (Temporal & Spatial)**: Since each .replace() creates a new string in a different part of the RAM, the CPU cannot rely on its Cache (the ultra-fast memory located inside the CPU chip).
Normally, the CPU likes to predict that if you read address 100, you’ll probably want address 101 next (Spatial Locality). But because each iteration jumps to a new memory allocation, the CPU constantly experiences Cache Misses. It has to reach all the way out to the "slow" RAM to fetch the new string, forcing the processor to sit idle for hundreds of clock cycles while waiting for the data to arrive.

* **Instruction Branching**: The underlying implementation of string searching (like Boyer-Moore or simple naive search) involves complex branching logic. Under the hood, .replace() is a search algorithm. It uses a loop that constantly asks: "Is the current character '('? If yes, is the next one ')'?".  Modern CPUs use a Pipeline to execute multiple instructions at once, "guessing" the result of these if statements to stay fast. However, because the string's structure is constantly changing as you delete pairs, the CPU's Branch Predictor often guesses wrong. When it guesses wrong, it has to "flush the pipeline"—throwing away all the work it started and restarting from the correct branch. This makes the execution flow  inefficient.

---

## 2. Stack Approach

### Intuition

The Brute Force approach was bad because it was "**forgetful**" - it had to re-scan the entire string over and over to find matching pairs. To optimize this, we need a way to process the string in a single pass $O(n)$ while keeping track of the opening brackets we've encountered.
This is where the **Stack** comes in. 

**The "Last-In, First-Out" Rule**

When you encounter an opening bracket like `(`, you’re essentially starting a "*requirement*." That `(` must be closed by a `)` before you can finish any brackets that came before it.
Because we only care about the **most recent** open bracket, a **Stack** is the perfect tool.

* Opening Brackets: When you see `(, [, or {` , push it onto the stack. It stays there, waiting for its partner.

* Closing Brackets: When you see `), ], or }`, look at the top of the stack.
  * The Match: If the top of the stack is the correct partner (e.g., you see `]` and the top is `[` ), pop it off. That pair is now resolved.
  * The Mismatch: If the stack is empty or the top is the wrong partner (e.g., you see `)` but the top is `{` ), the string is invalid.
  
* The Finish Line: If the stack is empty after you've read the whole string, every bracket found its partner. If not, something was left hanging which would mean the string is not valid.

### Implementation
```python

def counterpart(self, x):
        if x == ')' : return '('
        elif x == '}' : return '{'
        elif x == ']' : return '['
        else : sys.exit()

def stack_approach(self, s: str) -> bool:
        stack = []

        for i in s:
            if i == '(' or i == '{' or i == '[':
                stack.append(i)
            else:
                if stack == []:
                    return False
                
                cp = self.counterpart(i) 
                #Function call here instead of simple if else 
                #conditions is admittedly worse for performance , 
                #but the code looks cleaner
                popped = stack.pop()
                if cp != popped:
                    return False
        return stack == []

## See solution.py for a more pythonic implementation of the same approach

```

### Complexity Analysis

* **Time Complexity:** $O(n)$ - Single pass over the string. Push and Pop both take $O(1)$ time.
* **Space Complexity:** $O(n)$ - In the worst case (eg : `((((((`) we hold all n characters of string in the stack.

### Low-Level Implications

* **Cache Locality**: A stack is usually just an array under the hood. When the CPU fetches the "top" of the stack, it grabs a whole chunk of memory (a Cache Line) and puts it in the **L1 Cache**. Since we are always working at the very end of that array, the data we need is almost always sitting right there in the fastest memory possible. No jumping around the RAM.

* **Zero String "Churn"**: We aren't creating new strings or copying memory. We allocate the stack once. If the stack needs more room, it grows, but it doesn't leave "trash" behind for the Garbage Collector to clean up. This prevents those "*Stop-the-World*" pauses where the system freezes to reclaim memory.

* **Linear Hardware Prefetching**: Modern CPUs are smart - they see you moving through the string character by character. The Hardware Prefetcher starts loading the next characters into the cache before you even ask for them. This keeps the CPU "fed" with data, avoiding stalls.

---

## Comparison Table

| Approach       | Time Complexity | Space Complexity | Low Level Implication(s)                                                           |
| -------------- | --------------- | ---------------- | ---------------------------------------------------------------------------------- |
| **Bruteforce** | $O(n^2)$        | $O(n)$           | High memory churn and GC usage; Cache Inefficiency; Instruction Branching Failures. |
| **Stack**      | $O(n)$          | $O(n)$           | Cache Locality; No memory Churn; Great Hardware Prefetcher Performance.                               |


---

> ***Disclaimer** : This post was drafted with the assistance of AI to refine the wording and technical flow. The AI served as a writing partner to help clarify the intuition and drawbacks of these algorithms for a better reading experience.*
