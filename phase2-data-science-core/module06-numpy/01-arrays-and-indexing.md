# Module 06a: NumPy Arrays & Indexing

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [Module 05 — Python Tooling & Environments](../../phase1-python-foundations/module05-tooling-environments/03-code-editors-and-vscode.md)

## 🎯 Learning Objectives
- [ ] Explain what NumPy is and why it exists
- [ ] Create arrays with `np.array`, `np.zeros`, `np.ones`, `np.arange`, and `np.linspace`
- [ ] Inspect an array's `shape`, `dtype`, `size`, and `ndim`
- [ ] Index and slice 1D and 2D arrays

---

## Module Goal

Welcome to **Phase 2: Data Science Core**! This module introduces **NumPy** (Numerical Python), the foundational library that nearly every other data science and machine learning tool in Python is built on top of. You'll learn its core data structure — the **array** — and how to create, inspect, and slice it.

## Why This Matters on the Job

Pandas DataFrames, scikit-learn models, and PyTorch/TensorFlow tensors are all built directly on top of NumPy arrays, or use the exact same mental model. Every single module from here through the end of this course assumes fluency with NumPy arrays — this is the true starting line of "data science," where Phase 1's general-purpose Python becomes the specialized, numeric toolkit used in the field every day.

---

## What Is NumPy, and Why Does It Exist?

Plain Python `list`s are flexible but slow for numeric work, because each element can be *any* type, and Python has to check each one individually during operations. **NumPy** provides the `ndarray` ("n-dimensional array") — a fixed-type, contiguous block of memory that lets Python perform math on entire arrays at once, implemented in fast, compiled C code underneath.

💡 **Analogy:** A Python `list` is like a row of differently-shaped, differently-labeled boxes — flexible, but you have to open and check each one individually. A NumPy array is like a row of identical, uniform bins — because every bin is guaranteed the same size and type, you can process the whole row at once, dramatically faster.

## Installing NumPy

```bash
pip install numpy
```

## Creating Arrays

```python
import numpy as np

# From a Python list
arr = np.array([1, 2, 3, 4, 5])
print(arr)             # [1 2 3 4 5]
print(type(arr))         # <class 'numpy.ndarray'>

# From a list of lists -> a 2D array (matrix)
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix)
```
```
[[1 2 3]
 [4 5 6]]
```

**How it works:** `np.array(...)` converts an existing Python list (or list of lists) into a NumPy array. Every element in a NumPy array shares the same data type — passing `[1, 2, 3]` gives you an array of integers; mixing in a `float` like `[1, 2, 3.5]` upgrades the *entire* array to floats, since every element must share one type.

### Built-in Array Creation Functions

You often don't start from existing data — you need a placeholder array of a certain size and shape:

```python
np.zeros(5)              # array([0., 0., 0., 0., 0.])           -- 5 zeros
np.ones((2, 3))            # 2 rows x 3 columns, all 1.0
np.arange(0, 10, 2)           # array([0, 2, 4, 6, 8])              -- like range(), but returns an array
np.linspace(0, 1, 5)             # array([0., 0.25, 0.5, 0.75, 1.])   -- 5 evenly spaced points from 0 to 1
np.eye(3)                           # 3x3 identity matrix (1s on the diagonal, 0s elsewhere)
```

| Function | Purpose |
|---|---|
| `np.zeros(shape)` | Array of all zeros |
| `np.ones(shape)` | Array of all ones |
| `np.arange(start, stop, step)` | Evenly spaced values by **step size** (like `range()`) |
| `np.linspace(start, stop, num)` | Evenly spaced values by **count** — specify how many points, not the step |
| `np.eye(n)` | `n x n` identity matrix |

💡 **Tip:** Use `np.arange` when you know the *step size* you want (e.g., every 2nd number). Use `np.linspace` when you know how *many* evenly-spaced points you want (e.g., exactly 100 points between 0 and 1) — this distinction trips people up constantly, and both come up often when generating data for plots (Module 09).

## Inspecting an Array

```python
arr = np.array([[1, 2, 3], [4, 5, 6]])

print(arr.shape)     # (2, 3) -- 2 rows, 3 columns
print(arr.ndim)         # 2 -- number of dimensions
print(arr.size)           # 6 -- total number of elements
print(arr.dtype)            # int64 (or int32 on some systems) -- the data type of every element
```

**How it works:** `.shape` is a tuple describing the array's dimensions — critical to check whenever something isn't working as expected, since a huge fraction of NumPy/Pandas bugs come down to a mismatched shape. `.dtype` tells you the underlying data type (`int64`, `float64`, `bool`, etc.) — every element shares it.

⚠️ **Warning:** `.shape` is an *attribute* (no parentheses), not a method — `arr.shape` is correct, `arr.shape()` raises a `TypeError`. This trips up beginners coming from calling everything else as a function/method.

## Indexing and Slicing

### 1D Arrays — Just Like Python Lists

```python
arr = np.array([10, 20, 30, 40, 50])

print(arr[0])          # 10
print(arr[-1])           # 50
print(arr[1:3])            # [20 30]  -- same slicing rules as Python lists (Module 01)
```

### 2D Arrays — Row, Column

```python
matrix = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

print(matrix[0])            # [1 2 3]         -- entire first row
print(matrix[0, 0])            # 1                 -- row 0, column 0
print(matrix[1, 2])              # 6                   -- row 1, column 2
print(matrix[:, 0])                 # [1 4 7]               -- ALL rows, column 0
print(matrix[0, :])                    # [1 2 3]                 -- row 0, ALL columns
print(matrix[0:2, 1:3])                   # [[2 3], [5 6]]             -- rows 0-1, columns 1-2
```

**How it works:** `matrix[row, column]` — the comma separates the row index/slice from the column index/slice. `:` alone means "every index along this dimension." This comma-separated syntax (`arr[rows, columns]`) is the single most important NumPy indexing pattern to internalize — you'll use it constantly, including in Pandas (`.iloc[]`) later.

⚠️ **Warning:** A NumPy array slice (unlike slicing a Python list) is a **view**, not a copy — modifying a slice modifies the original array too!

```python
arr = np.array([1, 2, 3, 4, 5])
sub = arr[1:3]
sub[0] = 999
print(arr)   # [1 999 3 4 5]  <- the original changed!
```

✅ **Best Practice:** If you need an independent copy, call `.copy()` explicitly: `sub = arr[1:3].copy()`. This "slices are views" behavior exists for performance (avoiding unnecessary copying of large arrays) but is a very common source of subtle bugs if you're not aware of it.

---

## Hands-On Exercise

**Task:** Write `array_basics.py` that:
1. Creates a 1D array of the numbers 1 through 10 using `np.arange`.
2. Prints its `shape`, `dtype`, and the slice containing only the even-indexed elements (`[0, 2, 4, ...]`).
3. Creates a 3x3 array of zeros, then uses indexing to set the entire middle row to `[7, 8, 9]`.
4. Creates a 4x4 array using `np.arange(16).reshape(4, 4)` (reshape is covered in the next lesson — just use it here), and prints the sub-array containing only its 2x2 top-left corner.

<details>
<summary>✅ Click to see the solution</summary>

```python
import numpy as np

numbers = np.arange(1, 11)
print(numbers.shape)       # (10,)
print(numbers.dtype)         # int64 (or int32, depending on platform)
print(numbers[::2])            # [1 3 5 7 9]  -- every other element, starting at index 0

grid = np.zeros((3, 3))
grid[1] = [7, 8, 9]
print(grid)

big_grid = np.arange(16).reshape(4, 4)
print(big_grid[0:2, 0:2])
```

**Expected output:**
```
(10,)
int64
[1 3 5 7 9]
[[0. 0. 0.]
 [7. 8. 9.]
 [0. 0. 0.]]
[[0 1]
 [4 5]]
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Calling `.shape()` with parentheses | It's an attribute, not a method — `arr.shape`, no `()` |
| Assuming a slice is an independent copy | NumPy slices are views — use `.copy()` if you need independence |
| Confusing `np.arange` (step-based) with `np.linspace` (count-based) | `arange(start, stop, step)` vs. `linspace(start, stop, num_points)` |
| Mixing types in a list before converting (`[1, 2, "3"]`) | Keep source data uniformly typed, or NumPy will upcast the whole array (often to strings!) |
| Forgetting the comma in 2D indexing (`matrix[0][0]` works but `matrix[0, 0]` is the idiomatic NumPy way) | Prefer `matrix[row, col]` — faster and the standard NumPy convention |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand why NumPy exists and how it differs from plain Python lists
- [ ] Can create arrays with `np.array`, `np.zeros`, `np.ones`, `np.arange`, `np.linspace`
- [ ] Can inspect `shape`, `dtype`, `size`, `ndim`
- [ ] Can index and slice both 1D and 2D arrays
- [ ] Understand that slices are views, not copies
- [ ] Completed the `array_basics.py` exercise

**Next:** Continue to [`02-vectorization-and-broadcasting.md`](02-vectorization-and-broadcasting.md)
