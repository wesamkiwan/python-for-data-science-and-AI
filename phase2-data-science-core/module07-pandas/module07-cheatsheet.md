# 📋 Module 07 Cheat Sheet: Pandas for Data Manipulation

Fast reference for Series/DataFrames, selection, column ops, groupby, and merging.

## Creating & Loading
```python
import pandas as pd

pd.Series([1, 2, 3], name="x")
pd.DataFrame({"col1": [...], "col2": [...]})

pd.read_csv("file.csv")
pd.read_json("file.json")
df.to_csv("out.csv", index=False)       # always pass index=False when saving
df.to_json("out.json", orient="records", indent=2)
```

## Inspecting (always run these first on new data)
```python
df.head(n)   df.tail(n)   df.shape   df.columns.tolist()
df.dtypes      df.info()      df.describe()
```

## Selecting
```python
df["col"]              # Series
df[["col1", "col2"]]      # DataFrame (note double brackets)

df.loc[row_label, col_label]      # label-based; slice END IS INCLUSIVE
df.iloc[row_pos, col_pos]            # position-based; slice end EXCLUSIVE (like Python)
```

## Filtering (boolean masks)
```python
df[df["col"] > x]
df[(df["col1"] > x) & (df["col2"] == y)]     # & / | only, parens required, NOT and/or
df[df["col"].isin([a, b, c])]
df.loc[condition, ["col1", "col2"]]                # filter rows + select columns in one step
```

## Column Operations
```python
df["new"] = df["a"] * df["b"]              # vectorized -- prefer this
df["new"] = df["a"].apply(lambda x: ...)      # custom row-by-row logic -- slower, last resort
df["new"] = np.where(condition, "yes", "no")     # vectorized conditional -- faster than apply

df = df.drop(columns=["col"])       # drop column(s) -- NOT in place by default
df = df.drop(index=[0])                # drop row(s) by label
df = df.rename(columns={"old": "new"})
```

## Sorting
```python
df.sort_values("col")                          # ascending
df.sort_values("col", ascending=False)            # descending
df.sort_values(["col1", "col2"])                     # multi-column
```

## Groupby (split-apply-combine)
```python
df.groupby("col")["target"].mean()
df.groupby("col").agg({"col_a": "mean", "col_b": "max"})
df.groupby("col")["target"].agg(["mean", "min", "max", "count"])
df.groupby(["col1", "col2"])["target"].sum()      # multi-column grouping
```

## Combining DataFrames
```python
pd.concat([df1, df2], ignore_index=True)       # stack rows -- always pass ignore_index=True

pd.merge(left, right, on="key", how="inner")     # SQL-style join
```

| `how` | Keeps |
|---|---|
| `"inner"` (default) | Rows matching in both |
| `"left"` | All left rows, matched data where available |
| `"right"` | All right rows, matched data where available |
| `"outer"` | All rows from both, matched where possible |

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Extra unnamed column after `to_csv`/`read_csv` round trip | Forgot `index=False` when saving | Always pass `index=False` unless you need the index preserved |
| `df["col"]` works but `df[["col"]]` behaves differently downstream | Single brackets → Series, double brackets → DataFrame | Use double brackets when a DataFrame is expected (e.g., multiple columns) |
| `.loc[0:2]` includes an "extra" row vs. expectation | `.loc` slicing is inclusive of the end label | Use `.iloc` if you want Python's normal exclusive-end slicing |
| `ValueError: truth value of a Series is ambiguous` | Used `and`/`or` on DataFrame conditions | Use `&`/`\|` with parentheses around each condition |
| Duplicate index labels after `pd.concat()` | Missing `ignore_index=True` | Always pass it when stacking rows |
| Unexpected `NaN` after a merge | Row had no match under the chosen `how` | Check `how`; inspect unmatched rows deliberately |
| `.apply()` feels slow on a large DataFrame | It runs a Python function per row, losing vectorization | Replace with vectorized arithmetic or `np.where()` |

## The "New Dataset" Workflow — do this every time
1. `pd.read_csv(...)` (or `read_json`) to load.
2. `df.head()`, `df.info()`, `df.shape` — always, before anything else.
3. Select/filter to the subset you need (`.loc`, boolean masks).
4. Derive any new columns with vectorized ops first; `.apply()` only if truly necessary.
5. `.groupby(...)` to summarize; `pd.merge(...)` to bring in other tables.
6. `.sort_values(...)` to present results in a meaningful order.
