# Module 08b: Duplicates & Fixing Data Types

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [01-missing-data.md](01-missing-data.md)

## 🎯 Learning Objectives
- [ ] Detect and remove duplicate rows with `.duplicated()` and `.drop_duplicates()`
- [ ] Convert column types with `.astype()`
- [ ] Safely convert messy numeric data with `pd.to_numeric(errors="coerce")`
- [ ] Convert text to real dates with `pd.to_datetime()`

---

## Module Goal

Continue building your data-cleaning toolkit: finding and removing duplicate records, and fixing columns that loaded with the wrong data type — both extremely common issues the moment real data comes from an external source (a CSV export, a form submission, a scraped webpage).

## Why This Matters on the Job

Duplicate records silently inflate totals and averages — "total revenue" is simply wrong if the same order got counted twice. Wrong data types are just as dangerous but sneakier: a "date" column that loaded as plain text can't be sorted chronologically or have days/months extracted from it; a "price" column with a stray `"N/A"` forces the *entire* column to load as text instead of numbers, breaking any math you try to do on it. Both are exactly the kind of "boring but critical" checks that separate a trustworthy analysis from a broken one.

---

## Detecting and Removing Duplicates

```python
import pandas as pd

df = pd.DataFrame({
    "name": ["Ada", "Grace", "Ada", "Alan", "Grace"],
    "department": ["Eng", "Eng", "Eng", "Research", "Eng"]
})

print(df.duplicated())        # True for each row that's an EXACT repeat of an earlier row
print(df.duplicated().sum())    # total count of duplicate rows
```
```
0    False
1    False
2     True
3    False
4     True
dtype: bool
```

**How it works:** `.duplicated()` marks a row `True` if it's identical to a row that appeared *earlier* in the DataFrame — the first occurrence is always `False`, only later repeats are flagged.

```python
print(df.drop_duplicates())                        # keeps first occurrence, drops later exact-duplicate rows
print(df.drop_duplicates(subset=["name"]))             # drops rows with a duplicate NAME, ignoring other columns
print(df.drop_duplicates(subset=["name"], keep="last"))   # keep the LAST occurrence instead of the first
```

**How it works:** Without `subset`, a row must match *every* column exactly to count as a duplicate. `subset=["name"]` instead considers only the `name` column — useful when "duplicate" means "same person," even if other columns (like a timestamp) legitimately differ between their rows.

✅ **Best Practice:** Always decide explicitly what "duplicate" means for your specific dataset — an exact full-row match, or a match on just a business-meaningful key like `customer_id` or `order_id` — rather than assuming the default behavior is automatically correct.

🎯 **On the job:** A very common real scenario: an API call that gets accidentally triggered twice inserts the same order into your data twice. `df.drop_duplicates(subset=["order_id"])` is the one-line fix that keeps your totals honest.

## Fixing Data Types

### `.astype()`: Direct Conversion

```python
df = pd.DataFrame({"x": ["1", "2", "3"]})
print(df.dtypes)          # x    str

df["x"] = df["x"].astype(int)
print(df.dtypes)             # x    int64
```

⚠️ **Warning:** `.astype()` raises an error immediately if *any* value can't convert — `pd.DataFrame({"x": ["1", "2", "bad"]})["x"].astype(int)` fails with `ValueError: invalid literal for int()`. It's an all-or-nothing conversion, which is exactly why real, messy data usually needs the next tool instead.

### `pd.to_numeric(errors="coerce")`: Safe Numeric Conversion

```python
messy = pd.Series(["25", "30", "N/A", "45"])
converted = pd.to_numeric(messy, errors="coerce")
print(converted)
```
```
0    25.0
1    30.0
2     NaN
3    45.0
dtype: float64
```

**How it works:** `errors="coerce"` tells Pandas "convert what you can, and turn anything that fails into `NaN`" instead of crashing the whole operation. This is precisely the "batch-processing-without-crashing" idea from Module 02/04, now built into Pandas as a single argument — the messy `"N/A"` becomes a normal, detectable missing value you can then handle with everything from the previous lesson (`.isna()`, `.fillna()`, `.dropna()`).

✅ **Best Practice:** `errors="coerce"` is almost always the right default choice for real-world numeric columns — you get a usable numeric column *and* an honest, inspectable record of exactly which values failed to convert (they become `NaN`, catchable with `.isna()`).

### `pd.to_datetime()`: Converting Text to Real Dates

```python
dates = pd.Series(["2024-01-15", "2024-02-20", "invalid"])
converted_dates = pd.to_datetime(dates, errors="coerce")
print(converted_dates)
```
```
0   2024-01-15
1   2024-02-20
2          NaT
dtype: datetime64[us]
```

**How it works:** Just like `to_numeric`, `errors="coerce"` turns unparseable dates into a special missing-date marker, `NaT` ("Not a Time") — Pandas' date-flavored equivalent of `NaN`. Once a column is a real datetime type (not just text that *looks* like a date), you unlock powerful operations:

```python
df = pd.DataFrame({"signup_date": pd.to_datetime(["2024-01-15", "2024-03-22", "2024-06-10"])})

print(df["signup_date"].dt.year)          # extract just the year
print(df["signup_date"].dt.month)           # extract just the month
print(df["signup_date"].dt.day_name())         # "Monday", "Tuesday", etc.
print(df["signup_date"] > "2024-02-01")           # date comparisons work correctly, chronologically
```

⚠️ **Warning:** A date column loaded from CSV without explicit conversion is just *text that happens to look like a date* — sorting it, comparing it, or extracting the month from it either fails outright or (worse) silently gives wrong results, since text sorts alphabetically, not chronologically (e.g., `"2024-12-01"` would sort *before* `"2025-01-01"` correctly, but `"9/1/2024"` would sort *before* `"10/1/2024"` incorrectly as plain text). ✅ **Best Practice:** always convert date-like columns with `pd.to_datetime()` immediately after loading, either via `pd.read_csv(..., parse_dates=["date_column"])` or a follow-up `pd.to_datetime()` call.

---

## Hands-On Exercise

**Task:** Write `cleaning_practice.py` using this DataFrame:
```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [1, 2, 3, 3, 4],
    "customer": ["Ada", "Grace", "Alan", "Alan", "Katherine"],
    "amount": ["100", "250", "N/A", "N/A", "75"],
    "order_date": ["2024-01-10", "2024-01-15", "2024-02-01", "2024-02-01", "bad-date"]
})
```
1. Detect and remove any fully duplicate rows (note: row `order_id=3` appears twice, identically).
2. Convert `amount` to numeric using `errors="coerce"`, then check how many values became missing.
3. Convert `order_date` to a real datetime column using `errors="coerce"`, then check how many became missing.
4. After cleaning, print the DataFrame's `.dtypes` to confirm `amount` is now numeric and `order_date` is now a datetime type.

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd

orders = pd.DataFrame({
    "order_id": [1, 2, 3, 3, 4],
    "customer": ["Ada", "Grace", "Alan", "Alan", "Katherine"],
    "amount": ["100", "250", "N/A", "N/A", "75"],
    "order_date": ["2024-01-10", "2024-01-15", "2024-02-01", "2024-02-01", "bad-date"]
})

print(f"Duplicate rows: {orders.duplicated().sum()}")
orders = orders.drop_duplicates()

orders["amount"] = pd.to_numeric(orders["amount"], errors="coerce")
print(f"Missing amounts after conversion: {orders['amount'].isna().sum()}")

orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
print(f"Missing dates after conversion: {orders['order_date'].isna().sum()}")

print(orders)
print(orders.dtypes)
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Assuming "duplicate" always means "identical in every column" | Use `subset=[...]` when duplicates should be judged by a business key |
| Using `.astype()` on messy data that might fail to convert | Use `pd.to_numeric()`/`pd.to_datetime()` with `errors="coerce"` instead |
| Treating a date column as text without converting it | Always `pd.to_datetime()` date-like columns before sorting/comparing/extracting parts |
| Not checking how many values became `NaN`/`NaT` after a coerced conversion | Always follow up with `.isna().sum()` to see how much data the coercion actually caught |
| Forgetting `.drop_duplicates()` doesn't modify in place | Reassign: `df = df.drop_duplicates()` |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Can detect and remove duplicate rows, with and without `subset`
- [ ] Can convert types with `.astype()` and understand its all-or-nothing failure mode
- [ ] Can safely convert messy numeric data with `pd.to_numeric(errors="coerce")`
- [ ] Can convert text to real dates with `pd.to_datetime(errors="coerce")` and use `.dt` accessors
- [ ] Completed the `cleaning_practice.py` exercise

**Next:** Continue to [`03-string-cleaning-and-outliers.md`](03-string-cleaning-and-outliers.md)
