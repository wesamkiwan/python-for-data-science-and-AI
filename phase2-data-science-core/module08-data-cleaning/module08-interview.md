# 🎤 Module 08 Interview Prep: Data Cleaning & Wrangling

## Conceptual Questions

### 🟢 Beginner

**Q: Why can't you check for missing values with `df["col"] == np.nan`?**
> A: `NaN` is defined by the IEEE floating-point standard to never equal anything, including another `NaN` — so this comparison always evaluates to `False`, even on rows that genuinely contain `NaN`. Pandas provides `.isna()` (and its inverse `.notna()`) specifically to check for missingness correctly.

**Q: What's the difference between `.dropna()` and `.fillna()`, and when would you choose one over the other?**
> A: `.dropna()` removes rows (or columns) containing missing values entirely, while `.fillna()` replaces missing values with a substitute (a fixed value, a computed statistic, or a per-column strategy). I'd lean toward `.dropna()` when missing data is rare and dropping it won't meaningfully bias the analysis; I'd lean toward `.fillna()` when there's a reasonable substitute value and I want to preserve as much of the dataset as possible, especially if the missing rows are otherwise valuable.

**Q: What does `pd.to_numeric(col, errors="coerce")` do differently from `col.astype(int)`?**
> A: `.astype(int)` requires every value to convert successfully — a single bad value (like `"N/A"`) raises an exception and stops the whole operation. `pd.to_numeric(col, errors="coerce")` converts what it can and turns anything that fails into `NaN` instead of crashing, which is almost always the more practical choice for real-world data that has occasional bad values mixed in with good ones.

### 🟡 Intermediate

**Q: How would you decide whether to use the mean or the median to fill missing values in a numeric column?**
> A: I'd look at the column's distribution first. If it's roughly symmetric with no major outliers, the mean is a reasonable, standard choice. If the column has significant outliers or a skewed distribution (e.g., income data, where a few very high earners pull the mean upward), the median is more representative of a "typical" value, since it isn't distorted by extreme values the way the mean is.

**Q: Why is a date column that "looks correct" when printed still potentially a problem?**
> A: If it loaded as plain text (dtype `object`/`str`) rather than an actual datetime type, sorting and comparisons happen alphabetically, not chronologically — this can silently produce wrong results depending on the date format (e.g., `"9/1/2024"` vs. `"10/1/2024"` sorting incorrectly as text), and operations like extracting the month or day of week simply aren't available at all. Converting explicitly with `pd.to_datetime()` (or `parse_dates=` in `read_csv`) is necessary before trusting any date-based logic on it.

**Q: Why might the z-score method be less reliable than IQR for detecting outliers in a dataset that already contains a significant outlier?**
> A: The z-score calculation uses the mean and standard deviation, both of which are themselves pulled/inflated by extreme values — a very large outlier can inflate the standard deviation enough that the outlier's own z-score no longer looks as extreme, potentially masking it. The IQR method is based on percentiles (Q1/Q3), which are far more resistant to a small number of extreme values, making it generally the more robust choice when you're not sure the data is "clean" going in.

## Practical/Coding Questions

**Q: Given a DataFrame with a `revenue` column stored as strings (some containing `"$"` and commas, like `"$1,200"`), write code to convert it to a clean numeric column.**
```python
import pandas as pd

df = pd.DataFrame({"revenue": ["$1,200", "$950.50", "N/A", "$2,300"]})

cleaned = df["revenue"].str.replace(r"[$,]", "", regex=True)
df["revenue"] = pd.to_numeric(cleaned, errors="coerce")
print(df)
```
> Explanation: `.str.replace()` with a regex strips out the `$` and `,` characters that would otherwise block numeric conversion, and `pd.to_numeric(errors="coerce")` then safely converts what's left, turning the still-invalid `"N/A"` into `NaN` rather than crashing.

**Q: Write code that removes duplicate customer records, keeping only the most recent one, given a `last_updated` date column.**
```python
import pandas as pd

df = df.sort_values("last_updated").drop_duplicates(subset=["customer_id"], keep="last")
```
> Explanation: sorting by `last_updated` ascending first, then `drop_duplicates(keep="last")`, guarantees that for each `customer_id`, the row that survives is the one with the latest `last_updated` value.

## Scenario Questions

**Q: You're analyzing sales data and one region's average order value is 10x every other region's. How would you investigate?**
> A: First, I'd check whether it's a small handful of extreme values (a data-entry error, or a few legitimately huge orders) rather than a genuine shift across the whole region — using the IQR or z-score method on that region's order values specifically. If it's one or two outlier rows, I'd look for signs of a data-entry mistake (an extra zero, a currency mismatch) before deciding whether to correct, exclude, or keep them; if it's a broad, consistent pattern across many orders, it's more likely a real business signal (e.g., that region sells enterprise contracts) rather than an error to "clean."

**Q: A teammate's analysis of a "unique customers" count came out much higher than expected. What would you check?**
> A: The first thing I'd check is whether the customer identifier column (name, email, etc.) has inconsistent formatting — different casing, extra whitespace, or typos would cause Pandas to treat what's really the same customer as multiple distinct values. I'd run `.str.strip().str.lower()` on the relevant column and recompute the unique count, since this is one of the most common causes of an inflated "unique" count in real data.

## "Gotcha" Questions

**Q: What's wrong with this code, and what does it actually produce?**
```python
df["age"].fillna(df["age"].mean())
print(df["age"].isna().sum())   # still shows missing values!
```
> A: `.fillna()` returns a new Series by default — it doesn't modify `df["age"]` in place. The result of the fill was never assigned back, so the original column is unchanged. The fix: `df["age"] = df["age"].fillna(df["age"].mean())`.

**Q: A column that should be all numbers loads as `dtype: str`/`object` after `pd.read_csv()`. What's the most likely cause?**
> A: At least one value in that column isn't a valid number — a stray value like `"N/A"`, `"unknown"`, or an accidentally included unit (`"25kg"`) forces Pandas to infer the *entire* column as text, since every value in a column must share one dtype. Running `pd.to_numeric(df["col"], errors="coerce")` reveals exactly which values are the culprits (they become `NaN`).

## Quick-Fire Rapid Review

- Q: Correct way to check for missing values? → **`.isna()` / `.notna()`, never `== np.nan`**
- Q: What does `errors="coerce"` do? → **converts what it can, turns failures into `NaN`/`NaT` instead of raising**
- Q: More robust to outliers: mean or median? → **median**
- Q: More robust outlier-detection method: IQR or z-score? → **IQR**
- Q: `.duplicated()` marks which occurrence as `True`? → **later repeats, not the first occurrence**
- Q: What does `.dt.year` require of a column first? → **it must already be a real datetime dtype (via `pd.to_datetime`)**
- Q: What should you do before grouping/counting a text column? → **standardize with `.str.strip().str.lower()` (or `.title()`)**
- Q: Do `.dropna()`, `.fillna()`, `.drop_duplicates()` modify in place by default? → **No — reassign the result**
