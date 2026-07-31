# 📋 Master Cheat Sheet: Python for Data Science & AI

A single-page, on-the-job quick reference for the entire course — organized by category, not by module, so you can find what you need fast regardless of when you learned it. Each module's own cheat sheet has more detail and worked examples; this file is the fast-lookup version.

---

## 1. Python Language Fundamentals

```python
# Variables & types
name = "Ada"; age = 36; gpa = 3.9; active = True; data = None
type(name)                          # <class 'str'>
int("42"); float("3.14"); str(42); bool(1)

# f-strings
f"Hello, {name}!"
f"Price: ${price:.2f}"                # 2 decimals
f"{value:,}"                             # thousands separator

# Control flow
if condition: ...
elif other: ...
else: ...
for item in iterable: ...
while condition: ...                     # break / continue
for i in range(2, 10, 2): ...               # 2,4,6,8 (stop excluded)

# Collections
[1, 2, 3]              # list — ordered, mutable, duplicates OK
(1, 2, 3)                # tuple — ordered, immutable
{"a": 1}                   # dict — key -> value; .get(key, default) avoids KeyError
{1, 2, 3}                    # set — unique, fast membership (`in`), & | - for set ops
[x**2 for x in lst if x > 1]    # list comprehension with filter

# Functions
def greet(name, greeting="Hello"):      # default arg
    """One-line docstring."""
    return f"{greeting}, {name}!"
def total(*args): return sum(args)         # args -> tuple
def describe(**kwargs): ...                   # kwargs -> dict
low, high = min_max(nums)                        # unpack multi-return tuple

# Scope
count = 0
def bump():
    global count            # required to MODIFY a global from inside a function
    count += 1

# Error handling
try:
    risky()
except ValueError as e:
    ...
except (TypeError, KeyError):
    ...
else:
    ...             # only if try succeeded
finally:
    ...            # always runs
raise ValueError("Age cannot be negative.")

# Imports
import numpy as np                 # np, pd, plt, sns are the universal aliases
from math import sqrt, pi
```

### Classes & OOP
```python
class Dog:                              # PascalCase
    species = "Canis familiaris"          # class attribute — shared by ALL instances
    def __init__(self, name, age):          # constructor
        self.name = name                       # instance attribute
        self.age = age
    def bark(self): return f"{self.name} says Woof!"

    @classmethod
    def get_count(cls): ...        # cls = the class itself
    @staticmethod
    def is_valid(x): ...              # no self/cls needed

class Puppy(Dog):                       # inheritance
    def __init__(self, name):
        super().__init__(name, age=0)      # call parent's __init__
    def bark(self): return "Yip!"             # override

# Dunder methods
def __str__(self): return "readable form"       # print()/str()
def __repr__(self): return "Dog(name='Rex')"      # REPL/debug/inside lists — safer fallback
def __eq__(self, other): return self.x == other.x   # value equality (default is identity)

# Encapsulation: _protected (convention only), __private (name-mangled)
@property
def balance(self): return self._balance             # read like a plain attribute
@balance.setter
def balance(self, value): self._balance = value        # validated write
```

---

## 2. Environment, Tooling & Version Control

```bash
python -m venv venv                  # create a virtual environment
venv\Scripts\activate                   # Windows activate
source venv/bin/activate                  # macOS/Linux activate
deactivate

pip install pandas==2.1.0
pip freeze > requirements.txt
pip install -r requirements.txt
```

```bash
git init; git branch -M main          # init + ensure branch named "main"
git status; git diff                     # what's changed
git add .; git commit -m "message"
git remote add origin <url>; git push -u origin main
git push; git pull
git checkout -b new-feature; git merge new-feature
```
`.gitignore` essentials: `venv/`, `__pycache__/`, `*.pyc`, `.env`

**VS Code:** `Ctrl+Shift+P` → "Python: Select Interpreter" | `` Ctrl+` `` terminal | `F5` debug | `# %%` Jupyter-style cell.

---

## 3. Files, JSON, CSV & APIs

```python
with open("file.txt", "w") as f: f.write("line\n")     # "w" ERASES, "a" appends, "r" reads
with open("file.txt") as f:
    for line in f: ...                                     # memory-efficient

import json
json.dump(data, file_obj, indent=4); json.load(file_obj)     # file versions
json.dumps(data); json.loads(json_string)                       # string versions ("s" suffix)

import csv
with open("d.csv", newline="") as f:                # ALWAYS newline="" for CSV
    reader = csv.DictReader(f)                          # preferred over plain csv.reader
    for row in reader: row["column_name"]

import requests
response = requests.get(url, params={"k": "v"}, timeout=5)   # ALWAYS set timeout
response.raise_for_status()                                     # raises HTTPError on 4xx/5xx
data = response.json()
# wrap in try/except: requests.HTTPError, ConnectionError, Timeout
```

---

## 4. NumPy — Array Fundamentals

```python
import numpy as np
np.array([1,2,3]); np.zeros(5); np.ones((2,3)); np.arange(0,10,2); np.linspace(0,1,5); np.eye(3)

arr.shape; arr.ndim; arr.size; arr.dtype        # attributes, no ()
matrix[row, col]; matrix[:, 0]; matrix[0:2, 1:3]     # 2D indexing
sub = arr[1:3].copy()                                   # slices are VIEWS — .copy() if needed

a + b   a * b   a > 2                    # vectorized, element-wise (NOT list concatenation!)
arr + 10                                    # broadcasting: scalar -> every element
arr[arr > 60]; arr[(arr>60) & (arr<90)]        # boolean masking — use & | not and/or
arr[[0, 2, 4]]                                    # fancy indexing

arr.sum(); arr.mean(); arr.std(); arr.argmax()     # argmax/argmin return INDEX not value
matrix.sum(axis=0)    # collapses axis 0 (rows) -> per-COLUMN result
matrix.sum(axis=1)    # collapses axis 1 (cols) -> per-ROW result

arr.reshape(3, -1); matrix.flatten(); matrix.T       # -1 = auto-compute; flatten always copies
np.concatenate([a,b]); np.vstack([a,b]); np.hstack([a,b])
```

---

## 5. Pandas — Data Manipulation

```python
import pandas as pd
pd.read_csv("f.csv"); pd.read_json("f.json")
df.to_csv("out.csv", index=False)                # ALWAYS index=False when saving

df.head(); df.info(); df.describe(); df.shape; df.dtypes    # run these FIRST, always

df["col"]              # Series      df[["c1","c2"]]     # DataFrame (double brackets)
df.loc[label, col]        # label-based, slice END INCLUSIVE
df.iloc[pos, pos]            # position-based, slice end EXCLUSIVE (Python-normal)

df[df["col"] > x]
df[(df["a"]>x) & (df["b"]==y)]           # & | only, parens required
df[df["col"].isin([a,b,c])]
df.loc[condition, ["c1","c2"]]              # filter + select in one step

df["new"] = df["a"] * df["b"]                  # vectorized — prefer this
df["new"] = np.where(cond, "yes", "no")           # vectorized conditional
df["new"] = df["a"].apply(lambda x: ...)             # last resort — slower

df = df.drop(columns=["c"]); df = df.rename(columns={"old":"new"})
df.sort_values("col", ascending=False)

df.groupby("col")["target"].agg(["mean","min","max","count"])
pd.concat([df1, df2], ignore_index=True)          # ALWAYS ignore_index=True
pd.merge(left, right, on="key", how="inner")         # inner/left/right/outer
```

---

## 6. Data Cleaning & Wrangling

```python
df.isna().sum()                          # missing count PER COLUMN — check first, always
df.dropna(subset=["col"]); df["col"].fillna(df["col"].median())   # median is outlier-robust

df.duplicated().sum(); df.drop_duplicates(subset=["key"])

df["col"].astype(int)                            # FAILS on any bad value
pd.to_numeric(df["col"], errors="coerce")           # bad -> NaN, safe
pd.to_datetime(df["col"], errors="coerce")             # bad -> NaT, safe
df["date_col"].dt.year; .dt.month; .dt.day_name()

df["col"].str.strip().str.lower()                   # standardize BEFORE groupby/value_counts
df["col"].str.replace(r"[-. ]", "", regex=True)
df["col"].str.contains("text", case=False)

# Outliers — IQR method
q1, q3 = data.quantile(0.25), data.quantile(0.75); iqr = q3 - q1
lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
outliers = data[(data < lower) | (data > upper)]
# Z-score method (roughly normal data only)
z = (data - data.mean()) / data.std(); outliers = data[z.abs() > 2]
```

---

## 7. Data Visualization

```python
import matplotlib.pyplot as plt
fig, ax = plt.subplots()                # ALWAYS start here
ax.plot(x, y, label="s"); ax.bar(cats, vals); ax.scatter(x, y); ax.hist(data, bins=30)
ax.set_title("T"); ax.set_xlabel("X"); ax.legend()
fig.savefig("chart.png", dpi=150, bbox_inches="tight")

import seaborn as sns
sns.histplot(data=df, x="col", kde=True, ax=ax)
sns.boxplot(data=df, x="cat", y="num", ax=ax)             # spread + outliers per category
sns.scatterplot(data=df, x="a", y="b", hue="cat", ax=ax)
sns.heatmap(df[["a","b","c"]].corr(), annot=True, cmap="coolwarm", ax=ax)
sns.pairplot(df[["a","b","c"]])                              # limit to ~5-6 columns

import plotly.express as px
fig = px.line(df, x="c1", y="c2", title="T"); fig.write_html("chart.html")
```
| Need to show | Use |
|---|---|
| Trend over time | Line |
| Compare categories | Bar |
| Two numeric vars | Scatter |
| Distribution of one var | Histogram |
| Distribution + outliers by category | Box plot |
| Correlation matrix | Heatmap |
| Every pairwise relationship | Pairplot |
| Interactive/shareable | Plotly |

---

## 8. Statistics & EDA

```python
series.mean(); series.median(); series.std(); series.skew()    # skew: ~0 symmetric, >0 right-tail

from scipy import stats
corr, p = stats.pearsonr(x, y)                       # correlation ≠ causation, always
t_stat, p = stats.ttest_ind(group_a, group_b)            # compare 2 group means
chi2, p, dof, exp = stats.chi2_contingency(table)           # compare 2 categorical vars
ci = stats.t.interval(0.95, len(data)-1, loc=data.mean(), scale=stats.sem(data))
```
**Hypothesis testing:** H₀ = no effect; p-value = P(data this extreme | H₀ true); α=0.05 typical; p<α → reject H₀. p-value ≠ "probability H₀ is true."

**Full EDA workflow:** Inspect → Clean → Describe → Visualize → Test → Conclude (separate description from inference).

---

## 9. SQL

```python
import sqlite3
conn = sqlite3.connect(":memory:"); cursor = conn.cursor()
cursor.execute("CREATE TABLE t (id INTEGER PRIMARY KEY, name TEXT)")
cursor.executemany("INSERT INTO t VALUES (?, ?)", rows); conn.commit()   # ALWAYS ? placeholders
pd.read_sql("SELECT * FROM t", conn)                                        # query -> DataFrame
```
```sql
SELECT col1, col2 FROM t WHERE condition ORDER BY col DESC LIMIT 5;
SELECT a.col, b.col FROM a INNER JOIN b ON a.key=b.key;     -- only matches
SELECT a.col, b.col FROM a LEFT JOIN b ON a.key=b.key;        -- all of a, NULL if no match
SELECT category, SUM(value) FROM t GROUP BY category HAVING SUM(value)>1000;  -- HAVING filters AFTER agg
WITH avgs AS (SELECT category, AVG(value) v FROM t GROUP BY category)
SELECT * FROM avgs WHERE v > 100;                              -- CTE, preferred over nested subqueries
```
| SQL | Pandas equivalent |
|---|---|
| `WHERE` | boolean mask |
| `INNER/LEFT JOIN` | `pd.merge(how="inner"/"left")` |
| `GROUP BY` + agg | `.groupby().agg()` |
| `ORDER BY`/`LIMIT` | `.sort_values()`/`.head()` |

⚠️ Never build SQL with f-strings/concatenation (injection risk) — always `?` placeholders.

---

## 10. Classical Machine Learning (scikit-learn)

```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

model = SomeModel(); model.fit(X_train, y_train); model.predict(X_test); model.score(X_test, y_test)
```
**Classification:**
```python
from sklearn.linear_model import LogisticRegression
model = LogisticRegression(max_iter=1000)
model.predict_proba(X_test)
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
```
**Regression:**
```python
from sklearn.linear_model import LinearRegression
model.coef_; model.intercept_
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
rmse = np.sqrt(mean_squared_error(y_test, preds))     # most interpretable — same units as target
```
**Feature engineering & pipelines:**
```python
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
preprocessor = ColumnTransformer([("num", StandardScaler(), num_cols), ("cat", OneHotEncoder(), cat_cols)])
pipeline = Pipeline([("preprocessor", preprocessor), ("classifier", LogisticRegression())])
# fit_transform ONLY on train; .transform() (reusing train stats) on test — NEVER fit on full data before split
```
**Cross-validation & tuning:**
```python
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV
cross_val_score(pipeline, X, y, cv=5)                     # ALWAYS pass the full pipeline
GridSearchCV(model, param_grid, cv=5)                        # exhaustive — few params/values
RandomizedSearchCV(model, param_distributions, n_iter=15)      # sampled — many params/continuous
```
**Unsupervised learning:**
```python
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
X_scaled = StandardScaler().fit_transform(X)                # ALWAYS scale first
kmeans = KMeans(n_clusters=3, n_init=10).fit_predict(X_scaled)
pca = PCA(n_components=2).fit_transform(X_scaled); pca.explained_variance_ratio_
```
**Ensembles:**
```python
from sklearn.ensemble import RandomForestClassifier      # bagging — reduces variance
import xgboost as xgb; import lightgbm as lgb              # boosting — reduces bias+variance, more tuning-sensitive
model.feature_importances_                                    # relative usefulness, NOT signed/causal
```
| Symptom | Fix |
|---|---|
| `ConvergenceWarning` | Scale features (StandardScaler in a Pipeline) |
| Train ≫ test score | Overfitting — simplify, regularize, more data |
| Both scores low | Underfitting — more complex model/features |

---

## 11. Deep Learning (PyTorch & TensorFlow/Keras)

```
neuron: weighted_sum(inputs)+bias -> activation -> output
CNN: [conv -> activation -> pool] x N -> flatten -> dense -> output
ReLU: max(0,x) default hidden | Sigmoid: (0,1) binary output | Softmax: multi-class output
```
**PyTorch:**
```python
import torch, torch.nn as nn
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(in_f, hidden); self.relu = nn.ReLU(); self.layer2 = nn.Linear(hidden, out_f)
    def forward(self, x): return self.layer2(self.relu(self.layer1(x)))

model = Net(); criterion = nn.CrossEntropyLoss(); optimizer = torch.optim.Adam(model.parameters(), lr=0.01)
for epoch in range(epochs):
    optimizer.zero_grad(); loss = criterion(model(X_train), y_train); loss.backward(); optimizer.step()
model.eval()
with torch.no_grad(): predictions = model(X_test)
```
**Keras:**
```python
from tensorflow import keras
model = keras.Sequential([keras.layers.Input(shape=(n,)), keras.layers.Dense(h, activation="relu"),
                           keras.layers.Dropout(0.3), keras.layers.Dense(k, activation="softmax")])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
model.fit(X_train, y_train, epochs=100, validation_split=0.2, callbacks=[
    keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)])
```
**CNNs:**
```python
# PyTorch: nn.Conv2d(in_c, out_c, kernel_size=3, padding=1) + nn.MaxPool2d(2,2), then flatten (x.view(x.size(0),-1))
# Keras: keras.layers.Conv2D(filters, 3, padding="same", activation="relu") + MaxPooling2D(2) + Flatten()
```
**Transfer learning:**
```python
model = torchvision.models.resnet18(weights="IMAGENET1K_V1")
for p in model.parameters(): p.requires_grad = False           # freeze base
model.fc = nn.Linear(model.fc.in_features, num_classes)            # new trainable head
```
| Symptom | Fix |
|---|---|
| Train acc 1.0, test much lower | Overfitting — dropout, early stopping, more data |
| Loss not decreasing | Learning rate wrong, or missing `optimizer.zero_grad()` |

---

## 12. NLP, Transformers & Generative AI / LLMs

```python
from transformers import AutoTokenizer, AutoModel, pipeline
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
tokenizer.tokenize(text)              # subword pieces, "##" = continuation
pipeline("sentiment-analysis")(text)
pipeline("zero-shot-classification")(text, candidate_labels=[...])
pipeline("ner", aggregation_strategy="simple")(text)     # NOT grouped_entities= (deprecated)
```
**Self-attention:** `Q=emb@Wq; K=emb@Wk; V=emb@Wv; scores=Q@K.T/sqrt(dim); weights=softmax(scores); out=weights@V` — every word attends to every other word; encoder=understanding (BERT), decoder=generation (GPT).

**LLM APIs & prompting:**
```python
import anthropic
client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
response = client.messages.create(model="claude-sonnet-4-5", max_tokens=1024, temperature=0.0,
    system="...", messages=[{"role": "user", "content": prompt}])
```
Prompting techniques: zero-shot (describe only) | few-shot (show examples) | chain-of-thought ("think step by step") | format spec ("respond only with JSON").

**Embeddings & RAG:**
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2"); embeddings = model.encode([...])

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
vectorstore = FAISS.from_texts(documents, HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2"))
retrieved = vectorstore.similarity_search(query, k=2)
# RAG = Retrieve (semantic search) -> Augment (insert into prompt) -> Generate (LLM answers from context)
```
⚠️ Prompt must explicitly say "answer using ONLY the context" or the LLM may ignore retrieved docs. Retrieval always returns its top-k closest match, relevant or not — check similarity scores if you need reliable "I don't know" behavior.

---

## 13. MLOps & Deployment

```python
import joblib
joblib.dump(pipeline, "model.joblib")           # save the FULL pipeline, never just the bare model
loaded = joblib.load("model.joblib")

# PyTorch: save weights only
torch.save(model.state_dict(), "w.pth"); model.load_state_dict(torch.load("w.pth")); model.eval()
```
```python
from fastapi import FastAPI
from pydantic import BaseModel
app = FastAPI(); model = joblib.load("model.joblib")     # load ONCE at startup

class Features(BaseModel): features: list[float]

@app.post("/predict")
def predict(data: Features):
    X = np.array(data.features).reshape(1, -1)
    return {"prediction": int(model.predict(X)[0])}          # cast NumPy -> plain Python type
```
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt . ; RUN pip install --no-cache-dir -r requirements.txt
COPY app.py . ; COPY model.joblib .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```
```python
# Drift detection — direct extension of Module 10's hypothesis testing
from scipy import stats
stat, p_value = stats.ks_2samp(training_data, production_data)
drift_detected = p_value < 0.05
```

---

## Universal Troubleshooting Quick-Reference

| Symptom | Likely Cause | Fix |
|---|---|---|
| `IndentationError` / `NameError` | Mixed tabs/spaces; typo/undefined var | 4-space indents; check spelling |
| `ModuleNotFoundError` | venv not activated, or wrong interpreter | Confirm `(venv)`; VS Code "Select Interpreter" |
| `git push` rejected | Local history behind remote | `git pull` first |
| `ValueError: truth value ... ambiguous` (NumPy/Pandas) | Used `and`/`or` instead of `&`/`\|` | Use `&`/`\|` with parens around each condition |
| Modifying a slice changed the original | NumPy slices are views | `.copy()` for an independent array |
| `df["col"] == np.nan` always False | NaN never equals anything | Use `.isna()`/`.notna()` |
| `.astype(int)` raises `ValueError` | Bad value can't convert directly | `pd.to_numeric(errors="coerce")` |
| Extra unnamed column after CSV round-trip | Forgot `index=False` | Always pass it when saving |
| `ConvergenceWarning` (LogisticRegression) | Unscaled features | `StandardScaler` inside a `Pipeline` |
| Suspiciously perfect test score | Data leakage — preprocessing fit before split | Split first; `fit_transform` train only, `transform` test |
| Train ≫ test performance | Overfitting | Simplify model, regularize, more data, dropout/early stopping |
| High accuracy but useless in practice | Imbalanced classes | Check precision/recall/F1, not just accuracy |
| SQL injection risk | f-string/concatenated query | Always `?` parameterized placeholders |
| API call hangs forever | No `timeout` set | Always pass `timeout=` |
| RAG answers ignore your documents | Prompt didn't demand context-only answers | "Answer using ONLY the context provided" |
| API returns NumPy serialization error | Returned raw `numpy.int64`/etc. | Cast to plain `int`/`float`/`str` |

## The Universal "New Task" Workflow

1. **Inspect** the data/problem first (`.head()`, `.info()`, `.shape`, `.isna().sum()`) before writing any logic.
2. **Clean & prepare** — handle missing data/duplicates/outliers/types; split train/test *before* any fitting.
3. **Explore** — visualize and describe before modeling; form a hypothesis.
4. **Build** — start simple (a baseline model), then compare against more complex options via cross-validation.
5. **Evaluate honestly** — on held-out data only, with metrics matched to the actual problem (not just accuracy).
6. **Communicate** — separate description from statistical inference; give a concrete, actionable recommendation.
7. **Deploy & monitor** — package, serve, containerize, and watch for drift once it's live.
