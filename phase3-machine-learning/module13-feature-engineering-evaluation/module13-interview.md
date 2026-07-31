# 🎤 Module 13 Interview Prep: Feature Engineering & Model Evaluation

## Conceptual Questions

### 🟢 Beginner

**Q: Why do some machine learning algorithms need feature scaling while others don't?**
> A: Algorithms that rely on distances between points (like KNN) or gradient-based optimization (like logistic regression, neural networks) can be dominated by whichever feature happens to have the largest numeric range, even if it's not the most predictive one — scaling puts every feature on a comparable footing. Tree-based models (decision trees, random forests) split on individual feature thresholds one at a time, so the relative scale between different features doesn't affect how they build splits, making scaling generally unnecessary for them.

**Q: What's the difference between one-hot encoding and ordinal encoding, and when would you use each?**
> A: One-hot encoding creates a separate binary column per category, with no implied order — correct for nominal data like color or city, where no category is inherently "more" or "less" than another. Ordinal encoding assigns a single number per category that preserves a genuine order — correct for data like shirt size (S/M/L) or education level, where the categories do have a natural sequence a model can meaningfully use.

**Q: What is data leakage, in your own words?**
> A: Data leakage is when information that wouldn't be available at prediction time — most commonly, information from the test set — accidentally influences training, making the model's evaluation results look better than they'd actually be in real, honest use. A common example is scaling or encoding the entire dataset before splitting into train/test, which lets test-set values subtly influence the preprocessing the model trains under.

### 🟡 Intermediate

**Q: Why should you fit a scaler only on the training data, not the entire dataset?**
> A: The test set is supposed to simulate genuinely new, unseen data. If you compute scaling statistics (mean, std, min/max) using the full dataset — including the test portion — those statistics are influenced by data the model shouldn't have any knowledge of yet, which can make evaluation results overly optimistic. The correct approach is to `.fit_transform()` the scaler only on the training set, then use `.transform()` (not `.fit_transform()`) to apply those same learned statistics to the test set.

**Q: What advantage does k-fold cross-validation have over a single train/test split?**
> A: A single split gives you exactly one performance estimate, which depends heavily on which specific rows happened to land in the test set — a particularly easy or hard test set by chance can make a model look better or worse than it typically performs. K-fold cross-validation trains and evaluates the model k separate times, each with a different fold held out, giving both a more reliable average performance estimate and a sense of how much that performance varies (via the standard deviation across folds).

**Q: How would you diagnose whether a model is overfitting or underfitting just from its train and test scores?**
> A: If both training and test scores are low and similar, the model is likely underfitting — it's too simple to capture the real pattern in either dataset. If the training score is high but the test score is noticeably lower, that gap signals overfitting — the model has learned patterns (including noise) specific to the training data that don't generalize. A model that's neither should show high, similar scores on both.

## Practical/Coding Questions

**Q: Write code that correctly scales a training and test set without leakage.**
```python
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # learn AND apply on train
X_test_scaled = scaler.transform(X_test)            # apply ONLY (reuses train's learned stats)
```
> Explanation: `.fit_transform()` on the training set learns the scaling parameters from training data only; `.transform()` (without re-fitting) on the test set applies those same parameters, ensuring the test set's own values never influence the scaling itself.

**Q: Write a scikit-learn pipeline that scales numeric features, one-hot encodes a categorical feature, and trains a logistic regression model, then run 5-fold cross-validation on it.**
```python
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), ["age", "income"]),
    ("cat", OneHotEncoder(), ["city"])
])

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression())
])

scores = cross_val_score(pipeline, X, y, cv=5)
print(f"Mean accuracy: {scores.mean():.4f}")
```
> Explanation: `ColumnTransformer` routes each column type to its own preprocessing step; wrapping the whole thing in a `Pipeline` and passing that pipeline (not just the classifier) to `cross_val_score` guarantees every fold's preprocessing is fit only on that fold's training portion.

## Scenario Questions

**Q: A model achieves 99% accuracy on your test set, which seems suspiciously high for the problem. What would you investigate first?**
> A: I'd first check for data leakage — specifically, whether any preprocessing (scaling, encoding, imputing missing values, feature selection) was fit on the full dataset before the train/test split, since that's one of the most common causes of unrealistically high scores. I'd also check whether the target variable accidentally includes information that wouldn't be available at real prediction time (e.g., a feature that's essentially a proxy for the answer), and confirm the test set genuinely represents unseen, held-out data rather than overlapping with training somehow.

**Q: You're deciding between a simple model with 82% cross-validated accuracy and a complex model with 85% cross-validated accuracy, but the complex model shows a much larger gap between training (98%) and cross-validation (85%) scores. Which would you lean toward, and why?**
> A: The large train/CV gap on the complex model is a warning sign of overfitting — its cross-validated performance might degrade further on genuinely new production data that differs even slightly from what it's seen. I'd lean toward the simpler model unless the 3-point accuracy difference is business-critical, since a smaller train/test gap generally suggests more reliable, stable real-world performance — though I'd also consider whether regularization or more training data could close that gap on the complex model before ruling it out entirely.

## "Gotcha" Questions

**Q: A colleague scales their entire dataset with `StandardScaler().fit_transform(X)` before calling `train_test_split()`. Why is this a problem, even though the code runs without any error?**
> A: This is a classic, silent data-leakage bug — the scaler's mean and standard deviation get computed using every sample, including what will become the test set, meaning the "unseen" test data has already influenced the preprocessing the model is evaluated under. The code runs fine and produces a number, but that number is a dishonestly optimistic estimate of real-world performance; the fix is to split first, then `.fit_transform()` only on the training data.

**Q: Why might a decision tree with `max_depth=None` (fully grown) show perfect training accuracy but noticeably lower test accuracy?**
> A: An unrestricted decision tree can keep splitting until it perfectly separates every training example, effectively memorizing the training data (including its noise and any random quirks) rather than learning a general pattern — this is a textbook case of overfitting, showing up exactly as a large train/test performance gap.

## Quick-Fire Rapid Review

- Q: Scaler that produces mean 0, std 1? → **`StandardScaler`**
- Q: Scaler that produces a fixed [0,1] range? → **`MinMaxScaler`**
- Q: Encoding for nominal (unordered) categories? → **one-hot encoding**
- Q: Encoding for genuinely ordered categories? → **ordinal encoding (with explicit `categories=`)**
- Q: What must happen before any preprocessing is fit? → **the train/test split**
- Q: What should you pass to `cross_val_score` — the model or the full pipeline? → **the full pipeline**
- Q: High train score + low test score = ? → **overfitting**
- Q: Low train score + low test score = ? → **underfitting**
