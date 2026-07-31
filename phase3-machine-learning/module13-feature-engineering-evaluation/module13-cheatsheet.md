# 📋 Module 13 Cheat Sheet: Feature Engineering & Model Evaluation

Fast reference for scaling, encoding, pipelines, and model evaluation.

## Feature Scaling
```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

StandardScaler().fit_transform(X)    # mean 0, std 1 -- default choice
MinMaxScaler().fit_transform(X)         # fixed [0, 1] range
```
✅ Needed for: logistic regression, KNN, neural networks. ⚠️ Usually NOT needed for tree-based models.

## Encoding Categorical Variables
```python
pd.get_dummies(df, columns=["col"])                 # one-hot, nominal (no order)
OneHotEncoder().fit_transform(df[["col"]])              # scikit-learn equivalent, pipeline-friendly

OrdinalEncoder(categories=[["low","med","high"]])          # ordinal, EXPLICIT order required
```
⚠️ `LabelEncoder` assigns alphabetical order by default — don't use it for genuinely ordered categories.

## Data Leakage — The Golden Rule
```python
# ✅ Split FIRST
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # fit_transform on TRAIN only
X_test_scaled = scaler.transform(X_test)             # transform only on TEST (reuses train stats)
```
⚠️ Never `.fit()` or `.fit_transform()` any preprocessing step on the full dataset before splitting.

## Pipeline
```python
from sklearn.pipeline import Pipeline

pipeline = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression())
])
pipeline.fit(X_train, y_train)        # scales train, then fits model
pipeline.score(X_test, y_test)           # transforms test with TRAIN stats, then scores
```

## ColumnTransformer (mixed numeric + categorical)
```python
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), ["age", "income"]),
    ("cat", OneHotEncoder(), ["city"])
])
full_pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", LogisticRegression())])
```

## Cross-Validation
```python
from sklearn.model_selection import cross_val_score

scores = cross_val_score(pipeline, X, y, cv=5)    # ALWAYS pass the full pipeline, not just the model
scores.mean()      # overall performance estimate
scores.std()          # how much performance varies by fold
```

## Overfitting vs. Underfitting

| | Train score | Test score | Fix |
|---|---|---|---|
| Underfitting | Low | Low | More complex model, more/better features |
| Good fit | High | High (close to train) | — |
| Overfitting | High | Noticeably lower | Simpler model, more data, regularization, more folds in CV |

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `ConvergenceWarning` on logistic regression | Unscaled features | Add `StandardScaler` to a `Pipeline` |
| Suspiciously perfect/near-perfect test score | Possible data leakage (scaled/encoded before split) | Verify split happens before any `.fit()`/`.fit_transform()` |
| Great train score, much worse test score | Overfitting | Reduce model complexity, get more data, or regularize |
| Poor score on both train and test | Underfitting | Increase model complexity or improve features |
| `LabelEncoder` gives a "wrong-looking" order | Alphabetical default, not your intended order | Use `OrdinalEncoder(categories=[[...]])` instead |

## The "New Model" Preprocessing Workflow
1. Split `X`/`y` into train/test FIRST.
2. Identify numeric vs. categorical columns.
3. Build a `Pipeline` (+ `ColumnTransformer` if mixed types) with scaling/encoding + the model.
4. `pipeline.fit(X_train, y_train)` — never fit preprocessing separately on the full dataset.
5. Evaluate with cross-validation (`cross_val_score(pipeline, ...)`), not just one split.
6. Compare train vs. test/CV performance — watch for overfitting or underfitting.
