---
title: "Maximum Value Of Expression - Manhattan Distance"
description: "Maximum Manhattan Distance"
date: 2026-02-02
last_reviewed: 2026-02-02 
difficulty: "easy"
status: "solved"

tags: ["array", "manhattan-distance", "bounding-box", "linear-scan", "absolute-terms", "L1 Norm / Coordinate Rotation"]

draft: true
type: "problem"
---

# Maximum Value Of Expression for a given Array

## 1. Deconstruct the Problem

**The Core 'Why':** We are given an array where we want to maximize .
**Theoretical Foundation:** This is the **Manhattan Distance** ( Norm) between two points in a 2D plane where the points are defined as .
**Physics Parallel:** Imagine a city grid where you can only move North-South or East-West. The problem asks for the two "buildings" in the city that are furthest apart given you must follow the streets.

---

## 2. Brute Force

The most obvious path is to check every possible pair  and calculate the distance.

* **Time:** 
* **Space:** 
* **The Bottleneck:** We are treating the distance as a **Relationship**. To calculate the value for , we are forced to wait until we pick a . This "coupling" locks us into nested loops.

---

## 3. The 'Bottleneck' Analysis

Why is  slow? Because of the **Absolute Value Bars** . In programming, `abs()` is a hidden `if-else` block. These conditional gates prevent us from using algebra to separate the  terms from the  terms. As long as they are "trapped" inside the bars, the variables are coupled.

---

## 4. The Smallest Step Forward

**Observation:** Distance is symmetric (). If we only look at the "right-hand side" of every point (where ), we don't lose any data, but we **linearize** the horizontal term.
If , then  becomes , which simplifies to .
**New Expression:** .

---

## 5. Iterative Refinement

1. **Branching:** To remove the last absolute value , we must consider two algebraic realities: building  is either taller than or shorter than building .
2. **Decoupling:** * **Case A ():** 
* **Case B ():** 


3. **The "Bridge":** We've turned a **Relationship** into a **Property**. Every index now has two independent "scores":  and .

---

## 6. Chain of Thought

The logic moves from **Searching** (comparing pairs) to **Tracking** (finding the boundaries of a shape).
Mathematically, we are performing a **45-degree Coordinate Rotation**:



By finding the `max` and `min` of these rotated coordinates, we are finding the **Manhattan Bounding Box**—the tilted square that encloses all our points. The maximum distance must be the largest "spread" (Max - Min) along one of these two diagonal axes.

---

## 7. Final Optimal State

### Python Implementation

```python

def optimal(self, arr : list[int]) -> int:
        n = len(arr)

        if(n < 2):
            # The constraints specify that size will never be 0,
            # But it can be 1
            # I've chosen to handle both cases either way
            return 0

        maxf1 = maxf2 = arr[0] - 0
        minf1 = minf2 = arr[0] + 0

        for x in range(0, n):
            f1 = arr[x] - x
            f2 = arr[x] + x

            if f1 > maxf1 : maxf1 = f1
            if f1 < minf1 : minf1 = f1
            if f2 > maxf2 : maxf2 = f2
            if f2 < minf2 : minf2 = f2

        return max( (maxf1 - minf1) , (maxf2 - minf2) )

```

---

## 8. Takeaways

> [!IMPORTANT]
> **Summary of the Journey:**
> 1. We identified the **Manhattan Metric** in a 2D point cloud.
> 2. We identified the **Bottleneck**: Absolute values couple  and  into .
> 3. We applied **Case Expansion** to decouple the variables.
> 4. We reduced the problem to finding the **Range** (Max - Min) of independent properties.
> 5. **Low-Level Insight:** This linear scan is  and extremely **cache-friendly** because it processes the array sequentially, allowing the CPU to utilize prefetching and avoid branch mispredictions.
> 6. **Additional Insight**: Bounding Box

---

## 🔗 Links & Resources


