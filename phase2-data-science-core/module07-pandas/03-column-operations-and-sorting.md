# Module 07c: Column Operations & Sorting

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [02-selection-and-filtering.md](02-selection-and-filtering.md)

## 🎯 Learning Objectives
- [ ] Add, modify, and drop columns
- [ ] Apply vectorized arithmetic across columns
- [ ] Use `.apply()` for custom, row-by-row transformations
- [ ] Sort a DataFrame with `.sort_values()`

---

## Module Goal

Learn to reshape a dataset's *columns* — computing new ones, transforming existing ones, and removing what you don't need — plus how to order rows meaningfully with sorting. This is the "transform" step that typically follows the "select and filter" skills from the last lesson.

## Why This Matters on the Job

Real analysis almost always requires deriving new information from existing columns — a profit margin from revenue and cost, an age group from a birth date, a full name from first/last name fields. Vectorized column math (directly inherited from Module 06's NumPy broadcasting) handles this in one line for the vast majority of cases; `.apply()` is your fallback for the rarer cases that need custom, per-row logic.

---

## Adding and Modifying Columns

The simplest way to add a column is vectorized arithmetic on existing ones — exactly like NumPy broadcasting, just labeled:

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ada", "Grace", "Alan", "Katherine", "Linus"],
    "age": [36, 85, 41, 101, 33],
    "department": ["Engineering", "Engineering", "Research", "Research", "Engineering"],
    "salary": [95000, 120000, 88000, 130000, 91000]
})

df["bonus"] = df["salary"] * 0.1        # new column: 10% of salary
print(df)
```
```
        name  age   department  salary    bonus
0        Ada   36  Engineering   95000   9500.0
1      Grace   85  Engineering  120000  12000.0
2       Alan   41     Research   88000   8800.0
3  Katherine  101     Research  130000  13000.0
4      Linus   33  Engineering   91000   9100.0
```

**How it works:** `df["salary"] * 0.1` is a vectorized operation across the entire `salary` column (a Series), producing a new Series that gets assigned to the new column name `df["bonus"]` — no loop needed, exactly like Module 06's array broadcasting.

You can modify an existing column the same way:

```python
df["salary"] = df["salary"] * 1.05   # a 5% raise across the board
```

## `.apply()`: Custom, Row-by-Row Logic

When a transformation can't be expressed as simple vectorized arithmetic — e.g., conditional logic per value — use `.apply()` with a function (often a `lambda`, from... well, this is the first time this course introduces one; it's just a compact, unnamed function).

```python
df["seniority"] = df["age"].apply(lambda age: "Senior" if age > 50 else "Junior")
print(df[["name", "age", "seniority"]])
```
```
        name  age seniority
0        Ada   36    Junior
1      Grace   85    Senior
2       Alan   41    Junior
3  Katherine  101    Senior
4      Linus   33    Junior
```

**How it works:** `.apply(function)` calls `function` once for *every value* in the Series, collecting the results into a new Series. `lambda age: "Senior" if age > 50 else "Junior"` is a shorthand, inline function — equivalent to writing:

```python
def classify_seniority(age):
    return "Senior" if age > 50 else "Junior"

df["seniority"] = df["age"].apply(classify_seniority)
```

⚠️ **Warning:** `.apply()` is meaningfully slower than vectorized operations, because it *does* run a Python function call per row internally (losing the C-level speed advantage from Module 06). ✅ **Best Practice:** always check first whether your logic can be expressed with vectorized comparisons/arithmetic or `np.where()` before reaching for `.apply()` — reserve it for genuinely custom logic that doesn't fit those patterns.

```python
import numpy as np
# Vectorized alternative to the seniority example above -- faster on large data
df["seniority"] = np.where(df["age"] > 50, "Senior", "Junior")
```

## Dropping Columns (and Rows)

```python
df_dropped = df.drop(columns=["bonus"])           # drop one or more columns
print(df_dropped.columns.tolist())

df_no_first_row = df.drop(index=0)                    # drop a row by its index label
```

⚠️ **Warning:** `.drop()` returns a **new** DataFrame by default — it does not modify `df` in place. If you want to update the original variable, reassign it: `df = df.drop(columns=["bonus"])`.

## Renaming Columns

```python
df = df.rename(columns={"name": "employee_name", "age": "employee_age"})
```

## Sorting with `.sort_values()`

```python
print(df.sort_values("age"))                           # ascending by default
print(df.sort_values("age", ascending=False))              # descending
print(df.sort_values(["department", "age"]))                  # sort by multiple columns, in order
```

**How it works:** `.sort_values(["department", "age"])` sorts first by `department` (alphabetically), and *within* each department, by `age` — exactly like sorting a spreadsheet by multiple columns. This is the standard way to produce a meaningfully ordered report (e.g., "top performers within each team").

💡 **Tip:** `.sort_values()` returns a new, sorted DataFrame — like `.drop()`, it doesn't sort in place unless you pass `inplace=True` (generally discouraged in modern Pandas in favor of explicit reassignment: `df = df.sort_values(...)`).

---

## Hands-On Exercise

**Task:** Write `column_operations_practice.py` using this DataFrame:
```python
import pandas as pd

products = pd.DataFrame({
    "name": ["Laptop", "Mouse", "Keyboard", "Monitor", "Webcam"],
    "cost": [700.00, 10.00, 20.00, 150.00, 25.00],
    "price": [999.99, 25.50, 45.00, 249.99, 60.00]
})
```
1. Add a column `profit` equal to `price - cost`.
2. Add a column `margin_pct` equal to `(profit / price) * 100`, rounded to 1 decimal place (hint: `.round(1)`).
3. Use `.apply()` (or `np.where()`) to add a column `price_tier` that's `"Premium"` if `price > 100`, otherwise `"Standard"`.
4. Sort the result by `profit`, descending, and print it.
5. Drop the `cost` column from the final result before printing.

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd
import numpy as np

products = pd.DataFrame({
    "name": ["Laptop", "Mouse", "Keyboard", "Monitor", "Webcam"],
    "cost": [700.00, 10.00, 20.00, 150.00, 25.00],
    "price": [999.99, 25.50, 45.00, 249.99, 60.00]
})

products["profit"] = products["price"] - products["cost"]
products["margin_pct"] = ((products["profit"] / products["price"]) * 100).round(1)
products["price_tier"] = np.where(products["price"] > 100, "Premium", "Standard")

result = products.sort_values("profit", ascending=False).drop(columns=["cost"])
print(result)
```

**Expected output:**
```
       name   price  profit  margin_pct price_tier
0    Laptop  999.99  299.99        30.0    Premium
3   Monitor  249.99   99.99        40.0    Premium
4    Webcam   60.00   35.00        58.3   Standard
2  Keyboard   45.00   25.00        55.6   Standard
1     Mouse   25.50   15.50        60.8   Standard
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Reaching for `.apply()` by default | Check for a vectorized alternative (arithmetic, `np.where()`) first — it's faster |
| Assuming `.drop()`/`.sort_values()` modify in place | They return a new DataFrame by default — reassign the result |
| Forgetting `columns=` in `.drop()` | `df.drop(columns=["x"])` for columns, `df.drop(index=[0])` for rows — easy to mix up |
| Sorting by one column when a tiebreaker matters | Pass a list to `.sort_values(["col1", "col2"])` for multi-column sort |

---

## ✅ Module Completion Checklist (Part C)
- [ ] Can add/modify columns with vectorized arithmetic
- [ ] Can use `.apply()` and know when a vectorized alternative is preferable
- [ ] Can drop columns/rows and rename columns
- [ ] Can sort by one or multiple columns, ascending or descending
- [ ] Completed the `column_operations_practice.py` exercise

**Next:** Continue to [`04-groupby-and-merging.md`](04-groupby-and-merging.md)
