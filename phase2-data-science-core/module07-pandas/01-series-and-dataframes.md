# Module 07a: Series & DataFrames — Pandas Fundamentals

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [Module 06 — NumPy Fundamentals](../module06-numpy/03-aggregation-and-reshaping.md)

## 🎯 Learning Objectives
- [ ] Explain what Pandas is and how Series/DataFrames relate to NumPy arrays
- [ ] Create a `Series` and a `DataFrame` from scratch
- [ ] Read data from CSV and JSON into a DataFrame
- [ ] Inspect a DataFrame with `.head()`, `.tail()`, `.info()`, `.describe()`, `.shape`, `.dtypes`

---

## Module Goal

Meet **Pandas**, the single most important library in the data scientist's toolkit — a library for working with labeled, tabular data (think: a spreadsheet, but programmable). You'll learn its two core data structures, `Series` and `DataFrame`, and how to load real data into them from files.

## Why This Matters on the Job

Pandas is how virtually every data scientist spends the first (and often largest) part of any project: loading, inspecting, and understanding a dataset before doing anything else with it. `pd.read_csv()` is very likely the single most-run line of code in this entire field. Every skill from Module 06 (NumPy) directly transfers here — Pandas is built *on top of* NumPy, and a DataFrame's columns are, underneath, NumPy arrays with labels attached.

---

## What Is Pandas?

**Pandas** ("Panel Data") adds labeled rows and columns on top of NumPy's fast array machinery, plus a huge set of tools for loading, cleaning, filtering, and summarizing data — everything a spreadsheet does, but scriptable, reproducible, and able to handle millions of rows.

```bash
pip install pandas
```

```python
import pandas as pd   # 'pd' is the universal, expected alias -- always use it
```

## `Series`: A Single Labeled Column

A **Series** is a one-dimensional, labeled array — like a single column of a spreadsheet, or a Python `dict` with guaranteed order and vectorized (NumPy-powered) operations.

```python
import pandas as pd

scores = pd.Series([10, 20, 30, 40], name="scores")
print(scores)
```
```
0    10
1    20
2    30
3    40
Name: scores, dtype: int64
```

**How it works:** The left column is the **index** (labels for each value — defaults to `0, 1, 2, ...`), the right column is the data. `.index` and `.values` expose these separately:

```python
print(scores.index)     # RangeIndex(start=0, stop=4, step=1)
print(scores.values)       # [10 20 30 40] -- a plain NumPy array underneath!
```

You can also build a Series from a `dict`, using the keys as the index:

```python
population = pd.Series({"London": 8_982_000, "Paris": 2_161_000, "Tokyo": 13_960_000})
print(population)
```
```
London     8982000
Paris      2161000
Tokyo     13960000
dtype: int64
```

## `DataFrame`: A Full Labeled Table

A **DataFrame** is a 2D table — a collection of Series sharing the same index, each one a column.

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ada", "Grace", "Alan", "Katherine"],
    "age": [36, 85, 41, 101],
    "department": ["Engineering", "Engineering", "Research", "Research"]
})
print(df)
```
```
        name  age   department
0        Ada   36  Engineering
1      Grace   85  Engineering
2       Alan   41     Research
3  Katherine  101     Research
```

**How it works:** Each key in the dictionary becomes a column name; each value (a list) becomes that column's data, all aligned by position into rows. Every column is itself a Series — `df["name"]` returns exactly the same kind of object you saw above.

💡 **Tip (pandas 3.0+):** In recent Pandas versions, plain text columns get a dedicated `str` dtype by default (shown as `dtype: str`) rather than the generic `object` dtype older Pandas versions used. You'll still see `object` referenced constantly in older tutorials and Stack Overflow answers — for the purposes of this course, treat them as meaning the same thing: "this column holds text."

## Reading Data from Files

In practice, you'll almost never type out a DataFrame's data by hand — you'll load it from a file.

```python
# Reading
df = pd.read_csv("employees.csv")
df = pd.read_json("employees.json")

# Writing (the reverse) -- useful for saving intermediate results
df.to_csv("output.csv", index=False)
df.to_json("output.json", orient="records", indent=2)
```

**How it works:** `pd.read_csv()` replaces the entire manual `csv.DictReader` loop-and-type-cast process from Module 04 with one line — it automatically infers column types (numbers become `int64`/`float64`, not strings), handles headers, and returns a ready-to-use DataFrame.

⚠️ **Warning:** `index=False` in `.to_csv()` is important — without it, Pandas writes its own row-number index as an extra unwanted column in the file. ✅ **Best Practice:** almost always pass `index=False` when saving to CSV unless you specifically want that index preserved.

🎯 **On the job:** `pd.read_csv()` accepts dozens of useful parameters you'll grow into over time — `sep=";"` for non-comma delimiters, `parse_dates=["date_column"]` to auto-convert date columns, `na_values=["N/A", "missing"]` to recognize custom missing-value markers, and more (Module 08 covers messy real-world data in depth).

## Inspecting a DataFrame

Before doing anything else with a new dataset, always look at it first:

```python
df.head()          # first 5 rows (or df.head(2) for a specific number)
df.tail(2)            # last 2 rows
df.shape                # (rows, columns) tuple, e.g. (4, 3)
df.columns.tolist()        # list of column names
df.dtypes                    # data type of each column
df.info()                       # column names, non-null counts, dtypes, memory usage -- all at once
df.describe()                      # summary statistics (mean, std, min/max, quartiles) for numeric columns
```

```python
print(df.info())
```
```
<class 'pandas.DataFrame'>
RangeIndex: 4 entries, 0 to 3
Data columns (total 3 columns):
 #   Column      Non-Null Count  Dtype
---  ------      --------------  -----
 0   name        4 non-null      str
 1   age         4 non-null      int64
 2   department  4 non-null      str
dtypes: int64(1), str(2)
memory usage: 287.0 bytes
```

```python
print(df.describe())
```
```
             age
count    4.00000
mean    65.75000
std     32.20119
min     36.00000
25%     39.75000
50%     63.00000
75%     89.00000
max    101.00000
```

**How it works:** `.info()` is your first stop on *any* new dataset — it instantly reveals how many rows exist, which columns have missing values (a `Non-Null Count` lower than the total row count means missing data — the focus of Module 08), and whether a column's inferred type makes sense (e.g., a date column that loaded as text instead of a date needs fixing). `.describe()` only summarizes *numeric* columns by default, giving you an immediate sense of each column's range and distribution.

✅ **Best Practice:** Run `df.head()`, `df.info()`, and `df.shape` as the very first three commands on any dataset you load, before writing a single line of analysis — this "first look" habit catches most loading mistakes (wrong file, wrong delimiter, unexpected missing data) immediately.

---

## Hands-On Exercise

**Task:** Write `dataframe_basics.py` that:
1. Creates a DataFrame `products` with columns `name`, `price`, and `category` for at least 5 products of your choice.
2. Saves it to `products.csv` (without the extra index column), then reads it back into a new variable.
3. Prints `.head(3)`, `.info()`, `.describe()`, and `.shape` on the loaded DataFrame.
4. Creates a `Series` of just the `price` column, and prints its `.mean()` and `.max()` (these Series methods behave exactly like the NumPy aggregation methods from Module 06, since a Series is built on a NumPy array underneath).

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd

products = pd.DataFrame({
    "name": ["Laptop", "Mouse", "Keyboard", "Monitor", "Webcam"],
    "price": [999.99, 25.50, 45.00, 249.99, 60.00],
    "category": ["Electronics", "Accessories", "Accessories", "Electronics", "Accessories"]
})

products.to_csv("products.csv", index=False)
loaded_products = pd.read_csv("products.csv")

print(loaded_products.head(3))
print(loaded_products.info())
print(loaded_products.describe())
print(loaded_products.shape)

prices = loaded_products["price"]
print(f"Average price: {prices.mean()}")
print(f"Max price: {prices.max()}")
```

**Expected output (abridged):** `.head(3)` shows the first three products, `.shape` is `(5, 3)`, and the average/max price are computed correctly from the `price` column.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Forgetting `index=False` when saving to CSV | Pandas otherwise writes an unwanted extra index column |
| Jumping straight into analysis without inspecting the data first | Always run `.head()`, `.info()`, `.shape` immediately after loading |
| Assuming `.describe()` covers every column | It only summarizes numeric columns by default |
| Confusing a Series (`df["col"]`) with a one-column DataFrame (`df[["col"]]`) | Single brackets return a Series; double brackets return a DataFrame |
| Not using the conventional `pd` alias | Always `import pandas as pd` — it's a near-universal convention |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand the relationship between Pandas and NumPy
- [ ] Can create a Series and a DataFrame from scratch
- [ ] Can read/write CSV and JSON with `pd.read_csv`/`to_csv`, `pd.read_json`/`to_json`
- [ ] Can inspect a DataFrame with `.head()`, `.tail()`, `.shape`, `.dtypes`, `.info()`, `.describe()`
- [ ] Completed the `dataframe_basics.py` exercise

**Next:** Continue to [`02-selection-and-filtering.md`](02-selection-and-filtering.md)
