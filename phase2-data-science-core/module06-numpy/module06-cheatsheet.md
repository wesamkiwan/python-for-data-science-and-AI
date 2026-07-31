# 📋 Module 06 Cheat Sheet: NumPy Fundamentals

Fast reference for array creation, indexing, vectorization, and aggregation.

## Creating Arrays
```python
import numpy as np

np.array([1, 2, 3])            # from a list
np.array([[1, 2], [3, 4]])       # from a list of lists -> 2D

np.zeros(5)                          # array of 0.0s
np.ones((2, 3))                        # array of 1.0s, shape (2, 3)
np.arange(0, 10, 2)                       # step-based: [0 2 4 6 8]
np.linspace(0, 1, 5)                        # count-based: 5 evenly spaced points
np.eye(3)                                     # 3x3 identity matrix
```

## Inspecting Arrays
```python
arr.shape       # dimensions, e.g. (3, 4) -- ATTRIBUTE, no ()
arr.ndim          # number of dimensions
arr.size            # total element count
arr.dtype             # data type of elements (int64, float64, ...)
```

## Indexing & Slicing
```python
arr[0]              # first element (1D)
arr[-1]                # last element
arr[1:3]                 # slice

matrix[row, col]           # 2D: comma-separated
matrix[0, :]                  # entire row 0
matrix[:, 0]                    # entire column 0
matrix[0:2, 1:3]                  # sub-block

sub = arr[1:3].copy()               # .copy() -- slices are VIEWS by default!
```

## Vectorized Arithmetic (element-wise)
```python
a + b     a - b     a * b     a / b     a ** 2
a > 2       # -> boolean array
```
⚠️ NumPy array `+` is element-wise math; Python list `+` is concatenation.

## Broadcasting
```python
arr + 10                        # scalar broadcasts to every element
matrix + row_vector                # 1D row broadcasts across every row of a 2D array
```
Shapes must align right-to-left: equal, or one of them is `1`/missing.

## Boolean Indexing (Masking)
```python
arr[arr > 60]                       # elements where condition is True
arr[(arr > 60) & (arr < 90)]           # combine conditions: use & / | (NOT and/or), parens required
(arr < 60).sum()                          # count of True values
```

## Fancy Indexing
```python
arr[[0, 2, 4]]      # select specific positions, any order
```

## Aggregation Functions
```python
arr.sum()   arr.mean()   arr.std()   arr.min()   arr.max()
arr.argmax()   arr.argmin()     # INDEX of max/min, not the value
```

## `axis` — the Dimension That Collapses
```python
matrix.sum(axis=0)     # collapse axis 0 (rows) -> one result per COLUMN
matrix.sum(axis=1)       # collapse axis 1 (columns) -> one result per ROW
```
💡 The axis number is the dimension that *disappears* from the result.

## Reshaping
```python
arr.reshape(3, 4)         # must match total element count
arr.reshape(3, -1)           # -1 = "figure this dimension out for me"
matrix.flatten()                # collapse to 1D -- always returns a COPY
matrix.T                          # transpose -- swap rows/columns
```

## Combining Arrays
```python
np.concatenate([a, b])     # join along existing axis
np.vstack([a, b])             # stack as new rows
np.hstack([a, b])                # stack side by side
```

## Quick Troubleshooting

| Error | Likely Cause | Fix |
|---|---|---|
| `ValueError: operands could not be broadcast together` | Shapes genuinely incompatible | Check `.shape` on both arrays; align dimensions |
| `ValueError: cannot reshape array of size N into shape (...)` | Target shape's element count doesn't match | Confirm `rows * cols == arr.size`, or use `-1` |
| `ValueError: truth value of an array is ambiguous` | Used `and`/`or` on array conditions | Use `&`/`\|` with parentheses around each condition |
| Modifying a slice changed the original array | Slices are views by default | Call `.copy()` if you need an independent array |
| Confusing `max()` with `argmax()` | `max()` returns the value, `argmax()` returns its index | Use `argmax`/`argmin` when you need the position |

## The "New Array Task" Workflow
1. Create the array with the right creation function (`array`, `zeros`, `arange`, `linspace`).
2. Check `.shape` and `.dtype` immediately — most bugs trace back to a wrong shape.
3. Prefer vectorized operations and boolean masks over any `for` loop.
4. When aggregating a 2D array, pause and confirm which `axis` gives the result you actually want.
5. Reshape/transpose only at the point you need a different dimensional layout — don't do it speculatively.
