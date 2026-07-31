# Module 10a: Descriptive Statistics & Distributions

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [Module 09 — Data Visualization](../module09-data-visualization/03-plotly-interactive-charts.md)

## 🎯 Learning Objectives
- [ ] Compute and interpret mean, median, mode, variance, and standard deviation
- [ ] Explain when the median is a better "typical value" than the mean
- [ ] Recognize a normal distribution and interpret skewness
- [ ] Connect these statistics to charts from Module 09

---

## Module Goal

Formalize the statistical vocabulary underlying everything you've computed so far (`.mean()`, `.std()` in Module 06/07, and the distribution shapes you visualized in Module 09) — understanding not just *how* to compute these numbers, but *what they actually mean* and when each one is the right tool.

## Why This Matters on the Job

"The average is $75,000" sounds precise, but it can be dangerously misleading if the data is skewed by a few extreme values — a fact every data scientist needs to internalize before reporting any summary statistic to a stakeholder. This module gives you the vocabulary and judgment to know *which* statistic actually represents your data honestly, and to catch it when someone else's analysis doesn't.

---

## Measures of Central Tendency

These answer "what's a typical value in this data?" — but each answers it slightly differently.

```python
import pandas as pd

scores = pd.Series([85, 92, 78, 90, 65, 88, 92, 75])

print(scores.mean())      # 83.125  -- the arithmetic average
print(scores.median())       # 86.5    -- the middle value when sorted
print(scores.mode())            # 92      -- the most frequently occurring value(s)
```

**How it works:**
- **Mean** — sum of all values divided by the count. Sensitive to extreme values (a single very high or low number pulls it noticeably).
- **Median** — the middle value once sorted (or the average of the two middle values, for an even count). Robust to extreme values — this is why Module 08 recommended it for filling missing values in skewed columns.
- **Mode** — the most common value(s). Most useful for categorical data ("what's the most common department?") but works on numeric data too.

### Why the Median Matters: A Concrete Example

```python
salaries = pd.Series([45000, 48000, 50000, 52000, 55000, 500000])   # one very high outlier

print(salaries.mean())      # 125000.0  -- badly distorted by the one outlier!
print(salaries.median())       # 51000.0    -- much more representative of "typical" salary here
```

⚠️ **Warning:** This is exactly why "average salary" or "average home price" reported in the news can be misleading — a small number of very high values pulls the mean far above what's typical for most people. ✅ **Best Practice:** whenever a dataset might contain outliers (Module 08's IQR/z-score methods help confirm this), report the median alongside (or instead of) the mean, and say so explicitly.

## Measures of Spread

These answer "how spread out is the data?" — a single "typical value" alone doesn't tell you whether everyone is close to it or wildly scattered.

```python
print(scores.var())        # 93.27   -- variance: average squared distance from the mean
print(scores.std())           # 9.66     -- standard deviation: the square root of variance
```

**How it works:** **Variance** measures spread by averaging the squared distance of every value from the mean (squaring avoids positive/negative differences canceling out, but makes the units hard to interpret — "squared points"). **Standard deviation** takes the square root of variance, bringing the units back to the original scale ("points," not "points squared") — which is why std is almost always what gets reported and interpreted, not raw variance.

💡 **Tip:** A small standard deviation means values cluster tightly around the mean (consistent, predictable); a large standard deviation means values are spread widely (variable, less predictable) — two datasets can have the identical mean but very different standard deviations, and that difference is often the more interesting story.

🎯 **On the job:** "Average response time is 200ms" sounds fine — but if the standard deviation is huge, it means some requests take 20ms and others take 2 seconds, which is a very different (and more concerning) reality than a consistent 200ms every time. Always ask about spread, not just the average.

## Distributions & Skewness

A **distribution** describes the overall shape of how values are spread — you already visualized this with histograms in Module 09.

### The Normal Distribution

The **normal distribution** (a.k.a. Gaussian, or "bell curve") is symmetric around its mean — most values cluster near the center, tapering off evenly on both sides. It's the most commonly assumed shape in classical statistics (and directly underlies the z-score outlier method from Module 08).

```python
import numpy as np

np.random.seed(0)
normal_data = pd.Series(np.random.normal(loc=0, scale=1, size=1000))

print(normal_data.skew())    # ~0.03 -- very close to 0, confirming near-symmetry
```

### Skewness: Measuring Asymmetry

**Skewness** quantifies how asymmetric a distribution is:

```python
symmetric = pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9])
skewed = pd.Series([1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5, 50])   # one big outlier

print(symmetric.skew())     # 0.0    -- perfectly symmetric
print(skewed.skew())            # 3.92     -- strongly right-skewed (positive)
```

| Skewness value | Meaning |
|---|---|
| Near 0 | Roughly symmetric (like a normal distribution) |
| Positive (> 0) | Right-skewed — a long tail of high values pulls the mean above the median (e.g., income, house prices) |
| Negative (< 0) | Left-skewed — a long tail of low values pulls the mean below the median |

**How it works:** In a right-skewed distribution (like the salary example earlier), a few very large values stretch the distribution's tail to the right, pulling the mean upward while the median stays anchored closer to where most of the data actually sits — this is precisely *why* mean and median diverge on skewed data, connecting directly back to the salary example above.

🎯 **On the job:** Checking skewness (or just looking at a histogram, Module 09) is a standard early EDA step — it tells you whether the mean is a trustworthy summary, and later (Module 12+) whether a variable might need a transformation before feeding it into certain machine learning models that assume roughly normal input.

---

## Hands-On Exercise

**Task:** Write `descriptive_stats_practice.py` using this data:
```python
import pandas as pd

response_times_ms = pd.Series([120, 135, 128, 142, 119, 131, 125, 1850, 138, 122])
```
1. Compute and print the mean and median. Note how different they are.
2. Compute and print the standard deviation.
3. Compute the skewness and interpret it in a printed sentence (is it symmetric, right-skewed, or left-skewed?).
4. Based on what you've learned, print a sentence stating which measure (mean or median) better represents "typical" response time for this data, and why.

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd

response_times_ms = pd.Series([120, 135, 128, 142, 119, 131, 125, 1850, 138, 122])

mean_time = response_times_ms.mean()
median_time = response_times_ms.median()
std_time = response_times_ms.std()
skew_time = response_times_ms.skew()

print(f"Mean: {mean_time:.1f} ms")
print(f"Median: {median_time:.1f} ms")
print(f"Standard deviation: {std_time:.1f} ms")
print(f"Skewness: {skew_time:.2f}")

if skew_time > 0.5:
    print("The distribution is right-skewed -- one or more unusually slow requests are pulling the mean up.")
elif skew_time < -0.5:
    print("The distribution is left-skewed.")
else:
    print("The distribution is roughly symmetric.")

print(f"The median ({median_time:.1f} ms) is a more representative 'typical' response time than "
      f"the mean ({mean_time:.1f} ms), since one extreme outlier (1850ms) is pulling the mean upward.")
```

**Expected output (abridged):** Mean will be noticeably higher than the median due to the 1850ms outlier, and skewness will be strongly positive — a clear illustration of exactly the salary-outlier pattern from earlier in this lesson, applied to a new context.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Reporting only the mean without checking for skew/outliers | Check skewness or a quick histogram before trusting the mean as "typical" |
| Confusing variance and standard deviation | Standard deviation is in the original units and is what's typically reported/interpreted |
| Assuming all data is normally distributed | Check skewness or visualize (Module 09) before assuming symmetry |
| Reporting an average with no sense of spread | Always pair a "typical value" (mean/median) with a spread measure (std) |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Can compute and interpret mean, median, mode
- [ ] Can compute and interpret variance and standard deviation
- [ ] Know when the median is more trustworthy than the mean
- [ ] Can compute and interpret skewness
- [ ] Completed the `descriptive_stats_practice.py` exercise

**Next:** Continue to [`02-correlation-and-hypothesis-testing.md`](02-correlation-and-hypothesis-testing.md)
