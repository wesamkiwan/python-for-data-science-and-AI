# 🎤 Module 07 Interview Prep: Pandas for Data Manipulation

## Conceptual Questions

### 🟢 Beginner

**Q: What's the difference between a Pandas `Series` and a `DataFrame`?**
> A: A `Series` is a single, one-dimensional labeled array — essentially one column of data with an index. A `DataFrame` is a two-dimensional table made up of multiple Series sharing the same index, each one a column. Selecting a single column from a DataFrame (`df["col"]`) returns exactly a Series.

**Q: What does `df.info()` tell you that `df.describe()` doesn't, and vice versa?**
> A: `.info()` reports column names, their data types, non-null counts (revealing missing data), and memory usage — a structural overview. `.describe()` computes summary statistics (mean, standard deviation, quartiles, min/max) for numeric columns only, giving a distributional overview. In practice, I'd run both immediately after loading any new dataset — `.info()` for structure, `.describe()` for a first sense of the numbers.

**Q: Why should you pass `index=False` when calling `.to_csv()`?**
> A: By default, Pandas writes its own row index as an extra column in the output file. `index=False` omits it, which is almost always what you want — otherwise, reading the file back in later adds a redundant "Unnamed: 0"-style column that has to be cleaned up.

### 🟡 Intermediate

**Q: Explain the difference between `.loc` and `.iloc`.**
> A: `.loc` selects by label — the actual index value and column name — and its slices are *inclusive* of the end label. `.iloc` selects by integer position, regardless of the actual labels, and its slices are *exclusive* of the end, matching standard Python slicing behavior. When the index is the default `0, 1, 2, ...`, they can look similar for single selections, but their slicing behavior always differs, and `.loc` is the only option once you have a non-integer index (like dates or IDs).

**Q: Walk through what happens, step by step, when you call `df.groupby("department")["salary"].mean()`.**
> A: This follows the split-apply-combine pattern: Pandas first *splits* the DataFrame into separate groups, one per unique value in `department`. It then *applies* the `.mean()` aggregation to the `salary` column within each group independently. Finally, it *combines* those per-group results into a single Series, indexed by the department values.

**Q: What's the difference between the four `how` options in `pd.merge()`?**
> A: `"inner"` (the default) keeps only rows with a matching key in both DataFrames. `"left"` keeps every row from the left DataFrame, filling in `NaN` where there's no match on the right. `"right"` does the mirror image, keeping every row from the right. `"outer"` keeps every row from both sides, with `NaN` wherever a match is missing on either side. Choosing correctly depends on which side's completeness you need to guarantee.

## Practical/Coding Questions

**Q: Given a DataFrame `df` with a `revenue` column, write code to add a `revenue_category` column that's `"High"` for revenue over 10,000, `"Medium"` for 1,000-10,000, and `"Low"` below that — using a vectorized approach, not `.apply()`.**
```python
import numpy as np

conditions = [df["revenue"] > 10000, df["revenue"] >= 1000]
choices = ["High", "Medium"]
df["revenue_category"] = np.select(conditions, choices, default="Low")
```
> Explanation: `np.where()` only handles a single binary condition; `np.select()` extends that to multiple conditions evaluated in order, each paired with a corresponding output — the first matching condition wins, and `default` covers anything that matches none of them. This stays fully vectorized, unlike an equivalent `.apply()` with an if/elif chain.

**Q: Given `orders` (with a `customer_id` column) and `customers` (with `customer_id` and `customer_name`), write code to find the total amount spent by each named customer, sorted from highest to lowest.**
```python
import pandas as pd

merged = pd.merge(orders, customers, on="customer_id", how="left")
totals = merged.groupby("customer_name")["amount"].sum().sort_values(ascending=False)
print(totals)
```
> Explanation: merge first to attach the readable `customer_name` to each order, then group by that name and sum the `amount` column, finally sorting descending for a "top spenders" style report.

## Scenario Questions

**Q: You merge two DataFrames on a `customer_id` column and the result has noticeably more rows than either input. What's likely going on?**
> A: This usually means the key column has duplicate values on one or both sides — if `customer_id` appears multiple times in either DataFrame (e.g., a customer has several orders), the merge produces one row for every combination of matching left/right rows, which can multiply the row count beyond either original table. I'd check for duplicate keys with `df["customer_id"].duplicated().sum()` on both sides to confirm before trusting the merged result.

**Q: A stakeholder wants "average order value per region, per month." How would you approach this in Pandas?**
> A: I'd group by both `region` and a month-derived column (extracting month from a date column, likely via `df["date"].dt.to_period("M")` or similar) in one `.groupby(["region", "month"])["order_value"].mean()` call — grouping by multiple columns at once, rather than looping over regions or months manually, gives the full breakdown in a single vectorized operation.

## "Gotcha" Questions

**Q: What's the bug in this code, and what actually happens?**
```python
df.drop(columns=["temp_column"])
print(df.columns)   # temp_column is still there!
```
> A: `.drop()` returns a *new* DataFrame by default rather than modifying `df` in place — the result of the drop was never captured, so the original `df` is unchanged. The fix is to reassign: `df = df.drop(columns=["temp_column"])`.

**Q: Why does this raise an error, and what's the fix?**
```python
df[df["age"] > 30 and df["department"] == "Engineering"]
```
> A: `and` expects a single `True`/`False`, but `df["age"] > 30` and `df["department"] == "Engineering"` are both entire boolean Series, not single values — this raises `ValueError: The truth value of a Series is ambiguous`. The fix is the element-wise `&` operator with parentheses around each condition: `df[(df["age"] > 30) & (df["department"] == "Engineering")]`.

## Quick-Fire Rapid Review

- Q: What does selecting a single column with single brackets return? → **a Series**
- Q: Is `.loc`'s slice end inclusive or exclusive? → **inclusive**
- Q: Is `.iloc`'s slice end inclusive or exclusive? → **exclusive**
- Q: Correct operator to combine DataFrame boolean conditions? → **`&` / `|`, not `and`/`or`**
- Q: Default `how` for `pd.merge()`? → **`"inner"`**
- Q: Which `how` guarantees every row from the left DataFrame survives? → **`"left"`**
- Q: What must you pass to `pd.concat()` to avoid duplicate index labels? → **`ignore_index=True`**
- Q: Why prefer vectorized ops over `.apply()`? → **`.apply()` runs a Python function per row, losing the C-level speed of vectorization**
