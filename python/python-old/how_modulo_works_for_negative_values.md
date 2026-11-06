---
title: "How % operation works for negative values" 
description: "how_modulo_works_for_negative_values"
date: 2026-07-07
updated: 2026-07-07
tags: [""]
draft: true
---


## **Python’s Modulo (%) and Floor Division (//) with Negative and Float Values**

Python handles `%` (modulo) and `//` (floor division) differently than languages like C++ or Java. This difference becomes obvious when you work with negative numbers and floating-point values.

The secret to understanding both operators lies in how Python defines **floor division** and uses it to calculate the remainder.

---

## **The Mathematical Core: It All Starts with Floor**

In Python, the floor division operator `//` yields the mathematical "floor" of the division. The floor function always rounds **down** toward negative infinity.

- **Positive example**: `5 // 2` results in `2` (since $5 / 2 = 2.5$, rounded down is `2`).
- **Negative example**: `5 // 2` results in `3` (since $-5 / 2 = -2.5$, rounded down toward negative infinity is `3`).

---

## **Deriving the Universal Modulo Equation**

The modulo operator `%` is not an independent calculation. It is strictly bound to floor division. We can derive their relationship directly from the classic mathematical **Division Algorithm**.

## **Step 1: The Fundamental Definition of Division**

In basic arithmetic, dividing a dividend ($a$) by a non-zero divisor ($b$) yields a quotient ($q$) and a remainder ($r$):$$a = (q \times b) + r$$

## **Step 2: Isolating the Remainder**

To find the equation for the remainder ($r$), rewrite the formula to isolate $r$:$$r = a - (q \times b)$$

## **Step 3: Mapping to Python Operators**

Python maps its programming syntax directly to these mathematical components:

- The Remainder ($r$) is represented by the modulo operator: `a % b`
- The Quotient ($q$) is represented by the floor division operator: `a // b`

## **Step 4: Final Substitution**

Substituting the Python operators into the isolated remainder equation gives us the universal formula:$$\mathbf{a \% b = a - (a // b) \times b}$$

Because Python defines the quotient ($q$) using **floor division**, the remainder ($r$) must adapt to keep this equation true.

---

## **Working with Negative Integers**

Plugging negative values into our derived formula explains the results that often confuse programmers.

## **Example: `5 % -2`**

1. **Calculate floor division**: `5 // -2` equals `3` (floor of `2.5`).
2. **Apply formula**: $5 - (-3 \times -2)$
3. **Simplify**: $5 - 6 = -1$
4. **Result**: `5 % -2` is `1`.

## **Example: `5 % 2`**

1. **Calculate floor division**: `5 // 2` equals `3` (floor of `2.5`).
2. **Apply formula**: $-5 - (-3 \times 2)$
3. **Simplify**: $-5 - (-6) \implies -5 + 6 = 1$
4. **Result**: `5 % 2` is `1`.

> **Golden Rule for Sign**: In Python, the result of `a % b` always takes the sign of the divisor (`b`). If you divide by a negative number, your remainder will be negative.

---

## **Working with Floating-Point Values**

Python applies this exact same derived formula to floats.

## **Example: `5.5 % 2.0`**

1. **Calculate floor division**: `5.5 // 2.0` equals `2.0` (floor of `2.75`).
2. **Apply formula**: `5.5 - (2.0 * 2.0)`
3. **Simplify**: `5.5 - 4.0 = 1.5`
4. **Result**: `5.5 % 2.0` is `1.5`.

## **Example with Negatives: `5.5 % 2.0`**

1. **Calculate floor division**: `5.5 // 2.0` equals `3.0` (floor of `2.75`).
2. **Apply formula**: `5.5 - (-3.0 * 2.0)`
3. **Simplify**: `5.5 - (-6.0) \implies -5.5 + 6.0 = 0.5`
4. **Result**: `5.5 % 2.0` is `0.5`.

---

## **Why Python Choosing Floor Matters**

Languages like C++ and Java use **truncated division** (rounding toward zero) instead of floor division. For example, in C++, `-5 / 2` truncates to `-2`.

Python’s choice to use floor division makes it incredibly useful for handling periodic cycles. For example, if you are wrapping an angle or a clock hands animation, `-30 % 360` correctly wraps around to `330`. In C++, this would return `-30`, forcing you to write extra conditional logic to fix the negative boundary.

---