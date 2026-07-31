# 📋 Module 12 Cheat Sheet: ML Foundations (scikit-learn)

Fast reference for the supervised learning workflow, classification, and regression.

## The Universal scikit-learn Pattern
```python
from sklearn.some_module import SomeModel

model = SomeModel()             # 1. create
model.fit(X_train, y_train)        # 2. train
model.predict(X_test)                 # 3. predict
model.score(X_test, y_test)              # (or) evaluate directly
```
Works identically for every scikit-learn algorithm — swap the class, keep the rest.

## Features & Target
```python
X = df.drop(columns=["target_col"])    # features (inputs)
y = df["target_col"]                      # target (what you're predicting)
```
| Predicting... | Type |
|---|---|
| A category (spam/not spam, species) | Classification |
| A number (price, quantity) | Regression |

## Train/Test Split
```python
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
```
⚠️ Never evaluate on data the model was trained on.

## Built-in Datasets (bundled, no download)
```python
from sklearn.datasets import load_iris, load_wine
data = load_iris()
data.data          # features array
data.target           # target array
data.feature_names       # column names
data.target_names           # class label names (classification only)
```
`fetch_california_housing()` — regression dataset, downloads on first use, then caches.

## Classification
```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier

model = LogisticRegression(max_iter=200)   # or KNeighborsClassifier()
model.fit(X_train, y_train)
predictions = model.predict(X_test)
probabilities = model.predict_proba(X_test)   # confidence per class
```

### Classification Metrics
```python
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

accuracy_score(y_test, predictions)
confusion_matrix(y_test, predictions)              # rows=true, cols=predicted
classification_report(y_test, predictions, target_names=data.target_names)
```
| Metric | Answers |
|---|---|
| Accuracy | Overall fraction correct (misleading if classes are imbalanced) |
| Precision | Of predicted positives, how many were actually positive? |
| Recall | Of actual positives, how many did we catch? |
| F1 | Harmonic mean of precision and recall |

## Regression
```python
from sklearn.linear_model import LinearRegression

model = LinearRegression()
model.fit(X_train, y_train)
predictions = model.predict(X_test)

model.coef_          # one coefficient per feature
model.intercept_        # baseline value
```

### Regression Metrics
```python
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

mse = mean_squared_error(y_test, predictions)
rmse = np.sqrt(mse)                                  # same units as target -- most interpretable
mae = mean_absolute_error(y_test, predictions)          # less sensitive to outliers than RMSE
r2 = r2_score(y_test, predictions)                         # proportion of variance explained (0-1, can go negative)
```

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `ConvergenceWarning` on `LogisticRegression` | Features on very different scales | Scale features (`StandardScaler`, Module 13) — raising `max_iter` alone often isn't enough |
| Perfect/near-perfect accuracy | Toy dataset (iris/wine) — not typical of real data | Expect messier results on real-world data |
| `.predict()` fails on a single new sample | Passed a flat list instead of a 2D array | Wrap it: `model.predict([[val1, val2, ...]])` |
| High accuracy but model seems useless in practice | Imbalanced classes | Check precision/recall/F1, not just accuracy |
| Coefficients seem to contradict "importance" intuition | Features aren't on comparable scales | Scale features before comparing coefficient magnitudes |

## The "New ML Model" Workflow — do this every time
1. Identify: classification (category) or regression (number)?
2. Split `X`/`y`, then `train_test_split` — before any data-dependent preprocessing.
3. `model = SomeAlgorithm()` → `.fit(X_train, y_train)`.
4. Evaluate on the **test** set only: accuracy/confusion matrix/classification report (classification) or RMSE/MAE/R² (regression).
5. Only after evaluating honestly, use `.predict()` on genuinely new data.
