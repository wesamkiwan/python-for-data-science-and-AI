# Module 13a: Feature Scaling & Encoding

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [Module 12 — ML Foundations](../module12-ml-foundations/03-regression-with-sklearn.md)

## 🎯 Learning Objectives
- [ ] Explain why feature scaling matters and when it's needed
- [ ] Apply `StandardScaler` and `MinMaxScaler`
- [ ] Encode categorical variables with one-hot encoding
- [ ] Choose the right encoding for nominal vs. ordinal categories

---

## Module Goal

Close the loop on Module 12's `ConvergenceWarning` cliffhanger: learn **feature scaling**, the standard fix for models struggling with features on wildly different numeric scales, and **encoding**, the standard way to convert categorical (text) columns into the numeric form every scikit-learn model requires.

## Why This Matters on the Job

Real datasets almost always mix numeric columns on different scales (age: 0-100, income: 0-500,000) and categorical columns (city, product category, department) that models can't use directly as text. Preparing features correctly — scaling and encoding — is often what separates a mediocre model from a genuinely good one, and it's squarely "boring but essential" work that happens before any modeling begins.

---

## Why Feature Scaling Matters

Many algorithms (including `LogisticRegression` from Module 12, K-Nearest Neighbors, and anything using gradient-based optimization) are sensitive to features being on very different numeric scales — a feature ranging 0-500,000 can numerically dominate one ranging 0-10, even if the smaller-scaled feature is actually more predictive.

```python
import numpy as np

X = np.array([
    [1, 200000],
    [2, 150000],
    [3, 300000],
    [4, 100000]
])   # column 0: small scale (1-4); column 1: large scale (100,000-300,000)
```

Without scaling, this exact mismatch is what caused Module 12b's `ConvergenceWarning` on the Wine dataset — the optimizer struggled because features spanned vastly different ranges (`proline` in the hundreds vs. `hue` around 0-2).

## `StandardScaler`: Zero Mean, Unit Variance

```python
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print(X_scaled)
```
```
[[-1.34164079  0.16903085]
 [-0.4472136  -0.50709255]
 [ 0.4472136   1.52127766]
 [ 1.34164079 -1.18321596]]
```

**How it works:** `StandardScaler` transforms each feature to have a mean of 0 and a standard deviation of 1 — exactly the **z-score** calculation from Module 10a, applied per column. After scaling, `X_scaled.mean(axis=0)` is `[0, 0]` and `X_scaled.std(axis=0)` is `[1, 1]` — both features are now on directly comparable scales.

## `MinMaxScaler`: Fixed 0-1 Range

```python
from sklearn.preprocessing import MinMaxScaler

minmax = MinMaxScaler()
X_minmax = minmax.fit_transform(X)
print(X_minmax)
```
```
[[0.         0.5       ]
 [0.33333333 0.25      ]
 [0.66666667 1.        ]
 [1.         0.        ]]
```

**How it works:** `MinMaxScaler` rescales every feature to a fixed `[0, 1]` range — the minimum value in each column becomes 0, the maximum becomes 1, and everything else scales proportionally in between.

| Scaler | Result | Use when |
|---|---|---|
| `StandardScaler` | Mean 0, std 1 (unbounded range) | The default choice for most algorithms; handles outliers slightly better |
| `MinMaxScaler` | Fixed `[0, 1]` range | You need a bounded range (e.g., for neural networks, Phase 4), or the data isn't normally distributed |

⚠️ **Warning:** `.fit_transform()` combines *learning* the scaling parameters (min/max, or mean/std) from the data *and* applying them in one step. This distinction matters enormously once train/test splits are involved — covered in depth in the next lesson (spoiler: you must `.fit()` only on training data, never on the test set).

✅ **Best Practice:** Scale your features whenever using distance-based algorithms (KNN), gradient-based optimization (logistic regression, neural networks), or regularized models. Tree-based models (decision trees, random forests, Module 15) are a notable *exception* — they split on individual feature thresholds and generally don't require scaling at all.

## Encoding Categorical Variables

scikit-learn models require **numeric** input — a text column like `"color": "red"` must be converted to numbers before any model can use it.

### One-Hot Encoding: For Nominal (Unordered) Categories

```python
import pandas as pd

df = pd.DataFrame({
    "color": ["red", "blue", "green", "blue"],
    "size": [10, 20, 15, 25]
})

dummies = pd.get_dummies(df, columns=["color"])
print(dummies)
```
```
   size  color_blue  color_green  color_red
0    10       False        False       True
1    20        True        False      False
2    15       False         True      False
3    25        True        False      False
```

**How it works:** `pd.get_dummies()` (Module 07's Pandas toolkit) creates one new binary (`True`/`False`) column *per category value* — `color_red`, `color_blue`, `color_green` — each indicating whether that row belongs to that category. No column is treated as "greater than" another, which is correct for **nominal** data (categories with no inherent order, like colors or city names).

scikit-learn's own equivalent, useful directly inside a modeling pipeline (covered next lesson):

```python
from sklearn.preprocessing import OneHotEncoder

encoder = OneHotEncoder(sparse_output=False)
encoded = encoder.fit_transform(df[["color"]])
print(encoded)
print(encoder.get_feature_names_out())   # ['color_blue' 'color_green' 'color_red']
```

### Label/Ordinal Encoding: For Ordered Categories

```python
from sklearn.preprocessing import LabelEncoder

sizes = pd.Series(["small", "medium", "large", "medium"])
encoder = LabelEncoder()
encoded_sizes = encoder.fit_transform(sizes)
print(encoded_sizes)          # [2 1 0 1]
print(encoder.classes_)          # ['large' 'medium' 'small']
```

⚠️ **Warning:** `LabelEncoder` assigns numbers **alphabetically** by default — here `"large"` gets `0`, not because it's "smallest," but simply because it's alphabetically first. If your categories have a genuine natural order (small < medium < large), this arbitrary alphabetical assignment can mislead a model into learning a nonsensical relationship. For truly ordered categories, use `OrdinalEncoder` with an explicit `categories=[["small", "medium", "large"]]` parameter to specify the real order, rather than relying on default alphabetical encoding.

| Encoding | Use for | Example |
|---|---|---|
| One-hot (`get_dummies`/`OneHotEncoder`) | Nominal (no order) | color, city, department |
| Ordinal (`OrdinalEncoder`, order specified explicitly) | Genuinely ordered categories | shirt size (S/M/L), education level |

---

## Hands-On Exercise

**Task:** Write `scaling_encoding_practice.py` using this DataFrame:
```python
import pandas as pd

df = pd.DataFrame({
    "age": [25, 45, 35, 50, 23],
    "income": [40000, 120000, 75000, 95000, 32000],
    "city": ["NYC", "LA", "NYC", "Chicago", "LA"],
    "education": ["Bachelors", "Masters", "PhD", "Bachelors", "Masters"]
})
```
1. Scale `age` and `income` with `StandardScaler`, and print the result showing both are now on a comparable scale.
2. One-hot encode `city` using `pd.get_dummies()`.
3. Ordinally encode `education` using `OrdinalEncoder`, specifying the correct order (`Bachelors` < `Masters` < `PhD`), and print the encoded result.
4. Combine everything into one final, fully-numeric DataFrame ready for modeling.

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd
from sklearn.preprocessing import StandardScaler, OrdinalEncoder

df = pd.DataFrame({
    "age": [25, 45, 35, 50, 23],
    "income": [40000, 120000, 75000, 95000, 32000],
    "city": ["NYC", "LA", "NYC", "Chicago", "LA"],
    "education": ["Bachelors", "Masters", "PhD", "Bachelors", "Masters"]
})

scaler = StandardScaler()
scaled = scaler.fit_transform(df[["age", "income"]])
df[["age_scaled", "income_scaled"]] = scaled

city_dummies = pd.get_dummies(df["city"], prefix="city")

edu_encoder = OrdinalEncoder(categories=[["Bachelors", "Masters", "PhD"]])
df["education_encoded"] = edu_encoder.fit_transform(df[["education"]])

final_df = pd.concat(
    [df[["age_scaled", "income_scaled", "education_encoded"]], city_dummies],
    axis=1
)
print(final_df)
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Not scaling features for distance/gradient-based algorithms | Scale for logistic regression, KNN, neural networks; usually unnecessary for tree-based models |
| Using `LabelEncoder`'s default alphabetical order on genuinely ordered data | Use `OrdinalEncoder` with explicit `categories=` for real ordering |
| One-hot encoding a column with hundreds of unique categories | Consider grouping rare categories or a different encoding strategy — one-hot explodes column count |
| Confusing `.fit()`, `.transform()`, and `.fit_transform()` | `.fit_transform()` learns parameters AND applies them; critical distinction once train/test splits are involved (next lesson) |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand why feature scaling matters and for which algorithms
- [ ] Can apply `StandardScaler` and `MinMaxScaler`
- [ ] Can one-hot encode nominal categorical variables
- [ ] Can correctly encode ordinal categorical variables with explicit ordering
- [ ] Completed the `scaling_encoding_practice.py` exercise

**Next:** Continue to [`02-pipelines-and-data-leakage.md`](02-pipelines-and-data-leakage.md)
