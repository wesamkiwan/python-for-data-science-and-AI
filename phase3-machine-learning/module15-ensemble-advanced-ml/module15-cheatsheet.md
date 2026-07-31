# 📋 Module 15 Cheat Sheet: Ensemble Methods & Advanced ML

Fast reference for Random Forest, gradient boosting, and hyperparameter tuning.

## Ensemble Strategy Comparison

| | Bagging (Random Forest) | Boosting (XGBoost/LightGBM) |
|---|---|---|
| Training | Independent, parallel | Sequential, each corrects prior errors |
| Reduces | Variance (overfitting) | Bias and variance |
| Tuning sensitivity | Lower | Higher |
| Scaling needed? | No (tree-based) | No (tree-based) |

## Random Forest
```python
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

forest = RandomForestClassifier(n_estimators=100, random_state=42)
forest.fit(X_train, y_train)
forest.predict(X_test)
forest.feature_importances_    # relative usefulness, NOT signed/causal
```

## XGBoost
```python
import xgboost as xgb

model = xgb.XGBClassifier(n_estimators=100, random_state=42, eval_metric="logloss")
# xgb.XGBRegressor for regression
model.fit(X_train, y_train)
model.predict(X_test)
model.feature_importances_
```

## LightGBM
```python
import lightgbm as lgb

model = lgb.LGBMClassifier(n_estimators=100, random_state=42, verbose=-1)
# lgb.LGBMRegressor for regression
model.fit(X_train, y_train)
```

## Hyperparameters vs. Parameters
| | Learned from data? | Example |
|---|---|---|
| Parameter | Yes, during `.fit()` | Linear regression coefficients, tree split thresholds |
| Hyperparameter | No, set by you beforehand | `n_estimators`, `max_depth`, `learning_rate` |

## GridSearchCV (exhaustive)
```python
from sklearn.model_selection import GridSearchCV

param_grid = {"n_estimators": [50, 100, 200], "max_depth": [3, 5, None]}
search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, scoring="accuracy")
search.fit(X_train, y_train)

search.best_params_       search.best_score_       search.score(X_test, y_test)
```

## RandomizedSearchCV (sampled, faster)
```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

param_distributions = {"n_estimators": randint(50, 300), "learning_rate": uniform(0.01, 0.3)}
search = RandomizedSearchCV(model, param_distributions, n_iter=15, cv=5, random_state=42)
search.fit(X_train, y_train)
```

| | GridSearchCV | RandomizedSearchCV |
|---|---|---|
| Coverage | Every combination | Random sample (`n_iter` controls how many) |
| Use when | Few hyperparameters, small ranges | Many hyperparameters / continuous ranges |

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Random Forest still overfits | Too few trees, or trees too deep with correlated features | Increase `n_estimators`, limit `max_depth` |
| Boosting model overfits more than expected | Boosting is more sensitive to hyperparameters than bagging | Tune `learning_rate`/`max_depth`/`n_estimators` via search |
| `GridSearchCV` extremely slow | Too many hyperparameter combinations | Switch to `RandomizedSearchCV`, or narrow the grid |
| Feature importance seems to contradict domain knowledge | Correlated features split importance between them | Treat importance as relative/directionless, investigate correlated groups |
| Tuned model doesn't beat the default | Defaults were already close to optimal for this data | Always compare against an untuned baseline — this is a valid, useful result |

## The "Advanced Model" Workflow
1. Baseline with a single model (Module 12-14) to know what you're improving on.
2. Try Random Forest (bagging) — usually a strong, low-effort improvement.
3. Try XGBoost/LightGBM (boosting) — often better still, more tuning-sensitive.
4. Tune the winner with `RandomizedSearchCV` (broad) then optionally `GridSearchCV` (narrow).
5. Evaluate the final chosen model on the untouched test set exactly once.
