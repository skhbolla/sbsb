---
type: tutorial
title: LC167 - Two Sum II - Input Array Is Sorted
shortTitle: Two sum II - Sorted Array
difficulty: Medium
date: 2026-03-08
author: Srikanth Bolla
tags: ["binary-search", "hashmap", "two-pointers"]
---

# LeetCode 167 - Two Sum II Input Array Is Sorted
[LeetCode Link ↗](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/)

## Description

Given a **1-indexed** array of integers numbers that is already sorted in non-decreasing order, find two numbers such that they add up to a specific target number. Let these two numbers be `numbers[index1]` and `numbers[index2]` where `1 <= index1 < index2 <= numbers.length`.

Return the indices of the two numbers `index1` and `index2`, each incremented by one, as an integer array `[index1, index2]` of length 2.

The tests are generated such that there is exactly one solution. **You may not use the same element twice**.


**Constraints:**  
* You must use $O(1)$ extra space.
* `2 <= numbers.length <= 3 * 104`
* `-1000 <= numbers[i] <= 1000`
* numbers is sorted in non-decreasing order.
* `-1000 <= target <= 1000`
* The tests are generated such that there is exactly one solution.


**Clarifications**  

* N/A

---

## 1. Bruteforce Approach

### Intuition

For each element at index `i`, we scan the remainder of the array (`j = i+1 to n`) to find if `nums[j] + nums[i] == target`. This approach ignores the sorted nature of the input and checks every possible combination.

> We run `j` from `i+1 to n` instead of `0 to n` because order of `i, j` do not matter. `nums[i] + nums[j]`  is same as `nums[j] + nums[i]`

### Implementation
```python
def bruteforce(self, numbers: List[int], target: int) -> List[int]:
        '''
        Ignore the ordering , try every possible pair
        Time Complexity - O(n ^ 2)
        Space Complexity - O(1)
        '''
        for i in range(0,len(numbers)):
            for j in range(i+1, len(numbers)):
                if numbers[i] + numbers[j] == target:
                    return [i+1, j+1]
```

### Complexity Analysis

* **Time Complexity:** $O(n^2)$ — Nested loops check roughly $n^2/2$ pairs.
* **Space Complexity:** $O(1)$ — No extra data structures used.

### Low-Level Implications: 

---

## 2. Hashmap Approach - Two Passes

### Intuition

We trade space for time. By pre-calculating a "lookup table," we can find the complement of any number in $O(1)$ time rather than scanning the array.

### Implementation
```python
# see solution.py for implementation
```

### Complexity Analysis

* **Time Complexity:** $O(n)$ — Two linear passes. The inner loop is $O(1)$ due to the "Exactly One Solution" guarantee.
* **Space Complexity:** $O(n)$ — The `lookup` dictionary stores all $n$ indices.

### Low-Level Implications: 

---

## 3. Hashmap Approach - Single Pass

### Intuition

we already know that the ordering does not matter. So why bother precomputing a lookup, just for the ability to do forward lookups..? 
Instead of pre-building the map, we check for the complement in the "already visited" items. This allows us to find the pair in a single traversal.

### Implementation
```python
def hashmap_one_pass(self, numbers: List[int], target: int) -> List[int]:
        lookup = {}
        for idx, val in enumerate(numbers):
            complement = target - val
            if complement in lookup:
                # Note: No loop is needed over lookup[complement] because:
                # 1. 'One solution' guarantee: If val != complement, 
                #complement appears only once (Guarenteed by the question).
                # 2. Implementation logic: If val == complement, we return the first index 
                #    (already in lookup) and the current index before the second one is ever 
                #    added to the map. Thus, lookup[complement] always has exactly one element.
                return [lookup[complement][0]+1, idx+1]
            if val not in lookup:
                lookup[val] = [idx]
            else:
                lookup[val].append(idx)
```

### Complexity Analysis

* **Time Complexity:** $O(n)$ — Single linear pass.
* **Space Complexity:** $O(n)$ — The `lookup` dictionary stores all $n$ indices.

### Low-Level Implications: 

---


## 4. Binary Search Approach

### Intuition

We take advantage of the **non-descending order**. For every element `x`, we know exactly what `y` ($target - x$) we need. Instead of a linear scan, we perform a Binary Search on the right side of the current element.

### Implementation
```python
def binary_search(self, numbers: List[int], target: int) -> List[int]:
        '''
        Since we know that the array is already in non-descending order..
        For a given value at index i , calculate complement as target - val
        and perform binary search over array[i+1] to array[n]

        This reduces our quadratic time search to a logarithmic search.

        Time complexity - O(n log n)
        Space complexity - O(1)
        '''

        for i in range(len(numbers)):
            l, r = i + 1, len(numbers) - 1
            tmp = target - numbers[i]
            while l <= r:
                mid = l + (r - l)//2
                if numbers[mid] == tmp:
                    return [i + 1, mid + 1]
                elif numbers[mid] < tmp:
                    l = mid + 1
                else:
                    r = mid - 1
```

### Complexity Analysis

* **Time Complexity:** $O(n \log n)$ — We perform a $\log n$ search for each of the $n$ elements.
* **Space Complexity:** $O(1)$ — Only a few pointers are stored.

### Low-Level Implications: 

---

## 5. Two Pointers

### Intuition

Since the array is sorted, we can use two pointers at the boundaries. If the sum is too large, we decrease the right pointer to find a smaller value. If the sum is too small, we increase the left pointer.

Place one pointer at the start (`left`) and one at the end (`right`).

* If `sum > target`: The only way to decrease the sum is to move the `right` pointer inward.
* If `sum < target`: The only way to increase the sum is to move the `left` pointer inward.

### Implementation

```python
def two_pointers(self, numbers: List[int], target: int) -> List[int]:
        l = 0
        r = len(numbers) - 1
        while(True):
            if numbers[l] + numbers[r] == target:
                return [l+1, r+1]
            elif numbers[l] + numbers[r] > target:
                r = r-1
            else:
                l = l+1
            #Note that we are not writing any break statements
            #inside the infinite while loop. This is usually very unsafe
            #but the question guarentees a solution exists. So the loop 
            #will break out through the return statement

```

### Low-Level Implications: Exploiting Spatial Locality

* **Predictable Branching:** In a sorted or semi-predictable distribution, the `if/else` checks become highly predictable for the CPU's **Branch Predictor**, minimizing pipeline flushes.
* **Sequential Access:** Unlike Binary Search (which jumps), Two Pointers move linearly, by doing this we maximize **Spatial Locality**. The CPU pre-loads the next chunks of the array into the L1 cache before the code even requests them.

---

## Comparison Table

| Approach          | Time Complexity | Space Complexity | Best Feature(s)               | Low Level Implication(s) |
| ----------------- | --------------- | ---------------- | ----------------------------- | ------------------------ |
| **Bruteforce**    | $O(n^2)$        | $O(1)$          | Simple to implement           | -                        |
| **Hashmap**       | $O(n)$          | $O(n)$           | Works on unsorted arrays      | -                        |
| **Binary Search** | $O(n \log n)$   | $O(1)$           | Better than $O(n^2)$          | -                        |
| **Two Pointers**  | $O(n)$          | $O(1)$           | **Optimal** for sorted arrays | -                        |


---

## TLDR

* **Two Pointers** is the gold standard here because it meets the $O(1)$ space constraint while running in linear time.
* **Binary Search** is a solid fallback if you want to emphasize the sorted property without using pointers.
* **Hashmaps** are great for Two Sum I, but the space overhead $O(n)$ is unnecessary when the array is already sorted.


---

## Pattern Labeling

* **Pattern:** Converging Pointers / Collision Pointers.
* **Trigger:** Sorted Input + Searching for a pair that satisfies a sum.
* **Systems Analogy:** This mirrors **Sliding Window** or **Two-Way Merge** logic, where we prune the search space linearly from both ends.

---

> ***Disclaimer** : This post was drafted with the assistance of AI to refine the wording and technical flow. The AI served as a writing partner to help clarify the intuition and drawbacks of these algorithms for a better reading experience.*
