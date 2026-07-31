# Capstone 1: Complete Reference Solution

Every code block below was executed and its output verified. Your own approach may differ in reasonable ways (different outlier handling, a different model choice) — that's normal in real data science. Compare your reasoning, not just your exact numbers.

## Step 1: First Look

```python
import pandas as pd
import numpy as np

df = pd.read_csv("customer_churn.csv")

print(df.shape)
print(df.dtypes)
print(df.isna().sum())
print(df.duplicated().sum())
print(df["churn"].mean())

for col in ["contract_type", "internet_service", "tech_support", "payment_method"]:
    print(col, df[col].unique())
```
```
(2008, 11)
customer_id             int64
age                   float64
tenure_months         float64
contract_type            str
internet_service         str
tech_support             str
payment_method           str
monthly_charges       float64
total_charges         float64
num_support_calls       int64
churn                   int64
dtype: object

age                  15
tech_support         15
total_charges        30
(all other columns: 0)

Duplicates: 8
Churn rate: 21.76%

contract_type: ['One year' 'Two year' 'Month-to-month' ' One year ' ' Month-to-month ' ' Two year ']
internet_service: ['No' 'Fiber optic' 'DSL' 'NO' 'FIBER OPTIC']
```

**Findings:** 8 exact duplicate rows, missing values in 3 columns, and inconsistent whitespace/casing in `contract_type` and `internet_service`. Churn rate is 21.76% — this is an **imbalanced classification problem** (roughly 1 in 5 customers churns), which matters directly for Step 5/7's metric choices — accuracy alone would be a misleading way to judge model quality here (Module 12b).

## Step 2: Clean the Data

```python
df = df.drop_duplicates()

df["contract_type"] = df["contract_type"].str.strip()
df["internet_service"] = (
    df["internet_service"].str.strip().str.upper()
    .map({"DSL": "DSL", "FIBER OPTIC": "Fiber Optic", "NO": "No"})
)

df["age"] = df["age"].fillna(df["age"].median())
df["tech_support"] = df["tech_support"].fillna("Unknown")
# total_charges is missing for some rows -- but we can reconstruct a reasonable
# estimate from tenure * monthly rate, which is a smarter fill than a blind median
df["total_charges"] = df["total_charges"].fillna(df["tenure_months"] * df["monthly_charges"])

q1 = df["monthly_charges"].quantile(0.25)
q3 = df["monthly_charges"].quantile(0.75)
iqr = q3 - q1
lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
outliers = df[(df["monthly_charges"] < lower) | (df["monthly_charges"] > upper)]
print(f"Outliers found: {len(outliers)}")
df = df[(df["monthly_charges"] >= lower) & (df["monthly_charges"] <= upper)]

print(df.isna().sum().sum())
print(df.shape)
```
```
Outliers found: 13
0
(1987, 11)
```

**Decisions and reasoning:**
- `age`: filled with the median — a small number of missing values (15), no reason to suspect they're systematically different from the rest.
- `tech_support`: filled with `"Unknown"` rather than the mode — since we don't know the true value, pretending it's the most common category could bias the analysis; keeping it as its own honest category is safer.
- `total_charges`: filled using `tenure_months * monthly_charges` rather than a blind median — since we *do* have the information to reconstruct a much better estimate, this is a smarter fill than ignoring available context (a step beyond Module 08's simplest examples, applying the same underlying principle).
- `monthly_charges` outliers: 13 rows (values like $662, $893, $1196/month) are wildly outside the normal $15-$150 range — almost certainly data-entry errors (e.g., an extra digit). Removed rather than capped, since there's no reliable way to guess the true intended value.

## Step 3: Explore the Data

```python
for col in ["contract_type", "internet_service", "tech_support", "payment_method"]:
    print(f"--- {col} ---")
    print(df.groupby(col)["churn"].mean().sort_values(ascending=False))
```
```
--- contract_type ---
Month-to-month    0.311034
One year          0.091295
Two year          0.087671

--- internet_service ---
Fiber Optic    0.267176
DSL            0.179792
No             0.168766

--- tech_support ---
No         0.259843
Yes        0.145299
Unknown    0.066667

--- payment_method ---
Credit card         0.240000
Electronic check    0.227181
Bank transfer        0.205761
Mailed check        0.200750
```

```python
print(df[["age", "tenure_months", "monthly_charges", "total_charges", "num_support_calls", "churn"]].corr()["churn"])
```
```
age                 -0.0107
tenure_months       -0.2084
monthly_charges      0.1277
total_charges       -0.1619
num_support_calls    0.1010
churn                1.0000
```

**Findings, before building any model:**
- **Month-to-month contracts churn at 31%** — over 3x the rate of one/two-year contracts (~9%). This is the single starkest pattern in the data.
- **Fiber optic customers churn more (27%)** than DSL (18%) or no-internet customers (17%).
- **No tech support correlates with higher churn (26% vs. 15%)** — customers without support may be more likely to hit friction and leave.
- **Payment method shows little difference** across categories (20-24%) — an interesting *null* result; not every plausible factor turns out to matter.
- **Tenure is negatively correlated with churn** (-0.21) — newer customers churn more, a very common real-world pattern (customers who've stuck around longer have already "proven" they're a good fit).
- **Age shows almost no relationship** (-0.01) — churn here doesn't appear to be an age-driven phenomenon.

**Hypothesis going in:** Contract type, tech support, and internet service type look like the strongest churn drivers; tenure matters too. Payment method and age look unlikely to matter much. Let's see if the model agrees.

## Step 4: Prepare Features & Split

```python
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, OneHotEncoder

X = df.drop(columns=["customer_id", "churn"])   # customer_id is just an identifier, not a real feature
y = df["churn"]

numeric_features = ["age", "tenure_months", "monthly_charges", "total_charges", "num_support_calls"]
categorical_features = ["contract_type", "internet_service", "tech_support", "payment_method"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

preprocessor = ColumnTransformer(transformers=[
    ("num", StandardScaler(), numeric_features),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
])
```

**Why `stratify=y`:** with only ~22% churn, a plain random split could occasionally produce a test set with a notably different churn rate than training by chance — `stratify=y` guarantees both sets preserve the original class proportions, giving a more reliable evaluation.

## Step 5: Train and Compare Models

```python
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, roc_auc_score
import xgboost as xgb

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
    "Random Forest": RandomForestClassifier(n_estimators=200, random_state=42),
    "XGBoost": xgb.XGBClassifier(n_estimators=200, random_state=42, eval_metric="logloss")
}

for name, model in models.items():
    pipeline = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", model)])
    cv_scores = cross_val_score(pipeline, X_train, y_train, cv=5, scoring="roc_auc")
    pipeline.fit(X_train, y_train)
    test_preds = pipeline.predict(X_test)
    test_proba = pipeline.predict_proba(X_test)[:, 1]
    print(f"{name}: CV AUC={cv_scores.mean():.4f}, Test Accuracy={accuracy_score(y_test, test_preds):.4f}, "
          f"Test AUC={roc_auc_score(y_test, test_proba):.4f}")
```
```
Logistic Regression: CV AUC=0.7924, Test Accuracy=0.7814, Test AUC=0.7411
Random Forest: CV AUC=0.7695, Test Accuracy=0.7638, Test AUC=0.6923
XGBoost: CV AUC=0.7379, Test Accuracy=0.7487, Test AUC=0.6671
```

**Metric choice:** AUC (area under the ROC curve) was used for model comparison rather than accuracy, since it's insensitive to the classification threshold and works well for imbalanced problems — a model that's simply biased toward predicting the majority class doesn't get an inflated score the way accuracy can produce (Module 12b).

**Result: Logistic Regression wins**, meaningfully outperforming both ensemble methods here. This is a good reminder from Module 15's material: more complex models (Random Forest, XGBoost) don't automatically win — when the true underlying relationship is closer to linear/additive (as churn risk often genuinely is), a well-regularized linear model can beat more flexible ones, especially on a moderately-sized dataset like this one.

## Step 6: Tune the Winner

```python
from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import uniform

pipeline = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000, random_state=42))
])

param_dist = {"classifier__C": uniform(0.01, 10)}
search = RandomizedSearchCV(pipeline, param_dist, n_iter=20, cv=5, scoring="roc_auc", random_state=42)
search.fit(X_train, y_train)

print(f"Best C: {search.best_params_}")
print(f"Best CV AUC: {search.best_score_:.4f}")
```
```
Best C: {'classifier__C': 0.2158}
Best CV AUC: 0.7929
```

Tuning `C` (the regularization strength) found a slightly stronger-regularized model, but the improvement over the default is marginal (0.7924 → 0.7929) — this dataset's signal is well-captured by logistic regression even without extensive tuning.

## Step 7: Evaluate Honestly

```python
from sklearn.metrics import confusion_matrix, classification_report

best_model = search.best_estimator_
test_preds = best_model.predict(X_test)
test_proba = best_model.predict_proba(X_test)[:, 1]

print(confusion_matrix(y_test, test_preds))
print(classification_report(y_test, test_preds, target_names=["No Churn", "Churn"]))
```
```
[[289  22]
 [ 65  22]]
              precision    recall  f1-score   support
    No Churn       0.82      0.93      0.87       311
       Churn       0.50      0.25      0.34        87
    accuracy                           0.78       398
```

⚠️ **Critical finding:** despite 78% accuracy, the model only **catches 25% of actual churners** (recall = 0.25). Given the business goal — "flag at-risk customers so retention can reach out" — this is a serious problem: 3 out of 4 customers who will actually churn are never flagged at all.

### Addressing the recall problem: `class_weight="balanced"`

```python
pipeline_balanced = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(max_iter=1000, random_state=42, class_weight="balanced", C=0.2158))
])
pipeline_balanced.fit(X_train, y_train)
test_preds_b = pipeline_balanced.predict(X_test)
test_proba_b = pipeline_balanced.predict_proba(X_test)[:, 1]

print(f"Test Accuracy: {accuracy_score(y_test, test_preds_b):.4f}")
print(f"Test AUC: {roc_auc_score(y_test, test_proba_b):.4f}")
print(confusion_matrix(y_test, test_preds_b))
print(classification_report(y_test, test_preds_b, target_names=["No Churn", "Churn"]))
```
```
Test Accuracy: 0.6809
Test AUC: 0.7430
[[207 104]
 [ 23  64]]
              precision    recall  f1-score   support
    No Churn       0.90      0.67      0.77       311
       Churn       0.38      0.74      0.50        87
    accuracy                           0.68       398
```

**The tradeoff, made concrete:** `class_weight="balanced"` raises churn recall from **0.25 → 0.74** (catching 3x more actual churners), at the cost of precision dropping from 0.50 → 0.38 (more false alarms) and overall accuracy dropping from 0.78 → 0.68. Notably, **AUC barely changes** (0.741 → 0.743) — AUC measures the model's ability to *rank* customers by risk, independent of where you set the decision threshold, while accuracy/precision/recall all depend on that threshold/weighting choice.

✅ **This is a business decision, not a purely technical one** (Module 12b): if reaching out to a customer who wasn't actually going to churn is cheap (a quick email, a small discount offer), the balanced model is clearly better — missing 75% of real churners (the unbalanced model) is far more costly than a bit more outreach to people who would've stayed anyway.

## Step 8: Interpret and Recommend

```python
feature_names = (
    numeric_features +
    list(best_model.named_steps["preprocessor"].named_transformers_["cat"].get_feature_names_out(categorical_features))
)
coefficients = best_model.named_steps["classifier"].coef_[0]
coef_df = pd.DataFrame({"feature": feature_names, "coefficient": coefficients}).sort_values(
    "coefficient", key=abs, ascending=False
)
print(coef_df.head(6))
```
```
                         feature  coefficient
5   contract_type_Month-to-month     1.1326
7         contract_type_Two year    -0.6420
3                  total_charges    -0.5947
2                monthly_charges     0.5282
6         contract_type_One year    -0.4855
11               tech_support_No     0.4357
```

**Top churn drivers, confirmed by the model:**
1. **Month-to-month contracts** are by far the strongest positive driver of churn — exactly matching Step 3's EDA finding.
2. **Longer-term contracts** (one/two year) are the strongest *protective* factors.
3. **Higher monthly charges** increase churn risk; interestingly, higher **total charges** (a proxy for tenure × spend) decreases it — customers who've spent more *cumulatively* over time (i.e., have stuck around) are less likely to leave, even if their current monthly rate is high.
4. **No tech support** meaningfully increases churn risk, consistent with the EDA.

### Business Summary (non-technical)

> **Findings:** Our analysis of 1,987 customer records (after removing duplicates, data-entry errors, and standardizing inconsistent formatting) found a 22% overall churn rate. The single strongest driver of cancellation is contract type: month-to-month customers churn at 31%, more than three times the rate of customers on one- or two-year contracts (~9%). Customers without tech support and those on fiber-optic internet also show elevated churn risk. Payment method and customer age showed little meaningful relationship with churn.
>
> We built a model that can rank customers by churn risk with reasonable accuracy (AUC ≈ 0.74). Importantly, there's a real tradeoff between catching more at-risk customers (higher recall) and avoiding false alarms (higher precision) — we recommend the retention team decide which matters more given the actual cost of an outreach versus the cost of a missed cancellation, and we can tune the model's threshold accordingly.
>
> **Recommendation:** Consider a targeted incentive (e.g., a discount for switching to an annual contract) aimed specifically at month-to-month customers without tech support — this is the highest-risk, most clearly identifiable segment in the data, and directly addresses two of the three strongest churn drivers found. We'd recommend a small A/B test of this offer before rolling it out broadly, to confirm it actually changes behavior rather than just correlating with it (recall Module 10's correlation-vs-causation lesson — our analysis identifies *risk factors*, not proven causes).

---

**Next:** [`portfolio-presentation.md`](portfolio-presentation.md) — how to present this project.
