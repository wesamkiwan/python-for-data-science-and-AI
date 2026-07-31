# Module 08c: String Cleaning & Outlier Detection

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [02-duplicates-and-dtypes.md](02-duplicates-and-dtypes.md)

## 🎯 Learning Objectives
- [ ] Clean messy text columns with the `.str` accessor
- [ ] Detect outliers using the IQR (interquartile range) method
- [ ] Detect outliers using the z-score method
- [ ] Decide what to do once an outlier is found

---

## Module Goal

Finish out the data-cleaning toolkit with two more extremely common real-world issues: inconsistent text formatting (extra whitespace, inconsistent casing, messy separators) and outliers (values so extreme they may be data-entry errors — or may be genuinely important signal).

## Why This Matters on the Job

`"New York"`, `" new york "`, and `"NEW YORK"` are the same city to a human, but three different strings to a computer — until you standardize them, a `.groupby("city")` will treat them as three separate groups, silently fragmenting your analysis. Outliers are just as consequential in the opposite direction: a single data-entry error (age `"999"` instead of `"99"`) can wildly skew an average, while a genuine outlier (a fraud case, a viral post) might be exactly the thing worth investigating rather than removing.

---

## String Cleaning with the `.str` Accessor

Pandas' `.str` accessor applies string operations to an entire column at once — vectorized, exactly like the arithmetic operations from Module 06/07.

```python
import pandas as pd

df = pd.DataFrame({"name": ["  Ada  ", "GRACE", "alan ", " Katherine"]})

print(df["name"].str.strip())         # remove leading/trailing whitespace
print(df["name"].str.lower())            # lowercase everything
print(df["name"].str.strip().str.title())   # chain methods: strip whitespace, THEN title-case
```
```
0          Ada
1        Grace
2         Alan
3    Katherine
Name: name, dtype: str
```

**How it works:** Every `.str` method mirrors Python's built-in string methods (`.strip()`, `.lower()`, `.upper()`, `.title()`, `.replace()`, etc.) from Module 01, but applies to *every value in the column* in one vectorized call, instead of needing a loop or `.apply()`.

### Common Cleaning Operations

```python
# Remove unwanted characters (e.g., standardizing phone number formats)
phones = pd.Series(["555-0100", "555.0101", "555 0102"])
print(phones.str.replace(r"[-. ]", "", regex=True))
```
```
0    5550100
1    5550101
2    5550102
Name: phone, dtype: str
```

```python
# Case-insensitive matching
emails = pd.Series(["ADA@Example.com", "grace@EXAMPLE.com"])
print(emails.str.lower())                             # standardize case
print(emails.str.contains("example", case=False))          # case-insensitive search
print(emails.str.split("@"))                                  # split into parts -- returns lists
```

💡 **Tip:** `case=False` is available on most `.str` search/match methods (`.contains()`, `.startswith()` doesn't have it, but you can `.str.lower()` first) — always consider whether a text comparison should be case-sensitive before writing it.

✅ **Best Practice:** Standardize categorical/text columns (`.str.strip().str.lower()`, or `.str.title()` for display) as an explicit cleaning step *before* any `.groupby()` or `.value_counts()` on them — otherwise `"USA"`, `"usa "`, and `"Usa"` silently become three separate groups.

🎯 **On the job:** This exact pattern is one of the most common causes of "why does this dataset have way more categories than it should" bugs — inconsistent capitalization/whitespace fragmenting what should be one category into several.

## Outlier Detection

An **outlier** is a data point far outside the normal range of the rest of the data. Outliers might be genuine errors (a typo: age `999`) or genuinely interesting extremes (a record-breaking sale) — detecting them is step one; deciding what to do about them is a separate judgment call.

### Method 1: IQR (Interquartile Range)

The **IQR** is the range between the 25th percentile (Q1) and 75th percentile (Q3) of the data — a measure of the "typical spread," robust to a few extreme values.

```python
import pandas as pd

data = pd.Series([10, 12, 11, 13, 12, 11, 100, 12, 13, 11])

q1 = data.quantile(0.25)
q3 = data.quantile(0.75)
iqr = q3 - q1

lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

outliers = data[(data < lower_bound) | (data > upper_bound)]
print(outliers)   # 6    100
```

**How it works:** The `1.5 * IQR` rule is a widely-used convention (it's also what generates the "whiskers" on a box plot, which you'll create in Module 09) — any value further than 1.5 times the IQR beyond Q1 or Q3 is flagged as a statistical outlier. `100` here is dramatically outside the rest of the data (clustered around 10-13), so it's correctly flagged.

### Method 2: Z-Score

The **z-score** measures how many standard deviations a value is from the mean. A common rule of thumb: flag values with an absolute z-score greater than 2 or 3.

```python
mean = data.mean()
std = data.std()

z_scores = (data - mean) / std
print(z_scores)

outliers = data[z_scores.abs() > 2]
print(outliers)   # 6    100
```

**How it works:** `(data - mean) / std` is vectorized across the whole Series — every value's distance from the mean, measured in standard deviations. A z-score of `2.84` (like `100` gets here) means that value is nearly 3 standard deviations from the average, a strong signal it's unusual.

| Method | Best when... |
|---|---|
| IQR | Data isn't normally distributed, or you want a method robust to the outliers themselves affecting the calculation |
| Z-score | Data is roughly normally distributed (bell-curve shaped) |

⚠️ **Warning:** The z-score method uses the mean and standard deviation — both of which are themselves distorted by extreme outliers. In a small dataset with a very extreme value (like this example), the outlier inflates the standard deviation, which can make *itself* look less extreme than it should. IQR (based on percentiles, not the mean) is generally more robust for this reason.

## What to Do About an Outlier

Finding an outlier is the easy part — deciding what to do is where judgment matters:

| Situation | Reasonable response |
|---|---|
| Clearly a data-entry error (age = 999) | Correct it if the true value is knowable, otherwise treat as missing (`NaN`) and handle per Module 08a |
| A rare-but-real extreme event (a huge but legitimate sale) | Keep it — but consider analyzing it separately, since it may skew averages |
| Unsure whether it's real or an error | Investigate further before deciding — don't delete data based on a guess |

✅ **Best Practice:** Never silently drop outliers without a documented reason — "I removed 3 rows because they were statistical outliers per the IQR method" is a defensible, professional statement; silently deleting inconvenient data points is not.

---

## Hands-On Exercise

**Task:** Write `string_and_outlier_practice.py` using this DataFrame:
```python
import pandas as pd

df = pd.DataFrame({
    "city": ["  New York", "los angeles ", "NEW YORK", "Chicago", " Los Angeles"],
    "revenue": [5000, 5200, 4800, 5100, 250000]
})
```
1. Clean the `city` column: strip whitespace and standardize to title case, then print the cleaned column's unique values with `.unique()` (should reveal only 3 true distinct cities, not 5).
2. Use the IQR method to detect any outliers in `revenue`.
3. Print the DataFrame with the outlier row(s) excluded, and separately print just the outlier row(s) for manual review.

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd

df = pd.DataFrame({
    "city": ["  New York", "los angeles ", "NEW YORK", "Chicago", " Los Angeles"],
    "revenue": [5000, 5200, 4800, 5100, 250000]
})

df["city"] = df["city"].str.strip().str.title()
print(df["city"].unique())   # 3 distinct values: New York, Los Angeles, Chicago (not 5!)

q1 = df["revenue"].quantile(0.25)
q3 = df["revenue"].quantile(0.75)
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr

is_outlier = (df["revenue"] < lower_bound) | (df["revenue"] > upper_bound)

print("Cleaned data (outliers excluded):")
print(df[~is_outlier])

print("Outliers for manual review:")
print(df[is_outlier])
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Grouping/counting a text column before standardizing case/whitespace | `.str.strip().str.lower()` (or `.title()`) first |
| Assuming `.str.contains()` is case-insensitive by default | Pass `case=False` explicitly when needed |
| Deleting outliers automatically without investigation | Investigate first; document the decision either way |
| Using z-score on data with extreme outliers already present | Consider IQR instead — it's more robust to the outliers distorting the mean/std |
| Forgetting `~` to invert a boolean mask (get the "not outlier" rows) | `df[~is_outlier]` selects everything the mask does NOT flag |

---

## ✅ Module 08 Completion Checklist
- [ ] Can clean text columns with `.str.strip()`, `.str.lower()`, `.str.replace()`, etc.
- [ ] Can detect outliers with the IQR method
- [ ] Can detect outliers with the z-score method
- [ ] Understand the difference between the two methods and when each fits better
- [ ] Can reason about what to do once an outlier is found, rather than deleting by reflex
- [ ] Completed the `string_and_outlier_practice.py` exercise
- [ ] Reviewed [`module08-cheatsheet.md`](module08-cheatsheet.md)
- [ ] Reviewed [`module08-interview.md`](module08-interview.md)
- [ ] Browsed [`module08-references.md`](module08-references.md)

**Next Step:** Module 09 — Data Visualization (`phase2-data-science-core/module09-data-visualization/`)
