# Module 15a: Random Forests & Bagging

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [Module 14 — Unsupervised Learning & Clustering](../module14-unsupervised-learning/02-hierarchical-clustering-and-pca.md)

## 🎯 Learning Objectives
- [ ] Explain the core idea behind ensemble methods
- [ ] Explain bagging and how Random Forest applies it
- [ ] Train a `RandomForestClassifier`/`RandomForestRegressor` and compare it to a single decision tree
- [ ] Interpret feature importance from a Random Forest

---

## Module Goal

Welcome to the final, most advanced module of Phase 3! Learn **ensemble methods** — combining many individual models into one stronger, more reliable model — starting with **Random Forest**, which directly solves the exact overfitting problem demonstrated with a single decision tree back in Module 13c.

## Why This Matters on the Job

Random Forest and gradient boosting (next lesson) are, together, the most widely used "traditional" (non-deep-learning) machine learning algorithms in real production systems — they consistently outperform single models like a lone decision tree or logistic regression on messy, real-world tabular data, while remaining far faster to train than deep learning. Understanding *why* combining many models helps (not just how to call the API) is what lets you reason about when ensembles are the right tool.

---

## The Core Idea: Ensemble Methods

An **ensemble method** combines predictions from multiple individual models ("weak learners") to produce a single, typically more accurate and more stable prediction than any one model alone.

💡 **Analogy:** Think of asking one expert for their opinion vs. polling a large panel of experts and taking the majority view (or average). Any single expert might be biased or simply wrong in a specific case, but errors across many independent experts tend to cancel out, while their shared correct insights reinforce each other. Ensembles apply this exact idea to models.

There are two major ensemble strategies, covered across this and the next lesson:

| Strategy | Idea | Example |
|---|---|---|
| **Bagging** (this lesson) | Train many models *independently* (often in parallel) on different random subsets of data, then average/vote their predictions | Random Forest |
| **Boosting** (next lesson) | Train models *sequentially*, each one specifically correcting the previous ones' mistakes | XGBoost, LightGBM |

## Recalling Module 13c's Overfitting Problem

Recall the synthetic, noisy dataset from Module 13c, where a single fully-grown decision tree overfit badly — perfect training accuracy but poor test accuracy:

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

tree = DecisionTreeClassifier(random_state=42)
tree.fit(X_train, y_train)
print(f"Single tree — train: {accuracy_score(y_train, tree.predict(X_train)):.4f}, "
      f"test: {accuracy_score(y_test, tree.predict(X_test)):.4f}")
```
```
Single tree — train: 1.0000, test: 0.6333
```

A single decision tree has high **variance** (Module 13c) — it's very sensitive to the specific training data it saw, memorizing noise along with real patterns. Bagging directly targets this weakness.

## Bagging: Bootstrap Aggregating

**Bagging** (short for **B**ootstrap **Agg**regating) trains many independent copies of the same model type, each on a different random sample (with replacement — a "bootstrap sample") of the training data, then combines their predictions by voting (classification) or averaging (regression).

## Random Forest: Bagging Applied to Decision Trees

**Random Forest** is bagging specifically applied to decision trees, with one extra trick: each tree also only considers a random *subset of features* at each split, further increasing diversity among the trees.

```python
from sklearn.ensemble import RandomForestClassifier

forest = RandomForestClassifier(n_estimators=100, random_state=42)
forest.fit(X_train, y_train)

print(f"Random Forest — train: {accuracy_score(y_train, forest.predict(X_train)):.4f}, "
      f"test: {accuracy_score(y_test, forest.predict(X_test)):.4f}")
```
```
Random Forest — train: 1.0000, test: 0.7667
```

**How it works:** `n_estimators=100` trains 100 individual decision trees, each on a different bootstrap sample of the training data, each considering only a random subset of features at each split. The forest's final prediction is the majority vote across all 100 trees. Notice: test accuracy jumped from `0.6333` (single tree) to `0.7667` (100-tree forest) — a substantial, concrete improvement, directly solving the overfitting problem from Module 13c. Training accuracy is still `1.0`, but that's now much less concerning, since the *test* performance (what actually matters) improved significantly.

**Why this works:** Each individual tree still overfits to its own particular bootstrap sample, but since every tree sees *different* random noise, their individual errors tend to be uncorrelated — averaging (voting) across many such trees cancels out much of that noise while preserving the real, shared signal every tree independently discovered.

🎯 **On the job:** Random Forest is frequently the strong, reliable "default" model to try first on a new tabular dataset — it requires very little preprocessing (no scaling needed, exactly like single decision trees from Module 13a), handles both numeric and categorical-encoded features well, and rarely performs *badly*, even without careful tuning.

## Feature Importance

Random Forest can report which features contributed most to its predictions — a form of interpretability, similar in spirit to Module 12c's linear regression coefficients, but computed very differently.

```python
import pandas as pd

importances = forest.feature_importances_
feature_importance_df = pd.DataFrame({
    "feature": [f"feature_{i}" for i in range(X.shape[1])],
    "importance": importances
}).sort_values("importance", ascending=False)

print(feature_importance_df.head())
```

**How it works:** `.feature_importances_` scores each feature by how much it reduced impurity (roughly, how "useful" it was for correctly splitting data) across all trees in the forest, averaged and normalized to sum to 1. Unlike linear regression's coefficients (Module 12c), which represent a direct, signed mathematical relationship, Random Forest importances only indicate *relative usefulness for prediction* — they don't tell you the direction of the effect (positive or negative), and they're less directly interpretable in plain business language.

⚠️ **Warning:** Feature importance from Random Forest can be misleading when features are highly correlated with each other — importance may get "split" between correlated features, making each look less important individually than a single, non-correlated equivalent feature would. Interpret feature importances as a useful *hint*, not a definitive causal explanation.

## Random Forest for Regression

Everything above applies identically to regression, just swapping the class:

```python
from sklearn.ensemble import RandomForestRegressor

forest_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
forest_regressor.fit(X_train, y_train)   # y_train would be continuous here, not classes
predictions = forest_regressor.predict(X_test)
```

---

## Hands-On Exercise

**Task:** Write `random_forest_practice.py` that:
1. Loads `load_wine()` from `sklearn.datasets` and splits 80/20 with `random_state=42`.
2. Trains a single `DecisionTreeClassifier` (default settings) and a `RandomForestClassifier` with `n_estimators=100`, both with `random_state=42`.
3. Prints train and test accuracy for both models.
4. Prints the top 5 most important features from the Random Forest, using `wine.feature_names`.
5. Writes a one-sentence comparison of the two models' generalization gap (train minus test accuracy).

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42
)

tree = DecisionTreeClassifier(random_state=42)
tree.fit(X_train, y_train)
tree_train_acc = accuracy_score(y_train, tree.predict(X_train))
tree_test_acc = accuracy_score(y_test, tree.predict(X_test))

forest = RandomForestClassifier(n_estimators=100, random_state=42)
forest.fit(X_train, y_train)
forest_train_acc = accuracy_score(y_train, forest.predict(X_train))
forest_test_acc = accuracy_score(y_test, forest.predict(X_test))

print(f"Tree: train={tree_train_acc:.4f}, test={tree_test_acc:.4f}, gap={tree_train_acc - tree_test_acc:.4f}")
print(f"Forest: train={forest_train_acc:.4f}, test={forest_test_acc:.4f}, gap={forest_train_acc - forest_test_acc:.4f}")

importance_df = pd.DataFrame({
    "feature": wine.feature_names,
    "importance": forest.feature_importances_
}).sort_values("importance", ascending=False)
print(importance_df.head())
```

**Expected outcome:** On the (fairly clean) Wine dataset, both models likely perform well and close to each other, since this dataset doesn't overfit as dramatically as Module 13c's synthetic noisy example — but the Random Forest should still show an equal or smaller train/test gap, consistent with its general variance-reduction property.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Assuming Random Forest is immune to overfitting | It reduces variance significantly but isn't magic — very correlated trees or too little data can still overfit |
| Interpreting feature importance as a signed, causal effect | It only reflects relative predictive usefulness, not direction or causation |
| Scaling features before Random Forest | Unnecessary — tree-based models don't need scaling (Module 13a) |
| Using very few trees (`n_estimators`) | More trees generally improve stability, at the cost of training time — 100+ is a common starting point |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand the general ensemble idea and the bagging vs. boosting distinction
- [ ] Can explain why Random Forest reduces variance compared to a single tree
- [ ] Can train `RandomForestClassifier`/`RandomForestRegressor`
- [ ] Can interpret (and appropriately caveat) feature importance
- [ ] Completed the `random_forest_practice.py` exercise

**Next:** Continue to [`02-gradient-boosting.md`](02-gradient-boosting.md)
