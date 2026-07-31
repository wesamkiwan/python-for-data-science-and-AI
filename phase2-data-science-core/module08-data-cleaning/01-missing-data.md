# Module 08a: Handling Missing Data

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [Module 07 — Pandas for Data Manipulation](../module07-pandas/04-groupby-and-merging.md)

## 🎯 Learning Objectives
- [ ] Detect missing values with `.isna()` / `.notna()`
- [ ] Remove rows/columns with missing data using `.dropna()`
- [ ] Fill missing values with `.fillna()`, including per-column strategies
- [ ] Decide, for a given situation, whether to drop or fill missing data

---

## Module Goal

Welcome to a module built entirely around a hard truth of real data work: **real-world data is messy**. This lesson focuses on the single most common form of messiness — missing values — and the tools Pandas gives you to detect and handle them deliberately, rather than let them silently break downstream analysis.

## Why This Matters on the Job

No dataset you receive on the job will be perfectly complete. A customer didn't fill in their phone number; a sensor failed to record a reading; a survey respondent skipped a question. How you handle these gaps — dropping them, filling them, or flagging them — is a real analytical decision with real consequences, and "I didn't notice there was missing data" is one of the most embarrassing things to have an interviewer or manager catch in your analysis.

---

## Detecting Missing Values

Pandas represents missing data as `NaN` ("Not a Number", from NumPy) for numeric columns, or `None`/`NaN` for other types.

```python
import pandas as pd
import numpy as np

df = pd.DataFrame({
    "name": ["Ada", "Grace", None, "Katherine"],
    "age": [36, np.nan, 41, 101],
    "score": [85.5, 92.0, np.nan, 78.0]
})
print(df)
```
```
        name    age  score
0        Ada   36.0   85.5
1      Grace    NaN   92.0
2       None   41.0    NaN
3  Katherine  101.0   78.0
```

```python
print(df.isna())          # boolean DataFrame: True wherever a value is missing
print(df.isna().sum())       # count of missing values PER COLUMN -- your first check on any new dataset
print(df.notna())              # the inverse of .isna()
```
```
name     1
age      1
score    1
dtype: int64
```

⚠️ **Warning:** `df["age"] == np.nan` never works as expected — `NaN` is defined to never equal anything, even itself (this is standard floating-point behavior, not a Pandas quirk). Always use `.isna()`/`.notna()` to check for missing values, never `==`.

✅ **Best Practice:** `df.isna().sum()` should be one of the very first things you run on any new dataset, right alongside `.info()` from Module 07 — it immediately tells you which columns have gaps and how many.

## Dropping Missing Data with `.dropna()`

```python
print(df.dropna())                       # drops any row with AT LEAST ONE missing value
print(df.dropna(subset=["age"]))            # drops rows only where "age" specifically is missing
print(df.dropna(axis=1))                       # drops COLUMNS that contain any missing value (rare, but exists)
```

**How it works:** By default, `.dropna()` removes any row containing *any* missing value in *any* column — which can be far too aggressive if only one column matters for your current analysis. `subset=[...]` restricts the check to specific columns, which is almost always the safer, more intentional choice.

⚠️ **Warning:** `.dropna()` (like `.drop()` from Module 07) returns a new DataFrame — it doesn't modify in place. Reassign: `df = df.dropna(subset=["age"])`.

## Filling Missing Data with `.fillna()`

Sometimes dropping rows throws away too much useful data — filling in a reasonable substitute value is often better.

```python
print(df["age"].fillna(0))                              # fill with a fixed value
print(df["age"].fillna(df["age"].mean()))                  # fill with the column's average -- a common default strategy

# Fill different columns with different strategies, all in one call
print(df.fillna({"age": df["age"].mean(), "name": "Unknown"}))
```
```
        name         age  score
0        Ada   36.000000   85.5
1      Grace   59.333333   92.0
2    Unknown   41.000000    NaN
3  Katherine  101.000000   78.0
```

**How it works:** Passing a `dict` to `.fillna()` lets you specify a different fill value **per column** in one call — here, missing ages get filled with the column mean, while missing names get filled with the placeholder `"Unknown"`, and `score`'s remaining `NaN` is left untouched since it wasn't included in the dict.

## Deciding: Drop or Fill?

There's no universal right answer — it depends on the situation:

| Situation | Likely approach |
|---|---|
| Very few rows have missing data, and losing them doesn't bias the analysis | `.dropna()` — simplest and safest |
| A column is missing so much data it's not useful | Drop the whole column instead of trying to fill it |
| A numeric column with occasional gaps, where a reasonable average makes sense | `.fillna(mean)` or `.fillna(median)` — median is more robust to outliers (Module 08c covers outliers) |
| A categorical column where "missing" is itself meaningful information | `.fillna("Unknown")` or `.fillna("Not Provided")` — keeps the row, makes the gap explicit |
| Time-series data, where the most recent known value is a reasonable stand-in | `.fillna(method="ffill")` (forward-fill: carries the last valid value forward) |

⚠️ **Warning:** Filling with the mean/median can subtly distort statistics (like variance) if a large fraction of a column is missing — always check `.isna().sum()` relative to the total row count before deciding a fill strategy is appropriate. If more than, say, 30-40% of a column is missing, seriously consider whether that column (or those rows) should be dropped instead.

🎯 **On the job:** This decision — drop vs. fill, and which fill strategy — should always be a documented, deliberate choice, not a default reflex. Interviewers frequently probe exactly this reasoning in take-home data exercises.

---

## Hands-On Exercise

**Task:** Write `missing_data_practice.py` using this DataFrame:
```python
import pandas as pd
import numpy as np

survey = pd.DataFrame({
    "respondent": ["Ada", "Grace", "Alan", "Katherine", "Linus"],
    "age": [36, np.nan, 41, 101, np.nan],
    "satisfaction": [4, 5, np.nan, 3, 5],
    "comments": ["Great!", None, "Could improve", None, "Loved it"]
})
```
1. Print the count of missing values per column.
2. Fill missing `age` values with the column's median (more robust than the mean for small samples).
3. Fill missing `satisfaction` values with the column's mean, rounded to 1 decimal.
4. Fill missing `comments` with `"No comment provided"`.
5. Confirm there are zero missing values left with a final `.isna().sum()` check.

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd
import numpy as np

survey = pd.DataFrame({
    "respondent": ["Ada", "Grace", "Alan", "Katherine", "Linus"],
    "age": [36, np.nan, 41, 101, np.nan],
    "satisfaction": [4, 5, np.nan, 3, 5],
    "comments": ["Great!", None, "Could improve", None, "Loved it"]
})

print(survey.isna().sum())

survey["age"] = survey["age"].fillna(survey["age"].median())
survey["satisfaction"] = survey["satisfaction"].fillna(round(survey["satisfaction"].mean(), 1))
survey["comments"] = survey["comments"].fillna("No comment provided")

print(survey)
print(survey.isna().sum())
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Checking for missing values with `== np.nan` | Always use `.isna()`/`.notna()` |
| Dropping every row with any missing value, in any column | Use `subset=[...]` to target only the columns that matter |
| Filling missing data before checking how much is missing | Run `.isna().sum()` first — a mean fill on a 60%-missing column is misleading |
| Assuming `.dropna()`/`.fillna()` modify in place | Reassign the result: `df = df.dropna(...)` |
| Using the mean to fill a column with extreme outliers | Consider the median instead — it's less sensitive to a few extreme values |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Can detect missing values with `.isna()`/`.notna()`
- [ ] Can drop missing data with `.dropna()`, using `subset` appropriately
- [ ] Can fill missing data with `.fillna()`, including per-column strategies
- [ ] Can reason about when to drop vs. fill, and which fill strategy fits
- [ ] Completed the `missing_data_practice.py` exercise

**Next:** Continue to [`02-duplicates-and-dtypes.md`](02-duplicates-and-dtypes.md)
