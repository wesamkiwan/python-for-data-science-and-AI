# Module 13b: Pipelines & Data Leakage

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [01-scaling-and-encoding.md](01-scaling-and-encoding.md)

## 🎯 Learning Objectives
- [ ] Explain data leakage and why preprocessing must respect the train/test split
- [ ] Combine preprocessing steps and a model into one `Pipeline`
- [ ] Apply different preprocessing to different column types with `ColumnTransformer`
- [ ] Recognize why pipelines prevent leakage automatically

---

## Module Goal

Learn the correct, leakage-free way to combine feature scaling, encoding, and modeling into one clean, reusable object — a **Pipeline** — resolving a subtlety flagged back in Module 12a (data leakage) and Module 13a (`.fit_transform()` vs. `.transform()`).

## Why This Matters on the Job

Getting preprocessing order wrong is one of the most common — and most dangerous — mistakes in applied machine learning, because it produces a model that looks great during evaluation but performs worse in real production use. It's a subtle bug that doesn't throw an error; it just quietly makes your evaluation numbers dishonest. Pipelines are the standard, professional way to make this mistake structurally difficult to make.

---

## Data Leakage: The Problem

**Data leakage** happens when information from outside the training data — most commonly, information from the test set — accidentally influences training, making evaluation results look better than they'd actually be in the real world.

```python
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

np.random.seed(1)
X = np.random.normal(100, 20, (20, 1))

# ❌ WRONG: scale BEFORE splitting -- the scaler "sees" the test data's values
scaler_wrong = StandardScaler()
X_scaled_wrong = scaler_wrong.fit_transform(X)
X_train_wrong, X_test_wrong = train_test_split(X_scaled_wrong, test_size=0.2, random_state=42)
print(scaler_wrong.mean_)   # [97.33] -- computed using ALL 20 samples, including the test set
```

```python
# ✅ RIGHT: split FIRST, fit the scaler only on the training data
X_train, X_test = train_test_split(X, test_size=0.2, random_state=42)

scaler_right = StandardScaler()
X_train_scaled = scaler_right.fit_transform(X_train)   # learns mean/std from TRAINING data only
X_test_scaled = scaler_right.transform(X_test)             # APPLIES those same stats to test data -- no re-fitting!
print(scaler_right.mean_)   # [97.87] -- computed using only the 16 training samples
```

**How it works:** In the wrong version, the scaler's mean/std were computed using *all 20 samples* — including the 4 that later became the "held out" test set. This means the test set's own values subtly influenced the preprocessing the model was trained under, which is a form of the test set "leaking" into training. In the correct version, `.fit_transform()` is called only on `X_train`, and the test set only ever gets `.transform()` (applying, not re-learning, those same statistics).

⚠️ **Warning:** This exact mistake — scaling, encoding, or imputing missing values on the *full* dataset before splitting — is one of the most common, hardest-to-notice bugs in real ML pipelines, because the code runs fine and produces a number; it's just a dishonestly optimistic one. Always split first, then fit every preprocessing step *only* on the training data.

## `Pipeline`: Chaining Preprocessing and Modeling Together

A **Pipeline** bundles preprocessing steps and a final model into one object, so `.fit()` and `.predict()` automatically apply every step in the correct order — making the leakage mistake above structurally difficult to make by accident.

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_wine

wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.2, random_state=42)

pipeline = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000))
])

pipeline.fit(X_train, y_train)          # scales X_train, THEN fits the classifier on the scaled result
accuracy = pipeline.score(X_test, y_test)   # scales X_test using TRAINING stats, THEN evaluates
print(f"Accuracy: {accuracy:.4f}")
```

**How it works:** `pipeline.fit(X_train, y_train)` runs `StandardScaler().fit_transform()` on `X_train` internally, then feeds the *scaled* result into `LogisticRegression().fit()` — all in one call. Critically, `pipeline.score(X_test, y_test)` calls `.transform()` (not `.fit_transform()`) on the scaler internally for the test data, automatically applying the training set's statistics — the leakage-safe pattern from above happens *automatically*, with no risk of forgetting a step or doing it in the wrong order.

🎯 **On the job:** This is precisely why the Module 12b `ConvergenceWarning` on the Wine dataset is now fully solvable — wrapping `StandardScaler()` and `LogisticRegression()` in a `Pipeline` (as shown here) both fixes the scaling issue *and* guarantees it's done leakage-free, with essentially no extra code compared to doing it manually (and incorrectly) yourself.

## `ColumnTransformer`: Different Preprocessing for Different Columns

Real datasets usually need *different* preprocessing per column type — scale the numeric columns, one-hot encode the categorical ones. `ColumnTransformer` applies different transformers to different column subsets, all within one pipeline step.

```python
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

np.random.seed(0)
n = 200
df = pd.DataFrame({
    "age": np.random.randint(20, 65, n),
    "income": np.random.normal(60000, 20000, n),
    "city": np.random.choice(["NYC", "LA", "Chicago"], n),
    "purchased": np.random.choice([0, 1], n)
})

X = df[["age", "income", "city"]]
y = df["purchased"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

numeric_features = ["age", "income"]
categorical_features = ["city"]

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), numeric_features),
    ("cat", OneHotEncoder(), categorical_features)
])

full_pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression())
])

full_pipeline.fit(X_train, y_train)
accuracy = full_pipeline.score(X_test, y_test)
print(f"Accuracy: {accuracy:.4f}")   # ~0.475 -- since 'purchased' here is random, unrelated noise
```

**How it works:** `ColumnTransformer` routes `numeric_features` through `StandardScaler()` and `categorical_features` through `OneHotEncoder()`, then concatenates the results back into one combined, fully-numeric feature set — all wrapped as the first step of the outer `Pipeline`, so the *entire* preprocessing-plus-modeling process trains and evaluates correctly with a single `.fit()`/`.score()` call.

💡 **Tip:** In this specific example, `purchased` was generated completely randomly, unrelated to any feature — so an accuracy near 0.5 (essentially a coin flip) is the *correct*, expected result, not a bug. This is a useful sanity check to keep in mind: if a model can't beat random guessing, either the features genuinely don't relate to the target, or something in the pipeline needs investigation.

✅ **Best Practice:** Use `Pipeline` + `ColumnTransformer` as your default approach for any real project with mixed numeric/categorical features — it's simultaneously less code, more readable, and structurally leakage-safe compared to manually preprocessing each piece yourself.

---

## Hands-On Exercise

**Task:** Write `pipeline_practice.py` that:
1. Loads `load_wine()` and splits 80/20 with `random_state=42`.
2. Builds a `Pipeline` with a `StandardScaler` step and a `LogisticRegression(max_iter=1000)` step (all 13 Wine features are numeric, so no `ColumnTransformer` is needed here).
3. Fits the pipeline and prints the test accuracy — confirm no `ConvergenceWarning` appears now that scaling is in place (unlike Module 12b's unscaled version).
4. Prints a one-sentence comparison: how does this pipeline's accuracy compare to Module 12b's unscaled model (which scored ~0.9556)?

<details>
<summary>✅ Click to see the solution</summary>

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42
)

pipeline = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000))
])

pipeline.fit(X_train, y_train)
accuracy = pipeline.score(X_test, y_test)
print(f"Accuracy: {accuracy:.4f}")

print(f"With scaling in the pipeline, accuracy is {accuracy:.4f}, "
      f"achieved with no convergence warning -- compared to Module 12b's "
      f"unscaled model, which needed max_iter=1000 and still warned.")
```

**Expected outcome:** The pipeline should train without any `ConvergenceWarning`, since `StandardScaler` resolves the scale mismatch that caused it in Module 12b.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Scaling/encoding the full dataset before splitting | Always split first, `.fit_transform()` on train only, `.transform()` on test |
| Manually repeating preprocessing steps for train and test separately | Use `Pipeline` to guarantee consistent, leakage-free application |
| Applying the same preprocessing to numeric and categorical columns | Use `ColumnTransformer` to route each column type to the right transformer |
| Assuming a low accuracy always means a bug | Check whether the target genuinely relates to the features first — sometimes ~50% (for binary) really is the honest, correct answer |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Understand data leakage and why splitting must happen before preprocessing
- [ ] Can build a `Pipeline` combining preprocessing and a model
- [ ] Can use `ColumnTransformer` to preprocess numeric and categorical columns differently
- [ ] Understand why pipelines prevent leakage automatically
- [ ] Completed the `pipeline_practice.py` exercise

**Next:** Continue to [`03-cross-validation-and-overfitting.md`](03-cross-validation-and-overfitting.md)
