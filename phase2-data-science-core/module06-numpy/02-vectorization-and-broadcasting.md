# Module 06b: Vectorization, Broadcasting & Boolean Indexing

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [01-arrays-and-indexing.md](01-arrays-and-indexing.md)

## 🎯 Learning Objectives
- [ ] Explain vectorization and why it's dramatically faster than looping
- [ ] Perform element-wise arithmetic on arrays
- [ ] Explain and apply broadcasting rules
- [ ] Use boolean indexing (masking) to filter array data
- [ ] Use fancy indexing to select data with a list of indices

---

## Module Goal

Learn NumPy's single most important performance concept — **vectorization** — along with **broadcasting** (how arrays of different shapes combine in arithmetic) and **boolean/fancy indexing** (how to filter and select data based on conditions, not just positions). These three ideas together are *why* NumPy (and everything built on it) is fast enough for real-world data work.

## Why This Matters on the Job

"Just use a for loop" is almost always the wrong answer once you're working with NumPy arrays or Pandas DataFrames — vectorized operations aren't just more convenient, they're often 50-100x faster on real datasets, and this speed difference is the entire reason NumPy exists. Boolean indexing (`data[data > threshold]`) is also the exact same mental model you'll use constantly in Pandas to filter rows — mastering it here makes Module 07 feel immediately familiar.

---

## Vectorization: Why Looping Over Arrays Is Slow

In plain Python, doing math on every element of a list requires a loop, and Python re-checks each element's type on every single iteration:

```python
# The SLOW way -- a plain Python loop
numbers = list(range(1_000_000))
squared = []
for n in numbers:
    squared.append(n ** 2)
```

NumPy lets you apply the operation to the **entire array at once** — no explicit loop, because the looping happens inside fast, compiled C code instead of the Python interpreter:

```python
import numpy as np

numbers = np.arange(1_000_000)
squared = numbers ** 2   # the ENTIRE array squared in one operation
```

### Proving It: A Real Timing Comparison

```python
import numpy as np
import time

size = 1_000_000
python_list = list(range(size))
numpy_array = np.arange(size)

# Plain Python loop
start = time.time()
result = [x ** 2 for x in python_list]
python_time = time.time() - start

# NumPy vectorized
start = time.time()
result = numpy_array ** 2
numpy_time = time.time() - start

print(f"Python loop: {python_time:.4f} seconds")
print(f"NumPy vectorized: {numpy_time:.4f} seconds")
print(f"NumPy was {python_time / numpy_time:.0f}x faster")
```
```
Python loop: 0.0425 seconds
NumPy vectorized: 0.0067 seconds
NumPy was 6x faster
```

💡 **Tip:** Run this yourself — the exact speedup varies a lot by machine and Python version (newer Python releases have gotten faster at plain loops, narrowing the gap somewhat), but NumPy wins every time, and the gap grows the more complex the per-element operation gets or the larger the array. On older Python versions, or with more expensive operations than a simple square, it's common to see 20-50x or more. The lesson isn't a specific multiplier — it's that reaching for vectorization instead of a loop is the reliably faster default.

✅ **Best Practice:** Whenever you catch yourself writing a `for` loop over a NumPy array or Pandas column to do math, stop and ask "is there a vectorized way to do this instead?" There almost always is.

## Element-Wise Arithmetic

```python
import numpy as np

a = np.array([1, 2, 3, 4])
b = np.array([10, 20, 30, 40])

print(a + b)      # [11 22 33 44]  -- element-wise addition
print(a * b)        # [10 40 90 160]  -- element-wise multiplication
print(b / a)          # [10. 10. 10. 10.]  -- element-wise division
print(a ** 2)            # [1 4 9 16]  -- every element squared

print(a > 2)                # [False False  True  True]  -- element-wise comparison, returns a boolean array
```

**How it works:** Arithmetic operators (`+`, `-`, `*`, `/`, `**`, comparisons) apply **element-wise** by default on NumPy arrays — `a + b` adds corresponding elements together, unlike Python lists where `+` concatenates instead.

⚠️ **Warning:** `a + b` on two Python *lists* concatenates them (`[1,2] + [3,4]` gives `[1,2,3,4]`), but `a + b` on two NumPy *arrays* adds them element-wise. This is one of the most disorienting gotchas for beginners switching between lists and arrays — always be sure which type you're working with.

## Broadcasting: Combining Different Shapes

**Broadcasting** is NumPy's rule set for how arrays of *different* shapes can still be combined in arithmetic, by conceptually "stretching" the smaller one to match — without actually copying data in memory.

### The Simplest Case: Scalar + Array

```python
arr = np.array([1, 2, 3, 4])
print(arr + 10)   # [11 12 13 14] -- 10 is "broadcast" to every element
```

### 2D Array + 1D Array

```python
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
row_addition = np.array([10, 20, 30])

print(matrix + row_addition)
```
```
[[11 22 33]
 [14 25 36]
 [17 28 39]]
```

**How it works:** `row_addition` (shape `(3,)`) is conceptually stretched to match `matrix`'s shape `(3, 3)`, adding to *every row*. NumPy compares shapes from right to left: dimensions are compatible if they're equal, or if one of them is `1` (or missing entirely).

⚠️ **Warning:** Broadcasting fails with a `ValueError: operands could not be broadcast together` if shapes are genuinely incompatible (e.g., adding a shape `(3,)` array to a shape `(4, 2)` matrix) — this is one of the most common real-world NumPy/Pandas errors, and reading the error's stated shapes is the fastest way to debug it.

🎯 **On the job:** Broadcasting is why you can write `df["price"] * 1.1` in Pandas (Module 07) to apply a 10% increase to an entire column in one line, or normalize an entire dataset by subtracting its mean and dividing by its standard deviation, all without writing a single loop.

## Boolean Indexing (Masking)

Instead of selecting elements by *position*, boolean indexing selects elements by *condition* — this is one of the most useful NumPy features for real data work.

```python
scores = np.array([55, 92, 78, 40, 88, 63])

mask = scores > 60
print(mask)             # [False  True  True False  True  True]  -- a "boolean mask"

print(scores[mask])       # [92 78 88 63]  -- only elements where mask is True

# More commonly written in one line:
print(scores[scores > 60])   # [92 78 88 63]

# Combining conditions with & (and) / | (or) -- NOT Python's `and`/`or`
print(scores[(scores > 60) & (scores < 90)])   # [78 88 63]
```

**How it works:** `scores > 60` produces a boolean array the *same shape* as `scores`, with `True` wherever the condition holds. Using that boolean array as an index (`scores[mask]`) returns only the elements where the mask is `True`.

⚠️ **Warning:** You must use `&` and `|` (not Python's `and`/`or`) when combining conditions on arrays, and each condition needs its own parentheses due to operator precedence: `(scores > 60) & (scores < 90)`, not `scores > 60 & scores < 90`. Using plain `and`/`or` raises a `ValueError` about the truth value of an array being ambiguous.

## Fancy Indexing: Selecting by a List of Indices

```python
arr = np.array([10, 20, 30, 40, 50])

indices = [0, 2, 4]
print(arr[indices])   # [10 30 50]  -- selects elements at positions 0, 2, and 4

# Also works to reorder or repeat elements
print(arr[[4, 0, 0, 2]])   # [50 10 10 30]
```

**How it works:** Passing a `list` (or array) of integer positions selects exactly those elements, in exactly that order — unlike a slice, which must be contiguous and in the original order.

---

## Hands-On Exercise

**Task:** Write `vectorization_practice.py` that:
1. Creates a NumPy array of 20 random-looking test scores between 40 and 100 (use `np.array([...])` with your own numbers, or `np.random.randint(40, 101, size=20)`).
2. Uses boolean indexing to find and print all scores that count as "passing" (60 or above).
3. Uses boolean indexing to print the number of *failing* scores (below 60), using `.sum()` on a boolean mask (hint: `True` counts as 1 when summed).
4. Uses broadcasting to create a new array `curved_scores` where every score has 5 points added, without writing a loop.
5. Times how long it takes to square every element in a 500,000-element array with a plain Python loop vs. NumPy vectorization, and prints the speedup factor.

<details>
<summary>✅ Click to see the solution</summary>

```python
import numpy as np
import time

np.random.seed(42)   # makes the "random" numbers reproducible for this exercise
scores = np.random.randint(40, 101, size=20)
print(scores)

passing_scores = scores[scores >= 60]
print(f"Passing scores: {passing_scores}")

num_failing = (scores < 60).sum()
print(f"Number of failing scores: {num_failing}")

curved_scores = scores + 5
print(f"Curved scores: {curved_scores}")

size = 500_000
python_list = list(range(size))
numpy_array = np.arange(size)

start = time.time()
_ = [x ** 2 for x in python_list]
python_time = time.time() - start

start = time.time()
_ = numpy_array ** 2
numpy_time = time.time() - start

print(f"NumPy was {python_time / numpy_time:.0f}x faster")
```

**Expected outcome:** Exact scores/speedup numbers vary (random seed affects scores, machine speed affects timing), but you should see a clear list of passing scores, a failing count, curved scores each +5, and NumPy consistently faster than the loop — anywhere from several times faster to well over 50x, depending on your machine and Python version.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Writing a `for` loop to do math over an array | Use vectorized operations — check if NumPy already has a built-in way first |
| Using `and`/`or` to combine array conditions | Use `&` / `\|` with parentheses around each condition |
| Expecting `list1 + list2` and `array1 + array2` to behave the same | Lists concatenate; arrays add element-wise |
| Broadcasting shapes that don't actually align | Check shapes carefully — NumPy compares dimensions right to left |
| Confusing a boolean mask with fancy indexing (list of positions) | Masking selects by condition (same-shape `True`/`False` array); fancy indexing selects by explicit position list |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Understand vectorization and why it's faster than a Python loop
- [ ] Can perform element-wise arithmetic on arrays
- [ ] Understand broadcasting and can predict when it will/won't work
- [ ] Can filter data with boolean indexing (`arr[arr > x]`)
- [ ] Can select data by position list with fancy indexing
- [ ] Completed the `vectorization_practice.py` exercise

**Next:** Continue to [`03-aggregation-and-reshaping.md`](03-aggregation-and-reshaping.md)
