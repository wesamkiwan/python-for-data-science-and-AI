# 🎤 Module 15 Interview Prep: Ensemble Methods & Advanced ML

## Conceptual Questions

### 🟢 Beginner

**Q: What is an ensemble method, in plain terms?**
> A: An ensemble method combines predictions from multiple individual models to produce one final prediction that's typically more accurate and more stable than any single model alone — similar to polling a panel of experts rather than trusting just one opinion. Random Forest and gradient boosting (XGBoost/LightGBM) are the two most common ensemble approaches for tabular data.

**Q: How does Random Forest reduce overfitting compared to a single decision tree?**
> A: A single decision tree, especially if grown fully, can memorize noise specific to its training data (high variance). Random Forest trains many trees, each on a different random bootstrap sample of the data and considering only a random subset of features at each split, then averages/votes across all of them. Because each tree overfits to different, largely uncorrelated noise, averaging cancels much of that noise out while preserving the real signal every tree independently discovered.

**Q: What's the difference between a parameter and a hyperparameter?**
> A: A parameter is learned automatically by the model during training — like a linear regression's coefficients or a decision tree's actual split thresholds. A hyperparameter is a setting you choose *before* training that controls how the model learns — like the number of trees in a forest or a tree's maximum depth — and isn't derived from the data itself.

### 🟡 Intermediate

**Q: Explain the core difference between bagging and boosting.**
> A: Bagging trains many models independently and in parallel, each on a different random sample of the data, then combines their predictions by averaging/voting — its main benefit is reducing variance. Boosting trains models sequentially, where each new model is specifically built to correct the mistakes of the previous ones — it can reduce both bias and variance, often achieving higher accuracy, but tends to be more sensitive to hyperparameter choices and can overfit if not tuned carefully.

**Q: Why might you choose `RandomizedSearchCV` over `GridSearchCV`?**
> A: `GridSearchCV` tries every combination of specified hyperparameter values, which grows combinatorially as you add more hyperparameters or values — quickly becoming impractically slow. `RandomizedSearchCV` instead samples a fixed number of random combinations, letting you control the total search budget directly (`n_iter`) regardless of how large the underlying search space is — usually finding a comparably good result in a fraction of the time, especially useful with many hyperparameters or continuous ranges.

**Q: What's a limitation of feature importance from a Random Forest or gradient boosting model?**
> A: It only reflects each feature's relative contribution to predictive accuracy across the ensemble's trees — it doesn't indicate the *direction* of the effect (unlike a linear regression coefficient's sign) and doesn't imply causation. It can also be misleading when features are highly correlated, since importance can get "split" between them, making each look individually less important than a single, uncorrelated equivalent feature would.

## Practical/Coding Questions

**Q: Write code to train a Random Forest and print its top 5 most important features, given a DataFrame `X` with named columns.**
```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

importance_df = pd.DataFrame({
    "feature": X.columns,
    "importance": model.feature_importances_
}).sort_values("importance", ascending=False)

print(importance_df.head())
```
> Explanation: `.feature_importances_` returns one score per feature, in the same order as the training columns; pairing them with column names and sorting gives a readable ranked list.

**Q: Write code that uses `RandomizedSearchCV` to tune an XGBoost classifier's `max_depth` and `n_estimators`, then reports the best parameters and final test accuracy.**
```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint
import xgboost as xgb

param_distributions = {
    "max_depth": randint(3, 10),
    "n_estimators": randint(50, 300)
}

search = RandomizedSearchCV(
    xgb.XGBClassifier(random_state=42, eval_metric="logloss"),
    param_distributions, n_iter=15, cv=5, random_state=42
)
search.fit(X_train, y_train)

print(f"Best params: {search.best_params_}")
print(f"Test accuracy: {search.score(X_test, y_test):.4f}")
```
> Explanation: `randint(low, high)` defines a range to sample integer hyperparameter values from; `RandomizedSearchCV` handles cross-validating each of the `n_iter` random combinations and automatically retains the best-performing one for the final `.score()` call.

## Scenario Questions

**Q: You need to choose between Random Forest and XGBoost for a new tabular classification project with limited time for tuning. What would you consider?**
> A: Random Forest is a safer, lower-effort starting point — it performs reasonably well with default settings and is less prone to badly overfitting even without careful tuning. XGBoost can often achieve higher accuracy, but tends to need more careful hyperparameter tuning (learning rate, depth, number of estimators) to realize that advantage, and can overfit more readily if left at defaults on a tricky dataset. Given limited tuning time, I'd likely start with Random Forest as a strong baseline, then try XGBoost with at least a modest randomized hyperparameter search if time allows, comparing both on held-out data before choosing.

**Q: A model tuned with `GridSearchCV` performs great on cross-validation but disappoints once deployed on new production data. What would you investigate?**
> A: I'd first check whether the test set (used for the final, honest evaluation) was genuinely held out and untouched throughout the entire tuning process — if hyperparameters were inadvertently selected based on test-set performance rather than purely cross-validation on training data, that constitutes a form of leakage. I'd also consider whether the production data has drifted from the original training distribution (a different underlying population than what the model was tuned on), which cross-validation on historical data can't detect.

## "Gotcha" Questions

**Q: A colleague evaluates several hyperparameter combinations directly against the test set to pick the "best" one, then reports that test score as the model's final performance. What's wrong with this?**
> A: By using the test set to *choose* between hyperparameter combinations, the test set has effectively become part of the model selection process — it's no longer a genuinely held-out, unseen evaluation. The reported "final" score is optimistically biased, since the chosen combination was specifically selected for performing well on that exact test set. The correct approach is to select hyperparameters using cross-validation on the training data only (via `GridSearchCV`/`RandomizedSearchCV`), and evaluate the single, final chosen model on the test set exactly once.

**Q: Two ensemble models — one bagging, one boosting — both show high training accuracy. Why might that alone not tell you which will generalize better?**
> A: High training accuracy alone doesn't reveal how well a model generalizes to new data — both bagging and boosting can achieve near-perfect training scores while differing substantially in their test/validation performance, since they arrive at that training fit through very different mechanisms (variance reduction vs. sequential error correction). Comparing training scores alone can't distinguish "learned real patterns well" from "overfit training noise" — you need test or cross-validation scores for that.

## Quick-Fire Rapid Review

- Q: Bagging trains models how? → **independently, in parallel**
- Q: Boosting trains models how? → **sequentially, each correcting prior errors**
- Q: Ensemble method Random Forest is an example of? → **bagging**
- Q: XGBoost/LightGBM are examples of? → **boosting**
- Q: Is scaling required before tree-based ensemble models? → **No**
- Q: Tool for exhaustive hyperparameter search? → **`GridSearchCV`**
- Q: Tool for sampled, faster hyperparameter search? → **`RandomizedSearchCV`**
- Q: Does feature importance indicate the direction (positive/negative) of an effect? → **No**
