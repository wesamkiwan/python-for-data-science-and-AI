# Module 07d: `groupby()` & Merging DataFrames

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [03-column-operations-and-sorting.md](03-column-operations-and-sorting.md)

## 🎯 Learning Objectives
- [ ] Explain the "split-apply-combine" pattern behind `.groupby()`
- [ ] Compute grouped aggregations, including multiple aggregations at once
- [ ] Combine DataFrames with `pd.concat()`
- [ ] Combine DataFrames with `pd.merge()`, and explain the different join types

---

## Module Goal

Learn Pandas' two most powerful data-combination tools: **`.groupby()`**, for summarizing data by category ("average salary *per department*"), and **merging**, for combining data spread across multiple tables — exactly like a `JOIN` in SQL (which you'll formalize further in Module 11).

## Why This Matters on the Job

Almost every business question is a groupby in disguise: "revenue by region," "average order value by customer segment," "signups per day." And real-world data is almost never in one single table — customer info lives in one table, orders in another, products in a third — so merging them together correctly is a daily, essential skill. Both of these concepts directly extend ideas you've already learned: `.groupby()` builds on Module 06's `axis`-based aggregation intuition, and merging formalizes the SQL-style joins you'll see by name in Module 11.

---

## `.groupby()`: Split-Apply-Combine

**Split-apply-combine** is the mental model behind every groupby: **split** the data into groups based on a column's values, **apply** an aggregation to each group independently, then **combine** the results back into one summary.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ada", "Grace", "Alan", "Katherine", "Linus"],
    "department": ["Engineering", "Engineering", "Research", "Research", "Engineering"],
    "salary": [95000, 120000, 88000, 130000, 91000],
    "age": [36, 85, 41, 101, 33]
})

print(df.groupby("department")["salary"].mean())
```
```
department
Engineering    102000.0
Research       109000.0
Name: salary, dtype: float64
```

**How it works:** `df.groupby("department")` **splits** the DataFrame into one group per unique `department` value (`"Engineering"`, `"Research"`). `["salary"].mean()` **applies** the mean to each group's `salary` column independently, then **combines** the two results into a single Series, indexed by department.

💡 **Tip:** This is the exact same idea as Module 06's `matrix.mean(axis=0)` — collapsing many values down to one summary per category — just grouped by a labeled column's *values* instead of by a fixed array dimension.

### Multiple Aggregations at Once with `.agg()`

```python
print(df.groupby("department").agg({"salary": "mean", "age": "max"}))
```
```
             salary  age
department
Engineering  102000.0   85
Research     109000.0  101
```

**How it works:** `.agg({"column": "function", ...})` lets you apply a *different* aggregation to each column in one call — here, the mean salary and the max age, per department.

You can also compute multiple statistics on the *same* column:

```python
print(df.groupby("department")["salary"].agg(["mean", "min", "max", "count"]))
```
```
                 mean    min     max  count
department
Engineering  102000.0  91000  120000      3
Research     109000.0  88000  130000      2
```

🎯 **On the job:** `.groupby(...).agg(...)` is the single most common way to produce a summary report — "average, min, max, and count per category" is one of the most frequently requested views of any dataset, in any company.

### Grouping by Multiple Columns

```python
df["seniority"] = ["Junior", "Senior", "Junior", "Senior", "Junior"]
print(df.groupby(["department", "seniority"])["salary"].mean())
```
```
department   seniority
Engineering  Junior        93000.0
             Senior       120000.0
Research     Junior        88000.0
             Senior       130000.0
Name: salary, dtype: float64
```

**How it works:** Passing a list groups by the unique *combination* of both columns — one result per (department, seniority) pair.

## Combining DataFrames with `pd.concat()`

`pd.concat()` stacks DataFrames together — most commonly, adding more rows (e.g., combining January's and February's data into one DataFrame).

```python
january = pd.DataFrame({"name": ["Ada", "Grace"], "sales": [100, 150]})
february = pd.DataFrame({"name": ["Ada", "Grace"], "sales": [120, 130]})

combined = pd.concat([january, february], ignore_index=True)
print(combined)
```
```
    name  sales
0    Ada    100
1  Grace    150
2    Ada    120
3  Grace    130
```

⚠️ **Warning:** Without `ignore_index=True`, the combined DataFrame keeps each original DataFrame's index, resulting in *duplicate* index labels (`0, 1, 0, 1`) — usually not what you want. ✅ **Best Practice:** pass `ignore_index=True` whenever concatenating row-wise, unless you specifically need to preserve the original indices.

## Combining DataFrames with `pd.merge()`

`pd.merge()` combines DataFrames *side by side*, matching rows based on a shared key column — exactly like a SQL `JOIN`.

```python
employees = pd.DataFrame({
    "name": ["Ada", "Grace", "Alan"],
    "department": ["Engineering", "Engineering", "Research"]
})

managers = pd.DataFrame({
    "department": ["Engineering", "Research", "Sales"],
    "manager": ["Sam", "Priya", "Jordan"]
})

merged = pd.merge(employees, managers, on="department", how="left")
print(merged)
```
```
    name   department manager
0    Ada  Engineering     Sam
1  Grace  Engineering     Sam
2   Alan     Research   Priya
```

**How it works:** `on="department"` tells Pandas to match rows where both DataFrames' `department` values are equal. `how="left"` keeps every row from the *left* DataFrame (`employees`), attaching matching data from `managers` wherever a match exists.

### Join Types (`how=`)

| `how` | Keeps |
|---|---|
| `"inner"` (default) | Only rows with a match in **both** DataFrames |
| `"left"` | **All** rows from the left DataFrame, matched data where available (else `NaN`) |
| `"right"` | **All** rows from the right DataFrame, matched data where available (else `NaN`) |
| `"outer"` | **All** rows from **both** DataFrames, matched where possible (else `NaN`) |

```python
# "Sales" (in managers) has no matching employees -- doesn't appear with how="left"
# Switching to how="outer" would include it, with employee columns as NaN:
print(pd.merge(employees, managers, on="department", how="outer"))
```
```
    name   department manager
0    Ada  Engineering     Sam
1  Grace  Engineering     Sam
2   Alan     Research   Priya
3    NaN        Sales  Jordan
```

💡 **Tip:** `"inner"` is the default and the most common choice — "only show me records that exist in both tables." Reach for `"left"` when you want to keep every record from your primary table even if there's no match (e.g., "every employee, plus their manager if we have one on file").

🎯 **On the job:** This is functionally identical to a SQL `JOIN` — Module 11 (SQL) will feel highly familiar once this concept is solid, since the underlying logic (`inner`/`left`/`right`/`outer`) is exactly the same, just expressed in a different syntax.

---

## Hands-On Exercise

**Task:** Write `groupby_merge_practice.py` using these DataFrames:
```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5, 6],
    "customer_id": [101, 102, 101, 103, 102, 101],
    "amount": [50.0, 75.0, 30.0, 120.0, 60.0, 45.0]
})

customers = pd.DataFrame({
    "customer_id": [101, 102, 103, 104],
    "customer_name": ["Ada", "Grace", "Alan", "Katherine"]
})
```
1. Group `orders` by `customer_id` and compute the total (`sum`) and count (`count`) of `amount` per customer.
2. Merge `orders` with `customers` (on `customer_id`) so every order shows the customer's name, using an appropriate `how` (every order should have a matching customer — decide if `inner` or `left` matters here, and why).
3. From the merged result, group by `customer_name` and print the total amount spent per named customer, sorted highest to lowest.
4. Merge `customers` with `orders` using `how="left"` and explain (as a comment) what happens to `"Katherine"` (customer_id 104), who has no orders.

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [1, 2, 3, 4, 5, 6],
    "customer_id": [101, 102, 101, 103, 102, 101],
    "amount": [50.0, 75.0, 30.0, 120.0, 60.0, 45.0]
})

customers = pd.DataFrame({
    "customer_id": [101, 102, 103, 104],
    "customer_name": ["Ada", "Grace", "Alan", "Katherine"]
})

print(orders.groupby("customer_id")["amount"].agg(["sum", "count"]))

# Since every order's customer_id exists in `customers`, "inner" and "left" give
# the same result here -- "left" is still the safer/more explicit choice, since
# it makes clear we intend to keep every order regardless of match.
merged = pd.merge(orders, customers, on="customer_id", how="left")
print(merged)

per_customer = merged.groupby("customer_name")["amount"].sum().sort_values(ascending=False)
print(per_customer)

# Katherine (customer_id 104) has no matching orders. With how="left" on
# customers (left) merged with orders (right), her row is KEPT, with
# order_id/amount filled in as NaN, since "left" preserves every row from
# the left DataFrame (customers) regardless of a match.
all_customers = pd.merge(customers, orders, on="customer_id", how="left")
print(all_customers)
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Forgetting `ignore_index=True` in `pd.concat()` | Duplicate index labels result — pass it whenever stacking rows |
| Using the wrong `how` in a merge | Think about which side's rows you need to guarantee are kept |
| Assuming a merge preserves row count | A merge can produce more or fewer rows than either input, depending on matches and `how` |
| Not checking for unexpected `NaN` after a merge | `NaN` in a merged result usually signals a missing match — inspect it, don't ignore it |
| Grouping by a column, then forgetting to select which column(s) to aggregate | `df.groupby("col")` alone is inert — chain `["target_col"].agg(...)` or `.agg({...})` |

---

## ✅ Module 07 Completion Checklist
- [ ] Understand split-apply-combine and can use `.groupby()` with `.mean()`/`.agg()`
- [ ] Can group by multiple columns
- [ ] Can combine DataFrames row-wise with `pd.concat()`
- [ ] Can merge DataFrames with `pd.merge()` and choose the correct `how`
- [ ] Understand the difference between inner/left/right/outer joins
- [ ] Completed the `groupby_merge_practice.py` exercise
- [ ] Reviewed [`module07-cheatsheet.md`](module07-cheatsheet.md)
- [ ] Reviewed [`module07-interview.md`](module07-interview.md)
- [ ] Browsed [`module07-references.md`](module07-references.md)

**Next Step:** Module 08 — Data Cleaning & Wrangling (`phase2-data-science-core/module08-data-cleaning/`)
