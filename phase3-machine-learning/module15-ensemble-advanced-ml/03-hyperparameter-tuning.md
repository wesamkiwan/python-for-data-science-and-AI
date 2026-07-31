# Module 15c: Hyperparameter Tuning

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [02-gradient-boosting.md](02-gradient-boosting.md)

## 🎯 Learning Objectives
- [ ] Explain what a hyperparameter is and how it differs from a learned model parameter
- [ ] Use `GridSearchCV` to systematically search for the best hyperparameters
- [ ] Use `RandomizedSearchCV` as a faster alternative for larger search spaces
- [ ] Combine hyperparameter tuning with everything learned across Phase 3

---

## Module Goal

Close out Phase 3 by learning to systematically tune a model's **hyperparameters** — the settings you choose *before* training (like `n_estimators` or `max_depth`) — rather than manually guessing values, using scikit-learn's built-in search tools combined with the cross-validation from Module 13c.

## Why This Matters on the Job

Every model in this course had settings you could adjust — `n_neighbors` for KNN, `max_depth` for a tree, `n_estimators` for a forest — and the "right" values depend entirely on the specific dataset. Manually guessing-and-checking these is slow and unreliable; automated hyperparameter search is the standard professional practice for squeezing meaningfully better performance out of a model you've already chosen.

---

## Hyperparameters vs. Parameters

- **Parameters:** values the model *learns* automatically during `.fit()` — like `LinearRegression`'s coefficients (Module 12c) or a decision tree's actual split thresholds.
- **Hyperparameters:** values *you* set before training, controlling how the model learns — `n_estimators`, `max_depth`, `learning_rate`, etc. These aren't learned from data; you choose them, ideally through systematic search rather than guesswork.

## `GridSearchCV`: Exhaustive Search

`GridSearchCV` tries **every combination** of a specified set of hyperparameter values, using cross-validation (Module 13c) to evaluate each combination fairly.

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier

wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.2, random_state=42)

param_grid = {
    "n_estimators": [50, 100, 200],
    "max_depth": [3, 5, None],
    "min_samples_split": [2, 5]
}

grid_search = GridSearchCV(
    RandomForestClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring="accuracy"
)
grid_search.fit(X_train, y_train)

print(f"Best params: {grid_search.best_params_}")
print(f"Best CV score: {grid_search.best_score_:.4f}")
print(f"Test score with best model: {grid_search.score(X_test, y_test):.4f}")
```
```
Best params: {'max_depth': 5, 'min_samples_split': 2, 'n_estimators': 100}
Best CV score: 0.9786
Test score with best model: 1.0000
```

**How it works:** `param_grid` defines the hyperparameter values to try — here, `3 × 3 × 2 = 18` total combinations. `GridSearchCV` runs 5-fold cross-validation (Module 13c) on *every* one of those 18 combinations (90 total model fits!), tracking each combination's mean CV score. `grid_search.best_params_` reveals the winning combination; `grid_search` itself then behaves like the best-found model, so `grid_search.score(X_test, y_test)` directly evaluates it on the held-out test set.

⚠️ **Warning:** `GridSearchCV`'s exhaustive search grows *combinatorially* — adding one more hyperparameter with 3 values multiplies your total combinations by 3, and each combination requires a full cross-validation run. This becomes impractically slow with more than a handful of hyperparameters/values, which is exactly the problem the next tool solves.

## `RandomizedSearchCV`: Sampling Instead of Exhausting

`RandomizedSearchCV` samples a fixed number of *random* combinations from the specified ranges, rather than trying every single one — usually finding a nearly-as-good result in a fraction of the time.

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint

param_distributions = {
    "n_estimators": randint(50, 300),
    "max_depth": [3, 5, 10, None],
    "min_samples_split": randint(2, 10)
}

random_search = RandomizedSearchCV(
    RandomForestClassifier(random_state=42),
    param_distributions,
    n_iter=10,          # try only 10 random combinations, not every possibility
    cv=5,
    random_state=42,
    scoring="accuracy"
)
random_search.fit(X_train, y_train)

print(f"Best params (random search): {random_search.best_params_}")
print(f"Best CV score (random search): {random_search.best_score_:.4f}")
```
```
Best params (random search): {'max_depth': 10, 'min_samples_split': 4, 'n_estimators': 121}
Best CV score (random search): 0.9786
```

**How it works:** `randint(50, 300)` defines a *range* (not a fixed list) to sample from randomly — `RandomizedSearchCV` picks `n_iter=10` random combinations from the defined distributions/lists and cross-validates each, rather than exhaustively trying every possibility. Here, it found a different combination than `GridSearchCV`, but reached the *same* best CV score (`0.9786`) — a reminder that there's often more than one "good enough" hyperparameter setting, and random search frequently finds a comparably good result far faster than an exhaustive grid.

| | `GridSearchCV` | `RandomizedSearchCV` |
|---|---|---|
| Coverage | Every combination — guaranteed to find the best *within the grid* | A random sample — may miss the absolute best, but usually finds something close |
| Speed | Slow, grows combinatorially with more hyperparameters | Fast, controlled directly by `n_iter` regardless of grid size |
| Use when | Few hyperparameters, small value ranges | Many hyperparameters and/or large/continuous ranges |

✅ **Best Practice:** Start with `RandomizedSearchCV` for an initial, broad exploration (especially with several hyperparameters or continuous ranges), then optionally narrow to a focused `GridSearchCV` around the promising region it found, for a final, more exhaustive pass.

## Putting Phase 3 Together: A Complete Workflow

This is a natural moment to see everything from Phase 3 combined:

```python
# 1. Split (Module 12a)
X_train, X_test, y_train, y_test = train_test_split(wine.data, wine.target, test_size=0.2, random_state=42)

# 2. (Scaling/encoding would go here if needed, via Pipeline -- Module 13a/13b)

# 3. Hyperparameter search WITH cross-validation (Module 13c + this lesson)
search = RandomizedSearchCV(RandomForestClassifier(random_state=42), param_distributions, n_iter=10, cv=5, random_state=42)
search.fit(X_train, y_train)

# 4. Final, honest evaluation on the untouched test set
final_score = search.score(X_test, y_test)
print(f"Final test score: {final_score:.4f}")
```

⚠️ **Warning:** The test set must remain completely untouched throughout the entire search process — all cross-validation during hyperparameter search happens *within* the training data only. Only after the search is fully complete do you evaluate the single, final chosen model on the test set, exactly once, for an honest final performance estimate.

---

## Hands-On Exercise

**Task:** Write `hyperparameter_tuning_practice.py` that:
1. Loads `load_wine()`, splits 80/20 with `random_state=42`.
2. Defines a `param_distributions` dict for `XGBClassifier` covering `n_estimators` (randint 50-300), `max_depth` (list: `[3, 5, 7, 10]`), and `learning_rate` (use `scipy.stats.uniform(0.01, 0.3)`).
3. Runs `RandomizedSearchCV` with `n_iter=15`, `cv=5`, `random_state=42`.
4. Prints the best parameters, best CV score, and final test score.
5. Compares the tuned model's test score against an untuned `XGBClassifier(random_state=42)` (default settings) trained on the same split.

<details>
<summary>✅ Click to see the solution</summary>

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import accuracy_score
from scipy.stats import randint, uniform
import xgboost as xgb

wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42
)

param_distributions = {
    "n_estimators": randint(50, 300),
    "max_depth": [3, 5, 7, 10],
    "learning_rate": uniform(0.01, 0.3)
}

search = RandomizedSearchCV(
    xgb.XGBClassifier(random_state=42, eval_metric="logloss"),
    param_distributions,
    n_iter=15,
    cv=5,
    random_state=42,
    scoring="accuracy"
)
search.fit(X_train, y_train)

print(f"Best params: {search.best_params_}")
print(f"Best CV score: {search.best_score_:.4f}")
print(f"Tuned test score: {search.score(X_test, y_test):.4f}")

default_model = xgb.XGBClassifier(random_state=42, eval_metric="logloss")
default_model.fit(X_train, y_train)
default_test_score = accuracy_score(y_test, default_model.predict(X_test))
print(f"Untuned (default) test score: {default_test_score:.4f}")
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Tuning hyperparameters using the test set | Only cross-validate on training data during search; evaluate on test once, at the end |
| Using `GridSearchCV` with many hyperparameters/values | Switch to `RandomizedSearchCV`, or narrow the grid first |
| Assuming tuning always yields a big improvement | Sometimes default settings are already close to optimal — always compare against a baseline |
| Forgetting `cv=` inside the search (relying on defaults blindly) | Set it explicitly and match your Module 13c cross-validation reasoning |

---

## ✅ Module 15 Completion Checklist
- [ ] Understand the difference between parameters and hyperparameters
- [ ] Can use `GridSearchCV` for exhaustive hyperparameter search
- [ ] Can use `RandomizedSearchCV` for faster search over larger spaces
- [ ] Understand when to prefer each search strategy
- [ ] Completed the `hyperparameter_tuning_practice.py` exercise
- [ ] Reviewed [`module15-cheatsheet.md`](module15-cheatsheet.md)
- [ ] Reviewed [`module15-interview.md`](module15-interview.md)
- [ ] Browsed [`module15-references.md`](module15-references.md)

**Next Step:** Capstone 1 — End-to-end EDA + ML Project (`capstones/`), or continue to Module 16 — Deep Learning Foundations (`phase4-deep-learning-and-ai/module16-deep-learning-foundations/`)

---

## 🎉 Phase 3 Complete!

You've finished **Phase 3: Machine Learning** — you can now build, evaluate, and tune supervised models (classification and regression), find hidden structure with unsupervised learning, and apply industry-standard ensemble methods (Random Forest, XGBoost, LightGBM). This is the core, most job-relevant skillset in classical data science. Capstone 1 is now unlockable, applying everything from Phases 2-3 to a real, portfolio-worthy project — and Phase 4 (Deep Learning & AI) awaits whenever you're ready to go further.
