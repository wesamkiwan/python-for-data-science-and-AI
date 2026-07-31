# Module 12c: Regression with scikit-learn

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [02-classification-with-sklearn.md](02-classification-with-sklearn.md)

## 🎯 Learning Objectives
- [ ] Train a regression model with `LinearRegression`
- [ ] Evaluate a regressor with MSE, RMSE, MAE, and R²
- [ ] Interpret a linear model's coefficients
- [ ] Recognize when regression is the right choice vs. classification

---

## Module Goal

Train and evaluate your first **regression** model — predicting a continuous number rather than a category — completing the two fundamental supervised learning types this module set out to cover.

## Why This Matters on the Job

"What will this house sell for?" "How many units will we sell next quarter?" "What's this customer's predicted lifetime value?" — these are all regression problems, just as common in real work as classification. The evaluation metrics here (MSE, RMSE, MAE, R²) are the standard vocabulary you'll use to judge and compare any regression model, and interpreting a linear model's coefficients is often the first thing a stakeholder asks about ("so what actually drives price the most?").

---

## Training a Regressor: `LinearRegression`

```python
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

housing = fetch_california_housing()   # downloads on first use, then caches locally
print(housing.feature_names)     # ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude']
print(housing.data.shape)          # (20640, 8) -- 20,640 California districts, 8 features each
print(housing.target.shape)           # (20640,)     -- median house value (in $100,000s) per district

X, y = housing.data, housing.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(predictions[:5])
```

**How it works:** The exact same `.fit()`/`.predict()` pattern from Modules 12a/12b — the only thing that changed is the algorithm class (`LinearRegression` instead of `LogisticRegression`/`KNeighborsClassifier`) and the fact that `y` is now a continuous number (median house value) rather than a category.

💡 **Tip:** `fetch_california_housing()` downloads its data from the internet the first time you call it (then caches it locally for future runs) — unlike `load_iris()`/`load_wine()`, which ship bundled directly with scikit-learn. If you're offline, this specific dataset won't be available until you've fetched it once with an internet connection.

## Evaluating a Regression Model

Regression can't use "accuracy" (there's no such thing as an exactly-correct numeric prediction) — instead, it measures how *far off* predictions are, on average.

```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"MSE: {mse:.4f}")     # 0.5559
print(f"RMSE: {rmse:.4f}")     # 0.7456
print(f"MAE: {mae:.4f}")         # 0.5332
print(f"R²: {r2:.4f}")              # 0.5758
```

**How it works:**
- **MSE (Mean Squared Error):** average of the squared differences between predicted and actual values. Squaring penalizes large errors disproportionately more than small ones, but the units become hard to interpret ("dollars squared").
- **RMSE (Root Mean Squared Error):** the square root of MSE, bringing the units back to the original scale — here, roughly $74,560 average error (since this target is in units of $100,000s: `0.7456 * 100,000`).
- **MAE (Mean Absolute Error):** average of the *absolute* differences — more directly interpretable than MSE/RMSE, and less sensitive to a few very large errors (echoing Module 10's mean-vs-median robustness lesson).
- **R² (R-squared):** the proportion of variance in the target the model explains, from 0 to 1 (can go negative for a model *worse* than just predicting the average every time). An R² of `0.58` here means the model explains about 58% of the variation in house values — decent for a simple linear model on real, messy data, but far from perfect.

| Metric | Units | Sensitive to outliers? |
|---|---|---|
| MSE | Squared units | Very (large errors punished heavily) |
| RMSE | Original units | Very (same reason as MSE) |
| MAE | Original units | Less |
| R² | Unitless (proportion) | Somewhat |

✅ **Best Practice:** Report RMSE or MAE (not raw MSE) when communicating results to a non-technical audience — "our model is off by about $75,000 on average" is far more meaningful than "our MSE is 0.56."

## Interpreting a Linear Model's Coefficients

```python
print(model.coef_)          # one coefficient per feature
print(model.intercept_)        # the baseline value when all features are 0

for feature_name, coefficient in zip(housing.feature_names, model.coef_):
    print(f"{feature_name}: {coefficient:.4f}")
```

**How it works:** Linear regression learns a formula: `prediction = intercept + (coef_1 × feature_1) + (coef_2 × feature_2) + ...`. Each coefficient tells you how much the predicted target changes for a one-unit increase in that feature, holding all others constant. A positive coefficient means "as this feature increases, the prediction increases"; negative means the opposite. Here, `MedInc` (median income) has the largest positive coefficient — unsurprisingly, income is the strongest driver of median house value in this dataset.

⚠️ **Warning:** Coefficient *magnitude* isn't directly comparable across features unless they're on the same scale — a coefficient of `0.44` on an income feature (measured in tens of thousands) and `-0.0000020` on population (measured in thousands of people) aren't directly comparable in "importance" without first scaling the features (Module 13's topic) — a larger-looking coefficient might just reflect a smaller-scaled feature, not a stronger real effect.

🎯 **On the job:** This coefficient interpretation is exactly what a stakeholder means by "what drives this outcome the most?" — and it's one of the reasons linear models remain popular in business settings even when more complex models (Module 15) might predict slightly better: they're directly explainable in plain language.

## Classification vs. Regression: Choosing the Right One

| Question sounds like... | Use |
|---|---|
| "Which category/class is this?" | Classification |
| "What number/amount will this be?" | Regression |
| "Will this customer churn?" (yes/no) | Classification |
| "How much will this customer spend?" ($) | Regression |

💡 **Tip:** Sometimes the same business question can be framed either way — "will this customer churn" (classification) vs. "what's this customer's probability of churning" (which could be read from a classifier's `.predict_proba()`, from Module 12b) — the right framing depends on what decision the prediction needs to support.

---

## Hands-On Exercise

**Task:** Write `regression_practice.py` that:
1. Loads `fetch_california_housing()`, splits 80/20 with `random_state=7`.
2. Trains a `LinearRegression` model.
3. Prints RMSE, MAE, and R² on the test set.
4. Prints each feature name alongside its coefficient, sorted by absolute coefficient value (largest impact first).
5. Prints a one-sentence interpretation of which feature has the strongest positive relationship with house value, and which has the strongest negative relationship.

<details>
<summary>✅ Click to see the solution</summary>

```python
from sklearn.datasets import fetch_california_housing
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

housing = fetch_california_housing()
X, y = housing.data, housing.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=7)

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, predictions))
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print(f"RMSE: {rmse:.4f}")
print(f"MAE: {mae:.4f}")
print(f"R²: {r2:.4f}")

coef_pairs = sorted(
    zip(housing.feature_names, model.coef_),
    key=lambda pair: abs(pair[1]),
    reverse=True
)
for feature_name, coefficient in coef_pairs:
    print(f"{feature_name}: {coefficient:.4f}")

strongest_positive = max(coef_pairs, key=lambda pair: pair[1])
strongest_negative = min(coef_pairs, key=lambda pair: pair[1])
print(f"{strongest_positive[0]} has the strongest positive relationship with house value.")
print(f"{strongest_negative[0]} has the strongest negative relationship with house value.")
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Reporting raw MSE to a non-technical audience | Use RMSE or MAE — same units as the target, easier to interpret |
| Comparing coefficient magnitudes across differently-scaled features | Scale features first (Module 13) before comparing "importance" this way |
| Using classification metrics (accuracy) on a regression problem | Use MSE/RMSE/MAE/R² instead — there's no "exact match" in regression |
| Assuming a high R² alone means a good model | Also check RMSE/MAE in real-world units, and validate on genuinely new data |

---

## ✅ Module 12 Completion Checklist
- [ ] Can train a `LinearRegression` model
- [ ] Can evaluate with MSE, RMSE, MAE, and R², and know when to report which
- [ ] Can interpret a linear model's coefficients
- [ ] Can decide whether a business question calls for classification or regression
- [ ] Completed the `regression_practice.py` exercise
- [ ] Reviewed [`module12-cheatsheet.md`](module12-cheatsheet.md)
- [ ] Reviewed [`module12-interview.md`](module12-interview.md)
- [ ] Browsed [`module12-references.md`](module12-references.md)

**Next Step:** Module 13 — Feature Engineering & Model Evaluation (`phase3-machine-learning/module13-feature-engineering-evaluation/`)
