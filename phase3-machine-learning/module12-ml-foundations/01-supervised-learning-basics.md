# Module 12a: Supervised Learning Basics — Features, Targets & Train/Test Splits

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [Module 11 — SQL for Data Scientists](../../phase2-data-science-core/module11-sql-for-data-science/03-subqueries-and-real-world-sql.md)

## 🎯 Learning Objectives
- [ ] Explain the difference between features and a target variable
- [ ] Explain what "supervised learning" means and its two main types
- [ ] Split data into training and test sets, and explain why this matters
- [ ] Recognize scikit-learn's consistent `.fit()` / `.predict()` / `.score()` API

---

## Module Goal

Welcome to **Phase 3: Machine Learning**! This module builds the conceptual foundation everything after it relies on: what a machine learning model actually *is*, how it learns from data, and the universal scikit-learn API pattern you'll reuse for every single model in this course, from a simple linear regression here to deep neural networks in Phase 4.

## Why This Matters on the Job

Every ML task, however different it looks on the surface, boils down to the same shape: take historical data with known outcomes, learn a pattern from it, then predict outcomes for new, unseen data. Understanding this shape — features, target, train/test split — before touching any specific algorithm means every model you learn afterward (Module 12 onward) is just a variation on one already-familiar template, not a fresh mental model each time.

---

## Installing scikit-learn

```bash
pip install scikit-learn
```

```python
import sklearn
print(sklearn.__version__)
```

## What Is Machine Learning?

**Machine learning** is the practice of having a computer learn patterns from data automatically, rather than being explicitly programmed with fixed rules. Instead of writing `if age > 65: category = "senior"`, you show the algorithm many examples of inputs and their correct outputs, and it learns the pattern connecting them itself.

## Supervised Learning: Learning from Labeled Examples

**Supervised learning** — the focus of this entire phase — means learning from data where you already know the correct answer for each example (the data is "labeled"). There are two main types:

| Type | Predicts | Example |
|---|---|---|
| **Classification** | A category (discrete label) | Is this email spam or not spam? Which species of flower is this? |
| **Regression** | A number (continuous value) | What will this house sell for? How many units will we sell next month? |

💡 **Tip:** Don't confuse "regression" here with the everyday word — in ML, regression specifically means predicting a *numeric* value, as opposed to classification's *category* prediction. This module covers one example of each.

## Features and the Target Variable

Every supervised learning problem splits your data into two parts:

- **Features** (often called `X`) — the input variables/columns used to make a prediction (e.g., a house's square footage, number of bedrooms, location).
- **Target** (often called `y`) — the single variable/column you're trying to predict (e.g., the house's sale price).

```python
from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris()

print(iris.feature_names)     # ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
print(iris.target_names)         # ['setosa' 'versicolor' 'virginica']
print(iris.data.shape)              # (150, 4)  -- 150 flowers, 4 features each
print(iris.target.shape)               # (150,)     -- 150 corresponding species labels

X = iris.data       # features -- shape (150, 4)
y = iris.target        # target -- shape (150,)
```

**How it works:** `load_iris()` is one of scikit-learn's built-in "toy" datasets — 150 flower measurements (`X`, the features: sepal/petal length and width) paired with which of 3 species each flower actually is (`y`, the target). This is a **classification** problem: predicting a category (species) from numeric measurements.

💡 **Tip:** You'll also see this same DataFrame-style view of the same data — combining `X` and `y` into one table with a readable species column is exactly the Module 07 pattern you already know:

```python
df = pd.DataFrame(X, columns=iris.feature_names)
df["species"] = pd.Categorical.from_codes(y, iris.target_names)
print(df.head())
```

## The Train/Test Split

If you train a model and then evaluate it on the *exact same data* it learned from, you learn nothing about how well it'll perform on genuinely new data — it might have simply memorized the examples rather than learned a generalizable pattern. The fix: split your data *before* training, so you have data the model has never seen to honestly evaluate it on.

```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.shape)   # (120, 4)  -- 80% of the data, used to TRAIN the model
print(X_test.shape)       # (30, 4)     -- 20% held out, used only to EVALUATE it
```

**How it works:** `test_size=0.2` reserves 20% of the data as the **test set** — never shown to the model during training — while the remaining 80% becomes the **training set**. `random_state=42` fixes the random shuffling so the split is reproducible (anyone running this exact code gets the identical split — the number `42` itself is arbitrary, just a widely-used convention).

⚠️ **Warning:** Never evaluate a model's performance on data it was trained on — this gives a falsely optimistic picture of how well it'll actually perform on new, real-world data (a problem called **overfitting**, formalized further in Module 13). The train/test split is the single most important habit in this entire module.

✅ **Best Practice:** Always split your data *before* doing any exploration or preprocessing that "learns" from the data (like computing a mean to fill missing values) — otherwise information from the test set can leak into training, invalidating your evaluation. This subtlety (called **data leakage**) is covered in more depth in Module 13.

## The scikit-learn API: `.fit()` / `.predict()` / `.score()`

Every scikit-learn model — regardless of the actual algorithm underneath — follows the exact same three-method pattern:

```python
from sklearn.neighbors import KNeighborsClassifier

model = KNeighborsClassifier()   # 1. Create the model object (an instance, per Module 03's OOP lesson)
model.fit(X_train, y_train)         # 2. Train it on the training data
predictions = model.predict(X_test)    # 3. Predict on new, unseen data
accuracy = model.score(X_test, y_test)   # (or) directly score its performance
```

**How it works:** `model = KNeighborsClassifier()` creates an **object** — exactly Module 03's class/instance pattern, where `model` is an instance with its own internal state. `.fit(X_train, y_train)` is the training step — the model examines the labeled training data and adjusts its internal state to capture the pattern (exactly like a method that mutates `self`'s data, from Module 03). `.predict(X_test)` then uses that learned state to make predictions on brand-new inputs. `.score()` is a convenience method that predicts *and* compares against the true answers in one step, returning a single performance number.

🎯 **On the job:** This `.fit()`/`.predict()`/`.score()` pattern is universal across scikit-learn — swapping `KNeighborsClassifier()` for `LogisticRegression()` or `RandomForestClassifier()` (Module 15) requires *zero* changes to the rest of your code, exactly like Module 03's polymorphism lesson. This consistency is precisely why scikit-learn is the industry-standard ML library — once you know the pattern, you effectively know how to use hundreds of different algorithms.

---

## Hands-On Exercise

**Task:** Write `supervised_learning_practice.py` that:
1. Loads the built-in `load_wine()` dataset from `sklearn.datasets` (a classification dataset, similar structure to `iris`).
2. Prints the feature names, target names, and the shapes of `data`/`target`.
3. Splits the data into training (75%) and test (25%) sets, using `random_state=1`.
4. Prints the shape of each resulting split to confirm the proportions are correct.

<details>
<summary>✅ Click to see the solution</summary>

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split

wine = load_wine()

print(wine.feature_names)
print(wine.target_names)
print(wine.data.shape)
print(wine.target.shape)

X = wine.data
y = wine.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")
```

**Expected output (abridged):** `wine.data.shape` is `(178, 13)` (178 wine samples, 13 chemical features); the train/test split gives roughly 133/45 samples respectively (75%/25% of 178).
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Evaluating a model on the same data it trained on | Always hold out a separate test set with `train_test_split` |
| Forgetting `random_state` for reproducibility | Set it explicitly so your split (and results) are reproducible |
| Confusing features (`X`) with the target (`y`) | `X` = inputs you have; `y` = the answer you're trying to predict |
| Thinking "regression" always means the everyday meaning | In ML, regression = predicting a number; classification = predicting a category |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand features (`X`) vs. target (`y`)
- [ ] Understand classification vs. regression
- [ ] Can perform a train/test split and explain why it matters
- [ ] Recognize the `.fit()` / `.predict()` / `.score()` API pattern
- [ ] Completed the `supervised_learning_practice.py` exercise

**Next:** Continue to [`02-classification-with-sklearn.md`](02-classification-with-sklearn.md)
