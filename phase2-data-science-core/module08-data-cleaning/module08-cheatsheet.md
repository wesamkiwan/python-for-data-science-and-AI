# 📋 Module 08 Cheat Sheet: Data Cleaning & Wrangling

Fast reference for missing data, duplicates, dtypes, string cleaning, and outliers.

## Missing Data
```python
df.isna()             df.notna()          # boolean DataFrame
df.isna().sum()          # missing count PER COLUMN -- run this first

df.dropna()                    # drop rows with ANY missing value
df.dropna(subset=["col"])         # drop rows missing only in specific column(s)

df["col"].fillna(0)                          # fixed value
df["col"].fillna(df["col"].mean())              # column mean
df["col"].fillna(df["col"].median())               # column median (robust to outliers)
df.fillna({"col_a": 0, "col_b": "Unknown"})           # per-column fill strategies
```
⚠️ Never check missing data with `== np.nan` — always `.isna()`/`.notna()`.

## Duplicates
```python
df.duplicated()                     # True for later occurrences of an exact repeat
df.duplicated().sum()                  # total duplicate count

df.drop_duplicates()                          # keep first occurrence
df.drop_duplicates(subset=["key"])               # duplicate = same key column(s), ignore rest
df.drop_duplicates(subset=["key"], keep="last")     # keep last occurrence instead
```

## Fixing Data Types
```python
df["col"].astype(int)                            # direct conversion -- FAILS on any bad value

pd.to_numeric(df["col"], errors="coerce")           # bad values -> NaN, rest converts
pd.to_datetime(df["col"], errors="coerce")             # bad values -> NaT, rest converts

df["date_col"].dt.year          df["date_col"].dt.month
df["date_col"].dt.day_name()       df["date_col"] > "2024-01-01"   # chronological comparison
```

## String Cleaning (`.str` accessor)
```python
df["col"].str.strip()                     # remove leading/trailing whitespace
df["col"].str.lower()   .str.upper()   .str.title()
df["col"].str.replace(r"[-. ]", "", regex=True)     # remove unwanted characters
df["col"].str.contains("text", case=False)             # case-insensitive search
df["col"].str.split("@")                                  # split into list per row
```
✅ Standardize (`.str.strip().str.lower()`) before `.groupby()` or `.value_counts()` on text columns.

## Outlier Detection

**IQR method:**
```python
q1 = data.quantile(0.25)
q3 = data.quantile(0.75)
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = data[(data < lower) | (data > upper)]
non_outliers = data[~((data < lower) | (data > upper))]
```

**Z-score method:**
```python
z = (data - data.mean()) / data.std()
outliers = data[z.abs() > 2]        # or > 3 for a stricter threshold
```

| Method | Best when |
|---|---|
| IQR | Non-normal data, or robustness to the outliers themselves needed |
| Z-score | Roughly normally distributed data |

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `df["col"] == np.nan` always False | `NaN` never equals anything, even itself | Use `.isna()`/`.notna()` |
| `.astype(int)` raises `ValueError` | A value in the column can't convert directly | Use `pd.to_numeric(errors="coerce")` instead |
| Date column won't sort/compare correctly | Still stored as plain text | `pd.to_datetime(df["col"], errors="coerce")` |
| More categories in `.groupby()`/`.value_counts()` than expected | Inconsistent whitespace/casing in text | `.str.strip().str.lower()` (or `.title()`) first |
| Mean/std look skewed | An undetected outlier is distorting them | Check with IQR (robust to this) before trusting mean/std-based stats |

## The "New Dataset" Cleaning Workflow — do this every time
1. `df.isna().sum()` — how much is missing, and where?
2. `df.duplicated().sum()` — any exact or key-based repeats?
3. `df.dtypes` — does every column's type make sense? Fix with `to_numeric`/`to_datetime` + `errors="coerce"`.
4. `.str.strip().str.lower()` any text columns you'll group or compare.
5. Check numeric columns for outliers (IQR or z-score) — decide, don't default, on what to do with them.
