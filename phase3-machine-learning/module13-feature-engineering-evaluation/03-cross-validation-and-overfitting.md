# Module 13c: Cross-Validation, Overfitting & the Bias-Variance Tradeoff

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [02-pipelines-and-data-leakage.md](02-pipelines-and-data-leakage.md)

## 🎯 Learning Objectives
- [ ] Explain why a single train/test split can give a misleading performance estimate
- [ ] Use k-fold cross-validation to get a more reliable evaluation
- [ ] Define overfitting and underfitting, and recognize each from train vs. test scores
- [ ] Explain the bias-variance tradeoff conceptually

---

## Module Goal

Close out Module 13 with two closely related ideas: **cross-validation**, a more robust alternative to a single train/test split, and the **overfitting/underfitting** spectrum that every model sits somewhere on — formalizing the training-vs-test performance gap flagged as a warning sign back in Module 12's interview prep.

## Why This Matters on the Job

A single train/test split gives one snapshot of performance, which can vary quite a bit just from which specific rows happened to land in the test set. Cross-validation gives a far more trustworthy estimate. And recognizing overfitting — a model that's memorized training data rather than learned a generalizable pattern — before it ships to production is one of the most fundamental responsibilities of anyone building ML models professionally.

---

## The Problem with One Train/Test Split

A single `train_test_split()` result depends on which specific rows happened to end up in the test set — a "lucky" or "unlucky" split can make a model look better or worse than it really is, especially with smaller datasets.

## K-Fold Cross-Validation

**K-fold cross-validation** splits the data into `k` equal parts ("folds"), then trains and evaluates the model `k` times — each time using a different fold as the test set and the rest as training — giving `k` separate performance scores instead of just one.

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

wine = load_wine()
X, y = wine.data, wine.target

pipeline = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000))
])

scores = cross_val_score(pipeline, X, y, cv=5)   # 5-fold cross-validation
print(scores)
print(f"Mean: {scores.mean():.4f}, Std: {scores.std():.4f}")
```
```
[0.97222222 0.97222222 1.         0.97142857 1.        ]
Mean: 0.9832, Std: 0.0137
```

**How it works:** `cv=5` splits the data into 5 folds; the model is trained and evaluated 5 separate times, each time holding out a different fold. `cross_val_score` handles the entire process internally — including correctly calling `.fit()` only on each fold's training portion (leakage-safe, exactly like the last lesson, since we pass the whole `pipeline`, not just the classifier). The **mean** gives a more reliable overall performance estimate than any single split, and the **standard deviation** tells you how much that performance varies depending on which data happened to be held out — a low std (like `0.0137` here) suggests the model performs consistently regardless of the specific split.

💡 **Tip:** Always pass the *entire pipeline* (preprocessing + model) to `cross_val_score`, never just the raw classifier — this guarantees each fold's scaling/encoding is refit correctly on only that fold's training data, keeping every fold leakage-free.

✅ **Best Practice:** Use cross-validation (typically `cv=5` or `cv=10`) instead of a single train/test split whenever you're comparing models or tuning settings — it's more work computationally, but gives a far more trustworthy signal than one split's luck of the draw.

## Overfitting vs. Underfitting

- **Overfitting:** the model learns the training data *too* well — including its noise and quirks — performing great on training data but poorly on new data. High training score, noticeably lower test score.
- **Underfitting:** the model is too simple to capture the real pattern at all — performing poorly on *both* training and test data.

```python
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

X, y = make_classification(
    n_samples=200, n_features=20, n_informative=5, n_redundant=10,
    flip_y=0.15, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

for depth in [1, 2, 3, 5, 10, None]:
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))
    print(f"depth={depth}: train={train_acc:.4f}, test={test_acc:.4f}")
```
```
depth=1: train=0.6571, test=0.6833
depth=2: train=0.7786, test=0.7167
depth=3: train=0.8071, test=0.6333
depth=5: train=0.9500, test=0.7000
depth=10: train=1.0000, test=0.6333
depth=None: train=1.0000, test=0.6333
```

**How it works:** At `depth=1`, the model is too simple (**underfitting**) — it can't even fit the training data well (`0.66`), so it naturally does poorly on test data too. As `depth` increases, training accuracy climbs all the way to a perfect `1.0` — the model is memorizing increasingly specific quirks of the training data — while test accuracy actually *degrades* past `depth=2` (from `0.72` down to `0.63`), the classic signature of **overfitting**: better and better on training data, worse on genuinely new data.

🎯 **On the job:** This exact pattern — plotting train vs. test performance across increasing model complexity — is one of the standard diagnostic techniques for choosing model complexity (here, tree depth) that generalizes best, rather than simply chasing the highest possible training score.

## The Bias-Variance Tradeoff

This overfitting/underfitting spectrum is formally described as the **bias-variance tradeoff**:

- **Bias:** error from a model being too simple to capture the real pattern (underfitting). High-bias models make strong, possibly wrong, simplifying assumptions.
- **Variance:** error from a model being too sensitive to the specific training data it saw (overfitting). High-variance models would produce very different predictions if trained on a slightly different sample of the same underlying data.

| | Bias | Variance | Symptom |
|---|---|---|---|
| Underfitting | High | Low | Poor performance on both train and test |
| Good fit | Balanced | Balanced | Good performance on both, small train/test gap |
| Overfitting | Low | High | Great training performance, noticeably worse test performance |

💡 **Tip:** There's no single "right" model complexity in the abstract — it's a tradeoff you tune for your specific dataset and problem, typically by comparing train vs. test (or cross-validation) performance across a range of complexity settings, exactly as demonstrated above with `max_depth`.

✅ **Best Practice:** Whenever you see a large gap between training performance and test/cross-validation performance, suspect overfitting — consider a simpler model, more training data, or regularization techniques (a deeper topic for Module 15).

---

## Hands-On Exercise

**Task:** Write `cross_validation_practice.py` that:
1. Loads `load_wine()`.
2. Builds the same scaled `LogisticRegression` pipeline from the previous lesson.
3. Runs 10-fold cross-validation (`cv=10`) and prints the mean and standard deviation of the scores.
4. Using `DecisionTreeClassifier` on the same Wine data (80/20 split, `random_state=42`), loops over `max_depth` values `[1, 2, 3, 5, None]`, printing train and test accuracy for each, and identifies (by comparing the printed numbers) which depth shows the best balance — good test accuracy without a large train/test gap.

<details>
<summary>✅ Click to see the solution</summary>

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

wine = load_wine()
X, y = wine.data, wine.target

pipeline = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000))
])

scores = cross_val_score(pipeline, X, y, cv=10)
print(f"10-fold CV -- Mean: {scores.mean():.4f}, Std: {scores.std():.4f}")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

for depth in [1, 2, 3, 5, None]:
    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(X_train, y_train)
    train_acc = accuracy_score(y_train, model.predict(X_train))
    test_acc = accuracy_score(y_test, model.predict(X_test))
    gap = train_acc - test_acc
    print(f"depth={depth}: train={train_acc:.4f}, test={test_acc:.4f}, gap={gap:.4f}")
```

**Expected outcome:** Since Wine is a fairly clean, well-separated dataset (as noted in Module 12b), you'll likely see test accuracy stay high and stable even as depth increases — a smaller, cleaner illustration than the synthetic noisy example in this lesson, but the same principle applies: look for where the train/test gap starts growing.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Trusting a single train/test split's score as definitive | Use cross-validation for a more reliable estimate, especially with smaller datasets |
| Chasing the highest possible training accuracy | Watch the train/test (or CV) gap — a growing gap signals overfitting |
| Assuming a low training score means "try a more complex model" | First confirm it's genuinely underfitting (both train AND test are poor), not something else (bad features, wrong algorithm) |
| Passing just the classifier (not the full pipeline) to `cross_val_score` | Always pass the entire pipeline so each fold's preprocessing stays leakage-free |

---

## ✅ Module 13 Completion Checklist
- [ ] Understand why a single train/test split can be misleading
- [ ] Can run and interpret k-fold cross-validation
- [ ] Can recognize overfitting vs. underfitting from train/test performance patterns
- [ ] Understand the bias-variance tradeoff conceptually
- [ ] Completed the `cross_validation_practice.py` exercise
- [ ] Reviewed [`module13-cheatsheet.md`](module13-cheatsheet.md)
- [ ] Reviewed [`module13-interview.md`](module13-interview.md)
- [ ] Browsed [`module13-references.md`](module13-references.md)

**Next Step:** Module 14 — Unsupervised Learning & Clustering (`phase3-machine-learning/module14-unsupervised-learning/`)
