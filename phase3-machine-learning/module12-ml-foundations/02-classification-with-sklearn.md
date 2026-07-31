# Module 12b: Classification with scikit-learn

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [01-supervised-learning-basics.md](01-supervised-learning-basics.md)

## 🎯 Learning Objectives
- [ ] Train a classification model with `LogisticRegression`
- [ ] Evaluate a classifier with accuracy, a confusion matrix, and a classification report
- [ ] Use a trained model to predict on brand-new, unseen data
- [ ] Understand precision, recall, and F1-score at a conceptual level

---

## Module Goal

Train and properly evaluate your first real classification model — predicting a category from numeric features — and learn the standard metrics used to judge how good a classifier actually is, beyond a single accuracy number.

## Why This Matters on the Job

"Is this transaction fraudulent?" "Will this customer churn?" "Which category does this support ticket belong to?" — these are all classification problems, among the most common real-world ML applications. Accuracy alone is often misleading (imagine a fraud detector that just predicts "not fraud" every time — it'd have high accuracy but be completely useless), so understanding precision, recall, and the confusion matrix is essential for judging whether a classifier is actually good for its intended purpose.

---

## Training a Classifier: `LogisticRegression`

Despite the name, **logistic regression** is a classification algorithm (a historical naming quirk) — it predicts the probability of each class and picks the most likely one.

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

iris = load_iris()
X, y = iris.data, iris.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

predictions = model.predict(X_test)
print(predictions)
```

**How it works:** Exactly the pattern from the last lesson — create the model, `.fit()` it on training data, `.predict()` on the test set. `max_iter=200` raises the internal optimization step limit (the default sometimes isn't enough for this algorithm to fully converge on some datasets — scikit-learn will warn you if this happens).

## Evaluating Accuracy

```python
from sklearn.metrics import accuracy_score

accuracy = accuracy_score(y_test, predictions)
print(f"Accuracy: {accuracy:.4f}")   # Accuracy: 1.0000
```

**How it works:** `accuracy_score()` compares predictions against the true test labels and returns the fraction correct. A perfect `1.0` here reflects that the Iris dataset is a famously "easy," well-separated classic benchmark dataset — real-world classification problems essentially never achieve perfect accuracy, so don't expect this outcome to be typical once you work with real data.

⚠️ **Warning:** Accuracy alone can be dangerously misleading, especially with **imbalanced classes** — if 95% of transactions are legitimate, a model that predicts "legitimate" for *everything* scores 95% accuracy while being completely useless at its actual job (catching fraud). This is exactly why the next two metrics matter.

## The Confusion Matrix

A **confusion matrix** shows exactly which classes get confused with which:

```python
from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, predictions)
print(cm)
```
```
[[10  0  0]
 [ 0  9  0]
 [ 0  0 11]]
```

**How it works:** Each row represents the *true* class; each column represents the *predicted* class. The diagonal (top-left to bottom-right) shows correct predictions; anything off the diagonal is a misclassification — e.g., a `2` in row 0/column 1 would mean 2 actual setosa flowers were incorrectly predicted as versicolor. This particular result is a perfect diagonal (no off-diagonal errors), again reflecting how easy this specific dataset is.

## Precision, Recall & F1-Score

```python
from sklearn.metrics import classification_report

print(classification_report(y_test, predictions, target_names=iris.target_names))
```
```
              precision    recall  f1-score   support

      setosa       1.00      1.00      1.00        10
  versicolor       1.00      1.00      1.00         9
   virginica       1.00      1.00      1.00        11

    accuracy                           1.00        30
   macro avg       1.00      1.00      1.00        30
weighted avg       1.00      1.00      1.00        30
```

**How it works, conceptually** (using a fraud-detection example, since perfectly-scored iris doesn't illustrate the tradeoff):
- **Precision:** "Of everything the model predicted as fraud, what fraction actually was fraud?" High precision means few false alarms.
- **Recall:** "Of everything that actually was fraud, what fraction did the model catch?" High recall means few missed cases.
- **F1-score:** the harmonic mean of precision and recall — a single number balancing both, useful when you need one summary metric rather than juggling two.

| Metric | Answers | Costly to get wrong when... |
|---|---|---|
| Precision | "How trustworthy are positive predictions?" | False positives are expensive (e.g., wrongly flagging a legitimate transaction) |
| Recall | "How many real positives did we catch?" | False negatives are expensive (e.g., missing actual fraud) |

🎯 **On the job:** Which metric matters most is a *business* decision, not a purely technical one — a spam filter should favor precision (don't block real emails), while a cancer-screening model should favor recall (don't miss real cases), even at the cost of more false alarms.

## Predicting on Brand-New Data

The whole point of a trained model is using it on data it's never seen:

```python
new_flower = [[5.1, 3.5, 1.4, 0.2]]   # a single new flower's measurements
prediction = model.predict(new_flower)
print(iris.target_names[prediction[0]])   # setosa

probabilities = model.predict_proba(new_flower)
print(probabilities)   # [[0.977 0.023 0.00000005]] -- model's confidence in each class
```

**How it works:** `.predict()` takes a 2D array (even for a single sample, it must be a list-of-lists, since scikit-learn always expects multiple rows of features) and returns the predicted class. `.predict_proba()` reveals the model's underlying confidence for *each* possible class — useful whenever you need more nuance than just the single "winning" prediction (e.g., "flag this for manual review if confidence is below 80%").

---

## Hands-On Exercise

**Task:** Write `classification_practice.py` that:
1. Loads `load_wine()` from `sklearn.datasets` (used in the previous lesson's exercise) and splits it 75/25 with `random_state=1`.
2. Trains a `LogisticRegression` model with `max_iter=1000`.
3. Prints the accuracy on the test set.
4. Prints the confusion matrix.
5. Prints the full classification report using `wine.target_names`.

<details>
<summary>✅ Click to see the solution</summary>

```python
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

wine = load_wine()
X, y = wine.data, wine.target

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print(f"Accuracy: {accuracy_score(y_test, predictions):.4f}")
print(confusion_matrix(y_test, predictions))
print(classification_report(y_test, predictions, target_names=wine.target_names))
```

**Expected outcome:** Accuracy around 0.96, with most misclassifications between `class_0` and `class_1`. You'll likely also see a `ConvergenceWarning` printed — the Wine dataset's features have very different scales (e.g., `proline` is in the hundreds, `hue` is 0-2), which slows this algorithm's convergence. Increasing `max_iter` alone doesn't fully fix this; the real solution is **feature scaling** (e.g., `StandardScaler`), covered in Module 13. For now, the warning is expected and the model still performs well despite it — just don't be alarmed by it.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Trusting accuracy alone, especially on imbalanced data | Always also check precision/recall/F1, or a confusion matrix |
| Assuming perfect/near-perfect accuracy is typical | Real-world data is messier — Iris/Wine are famously easy benchmark datasets |
| Passing a single flat list to `.predict()` | Wrap it in an extra list/array — scikit-learn always expects a 2D array of samples |
| Picking precision or recall as "the" metric without business context | The right tradeoff depends on which type of error is more costly for your specific problem |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Can train a `LogisticRegression` classifier
- [ ] Can evaluate with accuracy, confusion matrix, and classification report
- [ ] Understand precision vs. recall and when each matters more
- [ ] Can predict on new, unseen samples with `.predict()` and `.predict_proba()`
- [ ] Completed the `classification_practice.py` exercise

**Next:** Continue to [`03-regression-with-sklearn.md`](03-regression-with-sklearn.md)
