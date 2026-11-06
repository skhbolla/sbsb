---
type: tutorial
title: LC11 - Container With Most Water
shortTitle: Container With Most Water
difficulty: Medium
date: 2026-03-11
author: Srikanth Bolla
tags: ["two-pointers", "l1-l2-Cache"] 
---

# LeetCode 11 - Container With Most Water 
[External Link ↗](https://leetcode.com/problems/container-with-most-water/description/)

## Description

You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `ith` line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

*Return the maximum amount of water a container can store.*

**Notice** that you may not slant the container.


**Constraints:**  
* `n == height.length`
* `2 <= n <= 10^5`
* `0 <= height[i] <= 10^4`


**Clarifications**  

* N/A

---

## 1. Bruteforce Approach

### Intuition

Since the goal is to find the maximum volume of water trapped between any two vertical lines, the most direct method is to simulate every possible container configuration and calculate its volume.
The brute force approach is essentially **Exhaustive Search**.

* **Selection**: We use two nested loops to pick every possible pair of lines $(i, j)$.
  
* **Constraint**: We ensure we don't compare a line with itself by starting the inner loop at $i + 1$
  
* **Calculation**: For every pair, the volume is defined by the "bottleneck" (the shorter of the two lines) and the distance between them. (`(j-i) * min(height[i], height[j])`)
  
* **Verification**: we maintain a running `max_water` variable, updating it only when a newly calculated volume exceeds our current record.

### Implementation
```python
def bruteforce(self, height: List[int]) -> int:
        '''
        The most naive way of solving this is by calculating
        the water stored by all possible containers and returning the
        maximum possible water.
        '''
        n = len(height)
        max_water = 0
        for i in range(0, n):
            for j in range(i+1, n):
                contained_water = (j-i) * min(height[i], height[j])
                max_water = max(max_water, contained_water)
        return max_water
```

### Complexity Analysis

* **Time Complexity:** $O(n^2)$
  * **Two nested loops**: The total number of pairs is $\frac{n(n-1)}{2}$, which asymptotically simplifies to $O(n^2)$.
  * **Min/Max/Arithmetic**: These are all $O(1)$ operations performed within the inner loop.
  * For $n = 10^5$, this results in $\approx 5 \times 10^9$ operations, which typically triggers a Time Limit Exceeded (TLE) error.
  
* **Space Complexity:** $O(1)$
  * We only use a fixed number of integer variables (`n`, `max_water`, `i`, `j`, `contained_water`) to track the state.
  * No extra data structures are created that grow with the input size.

### Low-Level Implications: 

* **Quadratic Instruction Scaling**: With two nested loops, the CPU instruction count explodes. For every single increment of the outer loop, the inner loop must scan the remaining tail of the array.

---

## 2. Two Pointers

### Intuition

Think of this like a trade-off. To get the most water, you need a container that is **both wide and tall**.

We start with the **widest possible container** (one pointer at the very left, one at the very right `l = 0` , `r = len(height) - 1`). After recording this initial area, we face a single, logical question:

> [!IMPORTANT] 
> ***Is there a container that is less wide than this one, but potentially tall enough to beat our current record?***

#### The Movement Logic 

The area of any container is strictly governed by its shorter side. This is our bottleneck.

* **The Realization**: Since we are already at the maximum possible width for our current shorter side, we have effectively "exhausted" its potential. It is mathematically impossible to find another container using this specific side that has a larger area, because any other container would be less-wider (narrower).

* **The Strategic Move**: We move the shorter side inward. By doing this, we are "throwing away" a line whose best performance we've already recorded. Moving the taller line never helps because it keeps the height the same but reduces the width.

* **The Goal**: We sacrifice width specifically to hunt for a taller height. We hope that by moving past the current bottleneck, we will encounter a much taller line that can compensate for the shrinking width and set a new maximum area.

### Implementation

```python
def two_pointers(self, height: List[int]) -> int:

        '''
        Start with the widest container and move inward, 
        trading width for the potential of finding more height.
        '''
 
        l = 0
        r = len(height)-1
        max_water = 0

        while(l < r):
            # 1. Record the area of the current widest possible container for these two sides
            contained_water = (r-l) * min(height[l], height[r])
            max_water = max(max_water, contained_water)

            #2. Try a narrower container in hopes of finding 
            # a height taller than our current bottleneck 
            if height[l] < height[r]:
                l = l + 1
            else:
            #Note: This else block includes the case where heights are equal.
                r = r - 1

        return max_water
```

### Complexity Analysis

* **Time Complexity:** $O(n)$
  * We visit each element once. By eliminating one "bottleneck" per step, we collapse a quadratic problem into a linear one.
  
* **Space Complexity:** $O(1)$
  * No extra storage is needed. We just track the `max_water` and the two pointer positions.


### Low-Level Implications

* **Instruction Pruning**: By using this logic, we skip $O(n^2)$ unnecessary area calculations. Instead of forcing the CPU to multiply and compare every possible pair, we use a single if/else condition to "prune" thousands of impossible candidates at every step

* **Streamlined Logic**: The CPU's branch predictor quickly learns the "move the shorter one" pattern, allowing the loop to execute at near-peak hardware speeds.
  
* **Cache Efficiency**: The pointers move inward in a predictable fashion. This allows the CPU's prefetcher to load the `height` values into the L1 cache before the code even needs them, resulting in near-instantaneous comparisons.

---

## Comparison Table

| Approach         | Time Complexity | Space Complexity | Best Feature(s)   | Low Level Implication(s)                             |
| ---------------- | --------------- | ---------------- | ----------------- | ---------------------------------------------------- |
| **Bruteforce**   | $O(n^2)$        | $O(1)$           | Easy to implement | Quadratic instructions                               |
| **Two Pointers** | $O(n)$          | $O(1)$           | Extremely fast    | Better Branch Prediction, pre-fetching data to cache |


---

## TLDR

* **Bruteforce** is $O(n^2)$ because we exhaust all possible containers
* **Two Pointers** $O(n)$ cleverly utilizes the fact that the smaller side of a container is the bottleneck. So move it inward in hopes of finding a side taller than the current bottleneck.


---

## Pattern Labeling

N/A

---

> ***Disclaimer** : This post was drafted with the assistance of AI to refine the wording and technical flow. The AI served as a writing partner to help clarify the intuition and drawbacks of these algorithms for a better reading experience.*
