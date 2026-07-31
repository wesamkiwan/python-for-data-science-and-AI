# Module 07b: Selection & Filtering with `.loc`, `.iloc` & Boolean Masks

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [01-series-and-dataframes.md](01-series-and-dataframes.md)

## 🎯 Learning Objectives
- [ ] Select one or more columns from a DataFrame
- [ ] Use `.loc` (label-based) and `.iloc` (position-based) selection
- [ ] Filter rows with boolean masks, including combined conditions
- [ ] Explain the difference between `.loc`/`.iloc` and boolean filtering, and when to use each

---

## Module Goal

Learn to precisely select and filter the exact rows and columns you need from a DataFrame — the single most common thing you'll do with real data, whether preparing it for analysis, cleaning, or feeding it into a model.

## Why This Matters on the Job

"Give me just the rows where revenue is over $10,000" or "show me only the name and email columns" are everyday requests, and Pandas' selection tools answer them in one line. This module's boolean filtering is the *exact same mental model* as Module 06's NumPy boolean indexing (`arr[arr > 60]`) — if that clicked, this will feel immediately familiar, just applied to labeled rows and columns instead of a raw array.

---

## Selecting Columns

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ada", "Grace", "Alan", "Katherine", "Linus"],
    "age": [36, 85, 41, 101, 33],
    "department": ["Engineering", "Engineering", "Research", "Research", "Engineering"],
    "salary": [95000, 120000, 88000, 130000, 91000]
})

print(df["name"])           # a single column -> returns a Series
print(type(df["name"]))       # <class 'pandas.core.series.Series'>

print(df[["name", "age"]])       # multiple columns -> returns a DataFrame (note the DOUBLE brackets)
```

⚠️ **Warning:** `df["name"]` (single brackets) returns a `Series`. `df[["name"]]` (double brackets — a list containing one name) returns a one-column `DataFrame`. These look almost identical but behave differently for some operations — the double-bracket list form is what you need whenever you want to select *multiple* columns.

## `.loc`: Label-Based Selection

`.loc` selects by **label** — the actual index value and column name, not their position.

```python
print(df.loc[0])                       # entire row with index label 0 (a Series)
print(df.loc[0, "name"])                  # single value: row 0, column "name"
print(df.loc[0:2, ["name", "age"]])          # rows with labels 0 through 2 (INCLUSIVE), specific columns
```

⚠️ **Warning:** `.loc` slicing is **inclusive of the end label** — `df.loc[0:2]` includes rows `0`, `1`, *and* `2`. This is different from Python's normal slicing (and from `.iloc`, below), where the end is always exclusive. This inconsistency exists because `.loc` slices by label, and labels aren't always sequential integers — but it's a very common point of confusion.

## `.iloc`: Position-Based Selection

`.iloc` selects by **integer position**, exactly like indexing a Python list or NumPy array — regardless of what the actual index labels are.

```python
print(df.iloc[0])                # first row, by position
print(df.iloc[0, 0])                # row 0, column 0 (by position)
print(df.iloc[0:2, 0:2])               # rows 0-1 (end EXCLUSIVE, like normal slicing), columns 0-1
```

| | `.loc` | `.iloc` |
|---|---|---|
| Selects by | Label (index value, column name) | Integer position |
| Slice end | **Inclusive** | **Exclusive** (like standard Python) |
| Use when | You know the actual labels | You know the position, regardless of labels |

💡 **Tip:** When the DataFrame's index is the default `0, 1, 2, ...` (as in most examples so far), `.loc` and `.iloc` happen to select the *same* rows for a single integer — but their slicing behavior still differs, and once you set a custom index (e.g., dates, or IDs), only `.loc` continues to make sense for label-based lookups like `df.loc["2024-01-15"]`.

## Filtering Rows with Boolean Masks

This is the pattern you'll use constantly — filter rows based on a condition, using the exact same idea as NumPy's `arr[arr > 60]`:

```python
print(df[df["age"] > 50])
```
```
        name  age   department  salary
1      Grace   85  Engineering  120000
3  Katherine  101     Research  130000
```

**How it works:** `df["age"] > 50` produces a boolean Series (`True`/`False` for each row). Using that boolean Series as `df[...]` keeps only the rows where it's `True` — exactly like NumPy's boolean masking, just filtering whole rows of a table instead of elements of a flat array.

### Combining Conditions

```python
print(df[(df["department"] == "Engineering") & (df["age"] < 40)])
```
```
    name  age   department  salary
0    Ada   36  Engineering   95000
4  Linus   33  Engineering   91000
```

⚠️ **Warning:** Exactly like NumPy in Module 06 — use `&` (and) / `|` (or), never Python's `and`/`or`, and wrap each condition in its own parentheses. `df["department"] == "Engineering" & df["age"] < 40` (without parens) raises a confusing error due to operator precedence; `(df["department"] == "Engineering") & (df["age"] < 40)` is correct.

### Filtering with `.loc` and a Condition

You can combine `.loc` with a boolean condition to filter rows *and* select specific columns in one step:

```python
print(df.loc[df["age"] > 50, ["name", "salary"]])
```
```
        name  salary
1      Grace  120000
3  Katherine  130000
```

✅ **Best Practice:** `df.loc[row_condition, column_list]` is the idiomatic, recommended way to filter rows and select columns simultaneously — cleaner than filtering first and then selecting columns as two separate steps.

## `.isin()`: Matching Against a List of Values

```python
target_departments = ["Research", "Sales"]
print(df[df["department"].isin(target_departments)])
```
```
        name  age department  salary
2       Alan   41   Research   88000
3  Katherine  101   Research  130000
```

💡 **Tip:** `.isin([...])` is the clean way to check "is this value one of several options" — the alternative, chaining multiple `==` conditions with `|`, works but becomes unwieldy past two or three options.

---

## Hands-On Exercise

**Task:** Write `filtering_practice.py` using this DataFrame:
```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104, 105, 106],
    "customer": ["Ada", "Grace", "Alan", "Ada", "Katherine", "Alan"],
    "amount": [250.00, 89.50, 430.00, 75.25, 600.00, 120.00],
    "status": ["shipped", "pending", "shipped", "cancelled", "shipped", "pending"]
})
```
1. Select and print just the `customer` and `amount` columns.
2. Use `.iloc` to print the first 3 rows and only the first 2 columns.
3. Filter and print only the orders with `status == "shipped"`.
4. Filter and print orders where `amount > 100` AND `status != "cancelled"`.
5. Use `.loc` to print just the `customer` and `amount` columns for orders placed by `"Ada"` or `"Alan"` (use `.isin()`).

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [101, 102, 103, 104, 105, 106],
    "customer": ["Ada", "Grace", "Alan", "Ada", "Katherine", "Alan"],
    "amount": [250.00, 89.50, 430.00, 75.25, 600.00, 120.00],
    "status": ["shipped", "pending", "shipped", "cancelled", "shipped", "pending"]
})

print(orders[["customer", "amount"]])

print(orders.iloc[0:3, 0:2])

print(orders[orders["status"] == "shipped"])

print(orders[(orders["amount"] > 100) & (orders["status"] != "cancelled")])

print(orders.loc[orders["customer"].isin(["Ada", "Alan"]), ["customer", "amount"]])
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Using `and`/`or` to combine DataFrame conditions | Use `&`/`\|` with parentheses around each condition |
| Forgetting `.loc`'s slice end is inclusive | Remember: `.loc` includes the end label; `.iloc` excludes it |
| Single vs. double brackets confusion | `df["col"]` -> Series; `df[["col"]]` -> one-column DataFrame |
| Chaining many `== "x"` / `== "y"` conditions with `\|` | Use `.isin([...])` instead once you have 3+ options |
| Filtering, then separately selecting columns | Combine into one step: `df.loc[condition, columns]` |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Can select single and multiple columns
- [ ] Understand `.loc` (label-based, inclusive slicing) vs. `.iloc` (position-based, exclusive slicing)
- [ ] Can filter rows with a boolean mask, including combined conditions
- [ ] Can use `.isin()` to match against a list of values
- [ ] Completed the `filtering_practice.py` exercise

**Next:** Continue to [`03-column-operations-and-sorting.md`](03-column-operations-and-sorting.md)
