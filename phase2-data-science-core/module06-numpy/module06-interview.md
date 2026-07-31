# 🎤 Module 06 Interview Prep: NumPy Fundamentals

## Conceptual Questions

### 🟢 Beginner

**Q: What is a NumPy array, and how is it different from a Python list?**
> A: A NumPy array (`ndarray`) is a fixed-type, contiguous block of memory optimized for numeric computation. Unlike a Python list, every element must share the same data type, and operations are implemented in compiled C code rather than the Python interpreter looping element by element. This makes arrays much faster and more memory-efficient for numeric work, at the cost of the flexibility to mix arbitrary types that a plain list offers.

**Q: What does "vectorization" mean, and why is it faster than a `for` loop?**
> A: Vectorization means applying an operation to an entire array at once (`arr * 2`) instead of looping over each element in Python (`for x in arr: x * 2`). It's faster because the actual looping happens inside NumPy's compiled C code, avoiding the overhead Python normally pays on every loop iteration (type-checking each element, interpreter bytecode dispatch, etc.). In practice this can be anywhere from several times to 50x+ faster, depending on the operation and array size.

**Q: What's the difference between `.shape` and `.reshape()`?**
> A: `.shape` is a read-only attribute that reports an array's current dimensions as a tuple, e.g. `(3, 4)`. `.reshape(new_shape)` is a method that returns a *new view* of the same data reorganized into different dimensions, as long as the total number of elements stays the same. `.shape` describes; `.reshape()` transforms.

### 🟡 Intermediate

**Q: Explain broadcasting with an example.**
> A: Broadcasting is NumPy's rule for combining arrays of different shapes in arithmetic by conceptually stretching the smaller array to match the larger one's shape, without actually copying data. For example, adding a shape `(3,)` array to a shape `(3, 3)` matrix broadcasts the smaller array across every row. NumPy compares shapes dimension by dimension from right to left — they're compatible if equal, or if one of them is `1` (or missing) — and raises a `ValueError` if they can't be aligned this way.

**Q: How does `axis=0` differ from `axis=1` when aggregating a 2D array?**
> A: The axis number identifies which dimension collapses in the result. `axis=0` collapses the rows, producing one result per column (e.g., `matrix.sum(axis=0)` gives column totals). `axis=1` collapses the columns, producing one result per row (row totals). A useful way to remember it: the axis you specify is the dimension that *disappears* from the output's shape.

**Q: Why is boolean indexing (`arr[arr > 60]`) preferred over writing a manual loop with an `if` check?**
> A: Boolean indexing is vectorized — the comparison `arr > 60` and the subsequent filtering both happen in NumPy's optimized internals rather than a Python-level loop, so it's both significantly faster on large arrays and more concise/readable. It's also the exact same pattern used to filter rows in a Pandas DataFrame later, so the mental model transfers directly.

## Practical/Coding Questions

**Q: Given a 2D array of exam scores (rows = students, columns = exams), write code to find the average score per student and the average score per exam.**
```python
import numpy as np

scores = np.array([
    [85, 90, 78],
    [92, 88, 95],
    [70, 75, 80],
])

avg_per_student = scores.mean(axis=1)   # one average per row -> per student
avg_per_exam = scores.mean(axis=0)          # one average per column -> per exam

print(avg_per_student)   # [84.33 91.67 75.  ]
print(avg_per_exam)         # [82.33 84.33 84.33]
```
> Explanation: "per student" means collapsing across each student's own row of exams, i.e. `axis=1`; "per exam" means collapsing down each exam's column across all students, i.e. `axis=0`.

**Q: Write code that replaces every negative value in an array with 0, without using a loop.**
```python
import numpy as np

arr = np.array([5, -3, 8, -1, 0, -7])
arr[arr < 0] = 0
print(arr)   # [5 0 8 0 0 0]
```
> Explanation: `arr < 0` produces a boolean mask identifying the negative positions; assigning `0` to `arr[mask]` updates exactly those positions in place, all in one vectorized statement.

## Scenario Questions

**Q: You're processing a dataset with a million rows and need to compute a transformed value for every row. A colleague suggests writing a `for` loop over the array. What would you say?**
> A: I'd recommend checking for a vectorized equivalent first — NumPy (and later, Pandas) almost always has one, and at a million rows, the performance difference between a Python loop and a vectorized operation is often dramatic (potentially minutes versus a fraction of a second). I'd only reach for a loop if the transformation genuinely can't be expressed as array operations — e.g., it depends on complex conditional branching per element that doesn't map cleanly to broadcasting or masking — and even then, I'd look at `np.where()` or `np.vectorize()` before defaulting to a plain loop.

**Q: You need to reshape a flat array of 784 pixel values (from a 28x28 grayscale image dataset) back into its original image grid to visualize it. How would you do this?**
> A: `pixels.reshape(28, 28)` — since 28 × 28 = 784, this exactly matches the total element count, reorganizing the flat array into a 2D grid without changing the underlying data or its order. This is a very common step when working with image datasets (covered further in Module 17), where images are often stored flattened for model input but need reshaping back to 2D for display.

## "Gotcha" Questions

**Q: What does this print, and why might it surprise someone coming from working with Python lists?**
```python
arr = np.array([1, 2, 3, 4, 5])
sub = arr[1:3]
sub[0] = 999
print(arr)
```
> A: It prints `[1 999 3 4 5]`. Unlike slicing a Python list (which creates an independent copy), slicing a NumPy array returns a *view* into the same underlying memory — modifying the slice modifies the original array too. To get an independent copy, you'd need `arr[1:3].copy()`.

**Q: What's wrong with this code, and what error does it raise?**
```python
arr = np.array([1, 2, 3, 4, 5])
if arr > 2 and arr < 5:
    print("in range")
```
> A: It raises `ValueError: The truth value of an array with more than one element is ambiguous`. Python's `and`/`or` expect a single `True`/`False`, but `arr > 2` returns an entire boolean *array*, not one value. The fix is to use the element-wise `&` operator with parentheses around each condition: `(arr > 2) & (arr < 5)`.

## Quick-Fire Rapid Review

- Q: What must be true for `reshape()` to succeed? → **the new shape's total element count must match the original**
- Q: Which axis collapses to give per-column results? → **`axis=0`**
- Q: Which axis collapses to give per-row results? → **`axis=1`**
- Q: Does `.flatten()` return a view or a copy? → **a copy**
- Q: Does slicing an array return a view or a copy? → **a view**
- Q: Correct operator to combine two array conditions? → **`&` (or `|` for "or"), not `and`/`or`**
- Q: Function that returns the *index* of the max value? → **`argmax()`**
- Q: `np.arange` is step-based; what's the count-based equivalent? → **`np.linspace`**
