# Module 06c: Aggregation Functions & Reshaping

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [02-vectorization-and-broadcasting.md](02-vectorization-and-broadcasting.md)

## 🎯 Learning Objectives
- [ ] Use aggregation functions (`sum`, `mean`, `std`, `min`, `max`) on arrays
- [ ] Understand and apply the `axis` parameter for row-wise vs. column-wise aggregation
- [ ] Reshape arrays with `.reshape()`, `.flatten()`, and `.T` (transpose)
- [ ] Combine and split arrays with `np.concatenate`, `np.vstack`, and `np.hstack`

---

## Module Goal

Learn to summarize arrays with **aggregation functions** — turning many values into one meaningful number (a total, an average, a spread) — and to reshape data into whatever dimensional structure a task requires. These are the final core NumPy skills before Module 07 introduces Pandas, which builds directly on both.

## Why This Matters on the Job

"What's the average of this column?" "What's the total per row?" "Reshape this flat list of pixels back into a 28x28 image" — these are daily questions in real data work, and NumPy's aggregation functions with the `axis` parameter answer them in one line. Getting `axis=0` vs. `axis=1` right (and confidently) is one of those small things that separates confident practitioners from people who guess-and-check every time — this module builds that intuition solidly.

---

## Aggregation Functions

```python
import numpy as np

scores = np.array([85, 92, 78, 90, 65])

print(scores.sum())        # 410     -- total
print(scores.mean())          # 82.0   -- average
print(scores.std())             # 9.777...  -- standard deviation (spread around the mean)
print(scores.min())               # 65      -- smallest value
print(scores.max())                 # 92       -- largest value
print(scores.argmax())                 # 1          -- INDEX of the largest value (not the value itself)
print(scores.argmin())                    # 4            -- INDEX of the smallest value
```

**How it works:** Each of these methods collapses an entire array down to a single summary number. `argmax()`/`argmin()` are subtly different from `max()`/`min()` — they return the *position* of the extreme value, not the value itself, which is useful when you need to know *which* element was the biggest/smallest, not just what its value was.

💡 **Tip:** These are also available as standalone functions — `np.sum(scores)` and `scores.sum()` do the exact same thing. Both styles are common in real code; use whichever reads more naturally in context.

## The `axis` Parameter: Row-wise vs. Column-wise

On a 2D array, aggregation functions default to collapsing the *entire* array into one number — but you can instead collapse along just one dimension using `axis`.

```python
grades = np.array([
    [85, 90, 78],    # student 1's three test scores
    [92, 88, 95],    # student 2's three test scores
    [70, 75, 80]     # student 3's three test scores
])

print(grades.sum())            # 753  -- sum of EVERY value in the whole array
print(grades.sum(axis=0))        # [247 253 253]  -- sum DOWN each column (per-test totals)
print(grades.sum(axis=1))          # [253 275 225]  -- sum ACROSS each row (per-student totals)

print(grades.mean(axis=0))            # [82.33 84.33 84.33]  -- average score per test, across all students
print(grades.mean(axis=1))              # [84.33 91.67 75.0]    -- average score per student, across all tests
```

**How it works — the trick that makes `axis` click:** `axis=0` means "collapse along the rows" (moving *down* the rows, producing one result per **column**). `axis=1` means "collapse along the columns" (moving *across* the columns, producing one result per **row**).

💡 **Tip:** A reliable memory trick: the axis number tells you *which dimension disappears*. `grades.shape` is `(3, 3)` here (3 students, 3 tests). `grades.sum(axis=0)` collapses dimension 0 (the 3 students), leaving one number per test — shape `(3,)` of per-test totals. `grades.sum(axis=1)` collapses dimension 1 (the 3 tests), leaving one number per student.

🎯 **On the job:** This is *exactly* the same mental model as Pandas' `df.mean(axis=0)` (average of each column, across all rows) vs. `df.mean(axis=1)` (average of each row, across all columns) — nailing `axis` here in NumPy means Module 07's Pandas aggregations will already feel intuitive.

## Reshaping Arrays

### `.reshape()`: Changing Dimensions Without Changing Data

```python
arr = np.arange(12)
print(arr)                 # [ 0  1  2  3  4  5  6  7  8  9 10 11]

reshaped = arr.reshape(3, 4)     # reorganize into 3 rows, 4 columns
print(reshaped)
```
```
[[ 0  1  2  3]
 [ 4  5  6  7]
 [ 8  9 10 11]]
```

⚠️ **Warning:** The total number of elements must stay the same — `reshape(3, 4)` requires exactly 12 elements (3 × 4). Trying to reshape into an incompatible size raises `ValueError: cannot reshape array of size 12 into shape (3,3)`.

💡 **Tip:** Pass `-1` for one dimension to let NumPy calculate it automatically: `arr.reshape(3, -1)` figures out the column count for you, given 3 rows. Very handy when you know one dimension but don't want to compute the other by hand.

```python
print(arr.reshape(3, -1))   # NumPy calculates -1 -> 4 columns, since 12 / 3 = 4
```

### `.flatten()`: Collapsing Back to 1D

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
flat = matrix.flatten()
print(flat)   # [1 2 3 4 5 6]
```

⚠️ **Warning:** Unlike a slice, `.flatten()` always returns a **copy** — modifying `flat` will *not* affect the original `matrix`. (The related `.ravel()` method returns a view when possible instead — a subtle distinction worth knowing exists, but `.flatten()`'s guaranteed-copy behavior is the safer default while learning.)

### `.T`: Transposing (Swapping Rows and Columns)

```python
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix.shape)     # (2, 3)
print(matrix.T)            # transpose -- rows become columns
print(matrix.T.shape)         # (3, 2)
```
```
[[1 4]
 [2 5]
 [3 6]]
```

🎯 **On the job:** Reshaping and transposing come up constantly when preparing data for machine learning models — e.g., reshaping a flat array of image pixel values back into a `(height, width)` grid, or transposing data so rows represent samples and columns represent features (the standard convention scikit-learn expects, covered in Module 12).

## Combining Arrays

```python
a = np.array([1, 2, 3])
b = np.array([4, 5, 6])

print(np.concatenate([a, b]))    # [1 2 3 4 5 6]  -- join along existing axis

print(np.vstack([a, b]))            # stack vertically -> becomes a 2x3 matrix
print(np.hstack([a, b]))               # stack horizontally -> [1 2 3 4 5 6] for 1D arrays
```
```
[[1 2 3]
 [4 5 6]]
```

**How it works:** `np.vstack` ("vertical stack") stacks arrays as new *rows*; `np.hstack` ("horizontal stack") joins them side by side along existing rows (for 1D arrays, this is equivalent to `concatenate`).

---

## Hands-On Exercise

**Task:** Write `sales_analysis.py` that:
1. Creates a 2D array `sales` representing 4 weeks (rows) of daily sales for 5 days (columns) — use any reasonable numbers.
2. Prints the total sales for the entire month.
3. Prints the total sales **per day-of-week** (i.e., summed down the weeks) using the correct `axis`.
4. Prints the total sales **per week** (i.e., summed across the days) using the correct `axis`.
5. Finds which week (by index) had the highest total sales, using `argmax()` on the per-week totals.
6. Reshapes the original `(4, 5)` array into a flat `(20,)` array using `.flatten()`, and separately into a `(5, 4)` array using `.reshape()`.

<details>
<summary>✅ Click to see the solution</summary>

```python
import numpy as np

sales = np.array([
    [120, 150, 130, 170, 200],   # week 1: Mon-Fri
    [110, 160, 140, 180, 210],   # week 2: Mon-Fri
    [130, 155, 135, 175, 205],   # week 3: Mon-Fri
    [125, 165, 145, 185, 220],   # week 4: Mon-Fri
])

print(f"Total sales for the month: {sales.sum()}")

per_day = sales.sum(axis=0)
print(f"Total sales per day of week (Mon-Fri): {per_day}")

per_week = sales.sum(axis=1)
print(f"Total sales per week: {per_week}")

best_week_index = per_week.argmax()
print(f"Best week (0-indexed): Week {best_week_index + 1}, with {per_week[best_week_index]} in sales")

flat_sales = sales.flatten()
print(f"Flattened shape: {flat_sales.shape}")

reshaped_sales = sales.reshape(5, 4)
print(f"Reshaped (5, 4):\n{reshaped_sales}")
```

**Expected output:**
```
Total sales for the month: 3210
Total sales per day of week (Mon-Fri): [ 485  630  550  710  835]
Total sales per week: [770 800 800 840]
Best week (0-indexed): Week 4, with 840 in sales
Flattened shape: (20,)
Reshaped (5, 4):
[[120 150 130 170]
 [200 110 160 140]
 [180 210 130 155]
 [135 175 205 125]
 [165 145 185 220]]
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Confusing `axis=0` and `axis=1` | Remember: the axis number is the dimension that *disappears* / collapses |
| Confusing `max()`/`min()` (the value) with `argmax()`/`argmin()` (the position) | Use `argmax`/`argmin` specifically when you need to know *which* element, not just its value |
| Assuming `.reshape()` always works | Total element count must match exactly; use `-1` to let NumPy compute one dimension |
| Assuming `.flatten()` returns a view | It always returns a copy — modifying it won't affect the original |
| Reshaping instead of transposing (or vice versa) | Reshape changes dimensional grouping while keeping element order; transpose swaps rows/columns based on position — they're not interchangeable |

---

## ✅ Module 06 Completion Checklist
- [ ] Can use `sum`, `mean`, `std`, `min`, `max`, `argmax`, `argmin`
- [ ] Confidently choose `axis=0` vs. `axis=1` for row-wise vs. column-wise aggregation
- [ ] Can reshape arrays with `.reshape()` (including using `-1`) and `.flatten()`
- [ ] Understand `.T` (transpose) and when it's useful
- [ ] Can combine arrays with `np.concatenate`/`vstack`/`hstack`
- [ ] Completed the `sales_analysis.py` exercise
- [ ] Reviewed [`module06-cheatsheet.md`](module06-cheatsheet.md)
- [ ] Reviewed [`module06-interview.md`](module06-interview.md)
- [ ] Browsed [`module06-references.md`](module06-references.md)

**Next Step:** Module 07 — Pandas for Data Manipulation (`phase2-data-science-core/module07-pandas/`)
