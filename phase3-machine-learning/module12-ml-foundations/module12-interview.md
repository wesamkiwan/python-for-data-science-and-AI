# 🎤 Module 12 Interview Prep: ML Foundations (scikit-learn)

## Conceptual Questions

### 🟢 Beginner

**Q: What's the difference between classification and regression?**
> A: Classification predicts a discrete category (spam vs. not spam, which species), while regression predicts a continuous numeric value (a price, a quantity). The distinction determines which algorithms and evaluation metrics apply — accuracy/precision/recall make sense for classification, while MSE/RMSE/R² make sense for regression.

**Q: Why do you split data into training and test sets before training a model?**
> A: If you evaluate a model on the same data it learned from, you can't tell whether it actually learned a generalizable pattern or simply memorized the training examples. Holding out a test set the model never sees during training gives an honest estimate of how it'll perform on genuinely new, real-world data.

**Q: What does `model.fit(X_train, y_train)` actually do?**
> A: It's the training step — the model examines the labeled training data (`X_train` as inputs, `y_train` as the correct answers) and adjusts its internal parameters to capture the pattern connecting them. After `.fit()`, the model object holds learned state it can then use to make predictions via `.predict()` on new data.

### 🟡 Intermediate

**Q: Why can accuracy be a misleading metric, and what would you check instead?**
> A: Accuracy can look great even for a useless model when classes are imbalanced — e.g., if only 2% of transactions are fraudulent, a model that always predicts "not fraud" scores 98% accuracy while catching zero actual fraud. I'd check precision and recall (and the confusion matrix) specifically for the minority/important class, since those reveal how the model performs on the cases that actually matter.

**Q: Explain the tradeoff between precision and recall with a concrete example.**
> A: Precision asks "of everything flagged positive, how much was actually positive?" — high precision means few false alarms. Recall asks "of everything actually positive, how much did we catch?" — high recall means few missed cases. In spam filtering, I'd prioritize precision (don't block real emails, even if a few spam messages slip through); in a medical screening test, I'd prioritize recall (don't miss a real case, even if it means more people get flagged for further, cheaper follow-up testing).

**Q: What does an R² of 0.75 mean, and does a higher R² always mean a better model?**
> A: An R² of 0.75 means the model explains about 75% of the variance in the target variable — the remaining 25% is unexplained by the features included. A higher R² generally indicates a better fit, but it's not the whole story: R² can be artificially inflated by adding more features (even irrelevant ones) without genuinely improving predictive power on new data, and it doesn't tell you the actual size of errors in real units the way RMSE/MAE do — I'd look at multiple metrics together, not R² alone.

## Practical/Coding Questions

**Q: Write code that trains a `KNeighborsClassifier`, evaluates it, and predicts the class of one new sample.**
```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)

model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

accuracy = accuracy_score(y_test, model.predict(X_test))
print(f"Accuracy: {accuracy:.4f}")

new_sample = [[5.0, 3.4, 1.5, 0.2]]
predicted_class = model.predict(new_sample)
print(iris.target_names[predicted_class[0]])
```
> Explanation: identical `.fit()`/`.predict()` pattern regardless of the specific algorithm; a new sample must be passed as a 2D array (a list containing one list of feature values) even for a single prediction.

**Q: Write code to compute and print RMSE and R² for a trained regression model, then interpret the RMSE in plain language given the target is measured in dollars.**
```python
from sklearn.metrics import mean_squared_error, r2_score
import numpy as np

rmse = np.sqrt(mean_squared_error(y_test, predictions))
r2 = r2_score(y_test, predictions)

print(f"RMSE: ${rmse:,.2f}")
print(f"R²: {r2:.4f}")
print(f"On average, predictions are off by about ${rmse:,.2f}.")
```
> Explanation: RMSE is in the same units as the target, so it can be reported directly in plain business language ("off by about $X on average"), which is usually far more useful to a stakeholder than an abstract R² or MSE number.

## Scenario Questions

**Q: A stakeholder is thrilled that your fraud detection model has 99% accuracy. How would you respond?**
> A: I'd want to see the confusion matrix and recall specifically for the fraud class before celebrating — if fraud only occurs in, say, 1% of transactions, a model that never predicts fraud at all would already achieve 99% accuracy while being completely useless. I'd present precision and recall for the fraud class specifically, since those tell the real story of whether the model is actually catching fraud, and at what cost in false alarms.

**Q: You train a linear regression model and get a very high R² on the training set, but poor performance on the test set. What's likely happening, and what would you check first?**
> A: This pattern is a classic sign of overfitting — the model has essentially memorized quirks of the training data rather than learning a pattern that generalizes. I'd double-check that the train/test split happened correctly (no data leakage), consider whether the model is too complex for the amount of data available, and look ahead to Module 13's techniques (regularization, cross-validation) for addressing this directly.

## "Gotcha" Questions

**Q: Why does `model.predict([5.1, 3.5, 1.4, 0.2])` raise an error, while `model.predict([[5.1, 3.5, 1.4, 0.2]])` works?**
> A: scikit-learn's `.predict()` always expects a 2D array — rows of samples, each with the same number of feature columns — even for a single prediction. Passing a flat 1D list is interpreted as a single "row" with no column structure and raises a shape error; wrapping it in an extra list (`[[...]]`) makes it a proper 2D array with one row.

**Q: A colleague scales their features, fits a model, and gets great results — but then reports "MedInc has the biggest coefficient, so it's clearly the most important feature," comparing it directly against an unscaled model's coefficients from a different run. What's wrong with this comparison?**
> A: Coefficient magnitudes are only directly comparable across features (or across models) when the features share a common scale. Comparing a coefficient from a model trained on unscaled data against one trained on scaled data mixes two different units of measurement — the comparison is meaningless unless both models used the same, consistent scaling approach.

## Quick-Fire Rapid Review

- Q: `X` conventionally represents...? → **features (inputs)**
- Q: `y` conventionally represents...? → **the target (what you're predicting)**
- Q: Function to split data into train/test sets? → **`train_test_split`**
- Q: Three core scikit-learn methods every model shares? → **`.fit()`, `.predict()`, `.score()`**
- Q: Metric misleading on imbalanced classes? → **accuracy**
- Q: Regression metric in the same units as the target? → **RMSE (or MAE)**
- Q: What does R² measure? → **proportion of variance in the target explained by the model**
- Q: Shape `.predict()` always expects? → **a 2D array (rows of samples)**
