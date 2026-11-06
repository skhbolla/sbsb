---
type: "problem" 
title: LC42 - Trapping Rain Water
shortTitle: Trapping Rain Water
difficulty: "Hard"
date: 2026-03-12
author: Srikanth Bolla
tags: ["two-pointers"]
---

# LeetCode 42 - Trapping Rain Water 
[External Link ↗](https://leetcode.com/problems/trapping-rain-water/description/)

## Description

Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.

Example :
* Input: `height = [0,1,0,2,1,0,1,3,2,1,2,1]`
* Output: `6`

**Constraints:**  
* `n == height.length`
* `1 <= n <= 2 * 10^4`
* `0 <= height[i] <= 10^5`


**Clarifications**  

* N/A

### Raw chain of thought:

1. Start with a bruteforce , at every index i , we check 0 to i-1 for the left max ; and i+1 to n for right max. We then use `min` of left and right max to calculate water at the index.

2. We realize that since we move from left to right , we can just keep a **running left max** as we progress. This will cut down the operation count from bruteforce by half, but asymptotic complexity remains same.

3. We realize that we were able to keep a running left max because we move from the left to right (i.e we have the power of retrospection) , unfortunately same cannot be said for right max since we dont have the ability to look forward without scanning the array. So what if we instead move from right to left to pre-compute a right max array (we basically arrived at a suffix max array approach here). It is very important to realize and explain that we could have just as easily created a left max prefix array too.. but doing so will be a waste of both time and space since we could easily maintain a running left max.

4. Here we realize something that lets us move to the final optimal approach [YOUR THOUGHTS ON THIS]


---

## 1. Bruteforce Approach

### Intuition

The amount of water at any index i is strictly governed by its surroundings. Specifically, you need to find the tallest bar to your left and the tallest bar to your right. The water level is capped by the shorter of these two peaks.

In a brute force mindset, we just scan. For every index i, we run a loop from 0 to i-1 to find max_left, and another loop from i+1 to n-1 to find max_right.


### Implementation
```python

```

### Complexity Analysis

* **Time Complexity:** $O(n^2)$ - For every element, we perform a linear scan of the rest of the array.
* **Space Complexity:** $O(1)$ - We aren't storing anything besides a few variables.

### Low-Level Implications: 

From a systems perspective, this is brutal. You're hitting the same memory locations over and over in nested loops, which is a massive waste of clock cycles. Even if the data is in cache, the instruction overhead for $n^2$ comparisons is significant.

---

## 2. Running Left Max - The Power of Retrospection

### Intuition

Notice that in our brute force, as we move from left to right, we are constantly re-scanning the same elements to find the max_left.

But we have the power of retrospection. If we’re already moving from left to right, we can just keep a single variable running_left_max and update it as we go. This cuts our work in half. We no longer need a loop for the left side—we just "remember" what we've seen. Unfortunately, this doesn't change the $O(n^2)$ complexity because we still have to scan the entire right side for every index.

### Implementation
```python
# see solution.py for implementation
```

### Complexity Analysis

* **Time Complexity:** $O(n^2)$ - Asymptotically the same, even if we cut the actual operations by roughly half.
* **Space Complexity:** $O(1)$ - Still no extra memory used.

### Low-Level Implications: 

---

## 3. Suffix Max: Pre-computing the Future

### Intuition

We handled the left side with a running variable because we were moving in that direction. We can't do that for the right side because we can't see the future without scanning.

So, what if we move from right to left first? By doing a pre-computation pass from the end of the array to the start, we can build a suffix_max array. This "freezes" the future.

Now, when we do our main pass, we have:

1. `running_left_max` (updated on the fly).
2. `suffix_max[i]` (pulled from our pre-computed array).

**Note**: We could have made a `prefix_max` array too, but that’s a waste of time and space. Since we’re already iterating forward, a single variable does the exact same job for free.

### Implementation
```python
# see solution.py for implementation
```

### Complexity Analysis

* **Time Complexity:** $O(n)$ - One pass to build the suffix array, one pass to calculate water.
* **Space Complexity:** $O(n)$ - We are now paying a memory tax to store the suffix array

### Low-Level Implications:

You've traded memory for speed. You're now allocating $N$ integers on the heap or stack. While this is $O(n)$, you're now introducing potential cache misses if the array is large enough to exceed your cache tiers.

---

## 4. Two Pointers: The Bottleneck Realization

### Intuition

The only reason we used that $O(n)$ suffix array was because we were afraid of the "unknown" on the right. But let's look at the bottleneck.

If we have a left pointer and a right pointer, and we see height[left] < height[right], we know something critical: the water at left is limited by its left_max. We don't need to know the actual right_max because we already have a "guarantee" (the bar at the right pointer) that a wall exists which is at least as tall as our current left side. (This means water trapped at left pointer won't spill out since a taller guarantee building exists).

By processing the shorter side and moving that pointer inward, we can track both left_max and right_max on the fly. We've effectively merged the forward and backward passes into one, eliminating the need for any extra arrays.

### Implementation
```python
# see solution.py for implementation
```

### Complexity Analysis

* **Time Complexity:** $O(n)$ - A single, clean pass from both ends.
* **Space Complexity:** $O(1)$ - We've dropped the suffix array entirely.

### Low-Level Implications:

This is the optimal engineering solution. No heap allocation, minimal register usage, and it's extremely friendly to the CPU prefetcher because the memory access pattern is strictly linear from both ends inward

---

## Comparison Table

| Approach               | Time Complexity | Space Complexity | Logic                                                  | Low Level Implication(s) |
| ---------------------- | --------------- | ---------------- | ------------------------------------------------------ | ------------------------ |
| **Bruteforce**         | $O(n^2)$        | $O(1)$           | Scan everything every time.                            | -                        |
| **Retrospective Scan** | $O(n^2)$        | $O(1)$           | Use a running max variable for left, still scan right. | -                        |
| **Suffix Max Array**   | $O(n)$          | $O(n)$           | Pre-compute the right side.                            | -                        |
| **Two Pointers**       | $O(n)$          | $O(1)$           | Move the shorter side inward.                          | -                        |


---

## TLDR

* Bruteforce is dumb and slow.
* Retrospection makes the left side "free" but the right side still hurts.
* Suffix Array fixes the right side but costs memory.
* Two Pointers realizes that the taller wall acts as a guarantee, so we only need to track the bottleneck.
  
---

## Pattern Labeling

N/A
---

> ***Disclaimer** : This post was drafted with the assistance of AI to refine the wording and technical flow. The AI served as a writing partner to help clarify the intuition and drawbacks of these algorithms for a better reading experience.*
