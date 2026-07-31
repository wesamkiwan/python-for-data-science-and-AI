# 🎤 Master Interview Prep: Python for Data Science & AI

A consolidated, category-organized interview guide covering the entire course. Each section groups conceptual questions by difficulty (🟢 Beginner / 🟡 Intermediate / 🔴 Advanced), followed by practical/coding questions, real-world scenario questions, and "gotcha" traps. A cross-cutting **Scenario Spotlight**, **Gotcha Hall of Fame**, and full **Quick-Fire Rapid Review** close out the guide.

> 💡 **How to use this file:** Don't just read the answers — cover them and answer out loud first. The model answers are written the way a strong candidate would actually speak them: concise, with a concrete example, and (where relevant) a nod to the tradeoff. For deep dives on any single topic, the module-level `moduleNN-interview.md` files have more room to breathe; this file is for broad review and rapid-fire practice before an interview.

---

## Table of Contents

1. [Python Language Fundamentals](#1-python-language-fundamentals)
2. [Tooling, Files & APIs](#2-tooling-files--apis)
3. [NumPy & Pandas](#3-numpy--pandas)
4. [Data Cleaning, Visualization & EDA/Statistics](#4-data-cleaning-visualization--edastatistics)
5. [SQL for Data Science](#5-sql-for-data-science)
6. [Classical ML: Foundations & Evaluation](#6-classical-ml-foundations--evaluation)
7. [Unsupervised Learning & Ensembles](#7-unsupervised-learning--ensembles)
8. [Deep Learning Foundations](#8-deep-learning-foundations)
9. [Computer Vision (CNNs)](#9-computer-vision-cnns)
10. [NLP & Transformers](#10-nlp--transformers)
11. [Generative AI, LLMs & RAG](#11-generative-ai-llms--rag)
12. [MLOps & Deployment](#12-mlops--deployment)
13. [Scenario Spotlight — Cross-Cutting System Design](#13-scenario-spotlight--cross-cutting-system-design)
14. [Gotcha Hall of Fame](#14-gotcha-hall-of-fame)
15. [Master Quick-Fire Rapid Review](#15-master-quick-fire-rapid-review)

---

## 1. Python Language Fundamentals

*(Modules 01-03: syntax, functions, OOP)*

### 🟢 Beginner

**Q: What's the difference between a list and a tuple?**
> A: Both are ordered collections that allow duplicates. The key difference is mutability — a list can change after creation, a tuple can't. I'd use a tuple for fixed data like coordinates, a list for anything expected to grow or change.

**Q: What does "dynamically typed" mean in Python?**
> A: You don't declare a variable's type up front, and a variable can be reassigned to a different type later — Python determines the type at runtime from the value itself.

**Q: What's the difference between `==` and `is`?**
> A: `==` checks value equality; `is` checks object identity (same object in memory). Always use `is None`, never `== None`.

**Q: What's the difference between a parameter and an argument?**
> A: A parameter is the named placeholder in a function's definition; an argument is the actual value passed at call time.

**Q: What is `self`, and why does every instance method need it?**
> A: `self` refers to the specific object a method was called on, letting the method read/modify that instance's own data. Python passes it automatically on `obj.method()`, but it must still be declared as the first parameter.

**Q: What's the difference between a class and an object?**
> A: A class is the blueprint; an object (instance) is a concrete thing built from it, with its own actual data. Many independent objects can come from one class.

### 🟡 Intermediate

**Q: When would you use a set over a list?**
> A: When you need unique items and don't care about order, or need fast membership checks — sets use a hash table internally, so `in` is roughly O(1) versus O(n) for a list. Classic use: de-duplicating IDs or "have I seen this before?" checks in a loop.

**Q: Why is `from module import *` discouraged?**
> A: It pulls every public name into your namespace with no prefix, obscuring where a name came from and risking silent overwrites of your own names. Prefer explicit imports.

**Q: Why shouldn't you use a mutable default argument like `def f(items=[]):`?**
> A: Default values are evaluated once, at function-definition time — every call sharing that default mutates the *same* object across calls. Fix: `def f(items=None): items = items if items is not None else []`.

**Q: What does `super()` do?**
> A: Gives access to the parent class's methods from a subclass — most commonly `super().__init__(...)` to reuse the parent's setup logic, so future changes to the parent automatically propagate instead of drifting out of sync with duplicated code.

**Q: Explain polymorphism with an example.**
> A: The same method call behaves differently depending on the object's actual type, with no `isinstance` branching needed by the caller. scikit-learn relies on this constantly — `model.fit(X, y)` works identically whether `model` is `LinearRegression` or `RandomForestClassifier`.

**Q: What's the difference between `__str__` and `__repr__`?**
> A: `__str__` is the friendly, human-readable form (`print()`/`str()`); `__repr__` is the unambiguous, ideally-recreate-the-object form used by the REPL and containers. If only `__repr__` is defined, Python falls back to it for `print()` too — so it's the safer one to always implement.

### Practical / Coding

```python
# Even numbers via comprehension
numbers = [1, 2, 3, 4, 5, 6]
evens = [n for n in numbers if n % 2 == 0]        # [2, 4, 6]

# safe_int with graceful fallback
def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

# Polymorphic Shape/Square inheritance
class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2
```

### Scenario

**Q: You're designing classes for Manager/Engineer/Intern that share `name`/`salary` but calculate bonuses differently. How would you structure this?**
> A: Base `Employee` class holding shared attributes in `__init__`; each subclass calls `super().__init__(...)` and overrides `calculate_bonus()` with its own formula. Calling code then invokes `employee.calculate_bonus()` polymorphically without caring which subclass it is.

### 🚩 Gotcha

**Q: Why does `add_item("a")` then `add_item("b")` return `['a']` then `['a', 'b']` when both calls omit the `items` argument?**
```python
def add_item(item, items=[]):
    items.append(item)
    return items
```
> A: The default `[]` is created once at definition time and shared/mutated across every call that doesn't supply its own list. Fix with `items=None` + `items or []` inside the body.

**Q: Why does `p1 == p2` return `False` for two `Point` objects with identical `x`/`y`?**
> A: Without a custom `__eq__`, `==` falls back to identity comparison (same as `is`) — two separate objects are never equal by default, regardless of matching data.

---

## 2. Tooling, Files & APIs

*(Modules 02, 04, 05: error handling, file I/O, JSON/CSV, requests, venvs, git)*

### 🟢 Beginner

**Q: What does a function return if it has no explicit `return`?**
> A: `None` — printing inside a function is not the same as returning a value.

**Q: Why always use `with open(...)` instead of manual `.close()`?**
> A: `with` is a context manager guaranteeing the file closes even if an exception occurs mid-block — a manual `.close()` at the end of the code never runs if an error happens first.

**Q: What's the difference between `"w"` and `"a"` file modes?**
> A: `"w"` erases existing content immediately on open; `"a"` appends to the end. Using `"w"` when you meant `"a"` is a classic way to destroy data.

**Q: What Python types does JSON map to?**
> A: Object → `dict`, array → `list`, `true`/`false`/`null` → `True`/`False`/`None`.

**Q: Why use virtual environments instead of installing packages globally?**
> A: Different projects need different, sometimes conflicting, package versions. A venv isolates each project and makes dependencies explicit/reproducible via `requirements.txt`.

**Q: What's the difference between `git add` and `git commit`?**
> A: `git add` stages changes as ready-to-include; `git commit` saves everything staged as a permanent snapshot with a message.

### 🟡 Intermediate

**Q: Why does `requests.get()` not raise an exception on a 404/500?**
> A: The HTTP request itself succeeded — a response came back, it just represents an error. Check `.status_code` or call `.raise_for_status()` (raises `requests.HTTPError` on 4xx/5xx).

**Q: Why does `csv.DictReader` return every value as a string, even numeric-looking columns?**
> A: CSV is plain text with no type system — the reader parses structure, not types. You must explicitly cast, or use `pd.read_csv()` later, which infers types automatically.

**Q: What's a practical reason to use a feature branch instead of committing directly to `main`?**
> A: Isolates in-progress/breakable work from a stable `main`, enables PR-based code review, and lets you discard a bad idea without ever touching `main`'s history.

**Q: How would you reproduce a teammate's exact environment on a new machine?**
> A: Clone the repo, `python -m venv venv`, activate, `pip install -r requirements.txt` — assuming an up-to-date `requirements.txt` (from `pip freeze`) was committed.

### Practical / Coding

```python
def fetch_user(user_id):
    try:
        response = requests.get(f".../users/{user_id}", timeout=5)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None
```
```bash
mkdir my_project && cd my_project
python -m venv venv && source venv/bin/activate
pip install requests && pip freeze > requirements.txt
git init && git branch -M main
echo -e "venv/\n__pycache__/" > .gitignore
git add . && git commit -m "Initial commit"
```

### Scenario

**Q: You accidentally committed and pushed an API key to a public GitHub repo. What do you do?**
> A: Immediately rotate/revoke the key at its source — deleting the file in a new commit does NOT remove it from git history. Then scrub history (`git filter-repo` or GitHub's guidance) and add it to `.gitignore` going forward.

**Q: An API you call hourly occasionally times out or 500s. How do you make the script resilient?**
> A: `try`/`except` around `requests.Timeout`/`HTTPError`/`ConnectionError`, always with explicit `timeout=`. Log failures with enough detail to diagnose later; consider a short retry/backoff for transient errors (not for a 404, which won't change on retry).

### 🚩 Gotcha

**Q: `pip install pandas` succeeds but `import pandas` still fails. Why?**
> A: The venv wasn't activated during install (or the running script points at a different environment). Always confirm `(venv)` in the prompt and match VS Code's selected interpreter.

**Q: `response.status_code` is 200 but `.json()` raises an error. Why?**
> A: 200 only confirms the request succeeded — it says nothing about the response body being valid JSON (could be empty, HTML, or malformed).

---

## 3. NumPy & Pandas

*(Modules 06-07)*

### 🟢 Beginner

**Q: How is a NumPy array different from a Python list?**
> A: Fixed-type, contiguous memory, operations run in compiled C rather than the Python interpreter — much faster and more memory-efficient for numeric work, at the cost of mixed-type flexibility.

**Q: What's the difference between a Pandas `Series` and a `DataFrame`?**
> A: A `Series` is one labeled 1D column; a `DataFrame` is a 2D table of multiple Series sharing an index. `df["col"]` returns a Series.

**Q: What does `.info()` tell you that `.describe()` doesn't?**
> A: `.info()` is structural — dtypes, non-null counts, memory. `.describe()` is distributional — mean/std/quartiles for numeric columns. Run both immediately after loading any new dataset.

### 🟡 Intermediate

**Q: Explain vectorization and why it's faster than a `for` loop.**
> A: Applying an operation to a whole array at once, with the looping happening inside NumPy's compiled C rather than the Python interpreter — avoiding per-iteration interpreter overhead. Can be several times to 50x+ faster.

**Q: Explain broadcasting with an example.**
> A: NumPy's rule for combining differently-shaped arrays by conceptually stretching the smaller one, without copying data — e.g. adding a shape `(3,)` array to a `(3,3)` matrix broadcasts across every row. Shapes must match (or be 1) when compared right-to-left.

**Q: `axis=0` vs `axis=1` when aggregating a 2D array?**
> A: The axis given is the one that *disappears* from the result. `axis=0` collapses rows → per-column results; `axis=1` collapses columns → per-row results.

**Q: Explain `.loc` vs `.iloc`.**
> A: `.loc` selects by label, slice end **inclusive**. `.iloc` selects by integer position, slice end **exclusive** (standard Python behavior). `.loc` is the only option with a non-integer index (dates, IDs).

**Q: Walk through `df.groupby("department")["salary"].mean()`.**
> A: Split-apply-combine: split into groups by unique `department` values, apply `.mean()` to `salary` within each group, combine into one Series indexed by department.

**Q: The four `how` options in `pd.merge()`?**
> A: `"inner"` (default, matches only), `"left"` (all of left + NaN gaps), `"right"` (mirror), `"outer"` (all of both, NaN wherever unmatched).

### Practical / Coding

```python
# Per-student vs per-exam averages
avg_per_student = scores.mean(axis=1)
avg_per_exam = scores.mean(axis=0)

# np.select for multi-condition vectorized categorization
conditions = [df["revenue"] > 10000, df["revenue"] >= 1000]
choices = ["High", "Medium"]
df["revenue_category"] = np.select(conditions, choices, default="Low")

# Merge + groupby: total spend per named customer
merged = pd.merge(orders, customers, on="customer_id", how="left")
totals = merged.groupby("customer_name")["amount"].sum().sort_values(ascending=False)
```

### Scenario

**Q: A merge produces noticeably more rows than either input. Why?**
> A: Duplicate keys on one or both sides — a merge produces one row per matching combination, which can multiply row count. Check with `.duplicated().sum()` on the key column before trusting the result.

### 🚩 Gotcha

**Q: Slicing `arr[1:3]` and modifying the slice changes the original array. Why?**
> A: NumPy slices are *views*, not copies (unlike Python list slicing) — use `.copy()` for an independent copy.

**Q: `if arr > 2 and arr < 5:` raises `ValueError: truth value of an array is ambiguous`. Fix?**
> A: `and`/`or` need a single boolean; array comparisons return whole boolean arrays. Use `&`/`|` with parentheses: `(arr > 2) & (arr < 5)`. Same rule applies to Pandas boolean Series filtering.

**Q: `df.drop(columns=["temp_column"])` runs but the column is still there. Why?**
> A: `.drop()` (like `.fillna()`, `.dropna()`, `.drop_duplicates()`) returns a new DataFrame by default — reassign: `df = df.drop(...)`.

---

## 4. Data Cleaning, Visualization & EDA/Statistics

*(Modules 08-10)*

### 🟢 Beginner

**Q: Why can't you check for missing values with `df["col"] == np.nan`?**
> A: `NaN` never equals anything by IEEE float spec, even another `NaN` — always `False`. Use `.isna()`/`.notna()`.

**Q: `.dropna()` vs `.fillna()` — when would you choose each?**
> A: `.dropna()` when missing data is rare and won't bias the analysis; `.fillna()` when there's a reasonable substitute and preserving rows matters more.

**Q: Matplotlib Figure vs. Axes?**
> A: Figure is the whole canvas; Axes is one plot within it (a Figure can hold many Axes/subplots). Nearly everything drawn is a method call on a specific Axes.

**Q: When is the median a better "typical value" measure than the mean?**
> A: When outliers or skew exist — a few extreme values pull the mean, but the median stays anchored near the bulk of the data (classic case: salary/home-price data).

**Q: Why is "correlation is not causation" so important?**
> A: A correlation could reflect A→B, B→A, or (most commonly) a confounding third variable driving both — e.g., ice cream sales and drowning deaths both rise with summer heat.

### 🟡 Intermediate

**Q: How would you decide mean vs. median for filling missing values in a numeric column?**
> A: Check the distribution — roughly symmetric, no major outliers → mean is fine; skewed/outlier-heavy (income, etc.) → median is more representative.

**Q: Why might z-score be less reliable than IQR for outlier detection on data that already has a big outlier?**
> A: Z-score uses mean/std, both distorted by the very outlier you're trying to detect, potentially masking it. IQR (percentile-based) is far more resistant to extreme values.

**Q: How does a Seaborn box plot relate to the IQR method?**
> A: The box spans Q1-Q3, whiskers extend to `1.5 × IQR` beyond the box — points beyond that are the exact same "outliers" IQR-based detection would flag. A box plot is the visual version of that calculation.

**Q: What does a correlation heatmap NOT tell you?**
> A: It only measures *linear* relationship strength — a strong non-linear (e.g. U-shaped) relationship can show near-zero correlation despite being clearly related on a scatter plot.

**Q: Explain, in plain terms, what a p-value represents.**
> A: The probability of observing data at least this extreme, *assuming the null hypothesis is true* — not the probability the null hypothesis is true, and not the probability of a fluke.

**Q: Statistical significance vs. practical significance?**
> A: Statistical significance means an effect is unlikely to be pure chance given sample size/variability. Practical significance is whether the effect is big enough to matter. Large samples can make even trivial differences statistically significant — always check effect size too.

**Q: Correctly interpret a 95% confidence interval.**
> A: If you repeated the sampling/estimation procedure many times, ~95% of the resulting intervals would contain the true value — a statement about the *method's* long-run reliability, not a 95% probability for this one already-computed interval.

### Practical / Coding

```python
# Regex + coerce cleaning of a currency string column
cleaned = df["revenue"].str.replace(r"[$,]", "", regex=True)
df["revenue"] = pd.to_numeric(cleaned, errors="coerce")

# t-test for two independent groups
from scipy import stats
t_stat, p_value = stats.ttest_ind(campaign_a_orders, campaign_b_orders)

# chi-square test of independence between two categoricals
contingency_table = pd.crosstab(df["department"], df["left_company"])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)

# Box plot with Seaborn
fig, ax = plt.subplots()
sns.boxplot(data=df, x="department", y="salary", ax=ax)
```

### Scenario

**Q: A stakeholder sees Team A's higher average score and asks you to confirm their process is "clearly better." How do you respond?**
> A: Run a formal t-test rather than trusting the visual gap — a mean difference can arise from random variation, especially with small teams. If not significant, say so; if significant, still flag that correlation with "using the process" doesn't prove causation (confounders like tenure or workload could explain it).

**Q: Sales in one region average 10x every other region. How do you investigate?**
> A: Check with IQR/z-score whether it's a handful of extreme rows (likely data-entry error) vs. a broad, consistent pattern across many orders (more likely a genuine business signal, e.g. enterprise contracts) before deciding to clean, exclude, or keep it.

### 🚩 Gotcha

**Q: `df["age"].fillna(df["age"].mean())` runs but `.isna().sum()` still shows missing values. Why?**
> A: `.fillna()` returns a new Series by default — must reassign: `df["age"] = df["age"].fillna(...)`.

**Q: A p-value of 0.04 comes from a study with n=100,000. Is the finding necessarily important?**
> A: Not necessarily — huge samples make even tiny, practically meaningless differences statistically significant. Always check effect size alongside the p-value.

**Q: A Seaborn plot inside `plt.subplots(1, 2)` shows up as a stray extra figure instead of filling its subplot slot. Why?**
> A: Forgot to pass `ax=ax` — without it, Seaborn draws on its own new Figure/Axes instead of the one already created.

---

## 5. SQL for Data Science

*(Module 11)*

### 🟢 Beginner

**Q: `WHERE` vs. `HAVING`?**
> A: `WHERE` filters rows before grouping/aggregation; `HAVING` filters groups after aggregation — the only place you can filter on an aggregate like `SUM()`.

**Q: `INNER JOIN` vs. `LEFT JOIN`?**
> A: `INNER JOIN` keeps only rows matched on both sides. `LEFT JOIN` keeps every row from the left table, filling `NULL` for unmatched right-side columns.

**Q: Why never build a query with an f-string-inserted variable?**
> A: SQL injection risk — untrusted input could contain SQL syntax that changes the query's meaning. Parameterized queries (`?` placeholders) always treat the value as pure data.

### 🟡 Intermediate

**Q: When would you use a subquery instead of a `JOIN`?**
> A: When comparing individual rows against a single aggregate computed from the same/related table (e.g., "employees earning more than the company average") — a case a plain join+`GROUP BY`/`HAVING` can't express as directly.

**Q: Benefit of a CTE (`WITH`) over a nested subquery?**
> A: Readability — names each logical step so you read top-to-bottom instead of parsing inward through nesting. Often functionally/performance-equivalent to the nested version.

**Q: How would you divide work between SQL and Pandas on a 50M-row table?**
> A: Filter/join/aggregate as much as possible in SQL first, so only the reduced result set gets pulled into a DataFrame; do statistics/viz/ML in Pandas once the data's a manageable size.

### Practical / Coding

```sql
-- Top N overall (true per-group top-N needs window functions, beyond this module)
SELECT name, department, salary FROM employees ORDER BY salary DESC LIMIT 3;
```
```python
cursor.execute("SELECT * FROM orders WHERE amount > ?", (min_amount,))
```
```sql
-- Customers who never ordered
SELECT customers.name FROM customers
LEFT JOIN orders ON customers.id = orders.customer_id
WHERE orders.id IS NULL;
```

### 🚩 Gotcha

**Q: `SELECT department, AVG(salary) FROM employees WHERE AVG(salary) > 90000 GROUP BY department;` fails. Why?**
> A: `WHERE` runs before aggregation, so it can't reference `AVG(salary)` — move the condition to `HAVING`.

**Q: `f"SELECT * FROM users WHERE username = '{username}'"` with `username = "x' OR '1'='1"` — what's the concrete risk?**
> A: Produces `... WHERE username = 'x' OR '1'='1'`, which is always true, returning every row — potentially bypassing login entirely. Fix with a parameterized query.

---

## 6. Classical ML: Foundations & Evaluation

*(Modules 12-13: scikit-learn basics, scaling/encoding, cross-validation)*

### 🟢 Beginner

**Q: Classification vs. regression?**
> A: Classification predicts a discrete category; regression predicts a continuous number. This determines which algorithms and metrics apply (accuracy/precision/recall vs. MSE/RMSE/R²).

**Q: Why split data into train/test sets?**
> A: Evaluating on the same data a model trained on can't distinguish genuine learning from memorization. A held-out test set gives an honest estimate of real-world performance.

**Q: Why do some algorithms need feature scaling while others don't?**
> A: Distance-based (KNN) or gradient-based (logistic regression, neural nets) algorithms can be dominated by whichever feature has the largest numeric range. Tree-based models split on one feature's thresholds at a time, so scale doesn't matter for them.

**Q: What is data leakage, in your own words?**
> A: Information that wouldn't be available at prediction time — most commonly from the test set — accidentally influencing training, making evaluation results look better than they'd really be.

### 🟡 Intermediate

**Q: Why can accuracy be misleading, and what would you check instead?**
> A: On imbalanced classes, a model that always predicts the majority class can score very high accuracy while being useless. Check precision/recall (and the confusion matrix) for the class that actually matters.

**Q: Explain the precision/recall tradeoff with an example.**
> A: Precision = "of what's flagged positive, how much is real?" Recall = "of what's really positive, how much did we catch?" Spam filtering favors precision (don't block real email); medical screening favors recall (don't miss a real case).

**Q: Why fit a scaler only on the training data, never the whole dataset?**
> A: The test set should simulate genuinely unseen data — computing scaling stats from the full dataset lets test values leak into preprocessing, inflating apparent performance. `.fit_transform()` on train, `.transform()` only on test.

**Q: Advantage of k-fold cross-validation over a single train/test split?**
> A: A single split's score depends heavily on which rows landed in test by chance. K-fold trains/evaluates k times with different holdouts, giving both a more reliable average and a sense of variance (via std across folds).

**Q: How would you diagnose overfitting vs. underfitting from train/test scores?**
> A: Both low & similar → underfitting (too simple). High train, notably lower test → overfitting (memorized training noise). High & similar → good fit.

### Practical / Coding

```python
# Correct train-only scaling
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)     # transform only, no re-fit

# Pipeline + ColumnTransformer + cross_val_score
preprocessor = ColumnTransformer([
    ("num", StandardScaler(), ["age", "income"]),
    ("cat", OneHotEncoder(), ["city"])
])
pipeline = Pipeline([("preprocessor", preprocessor), ("classifier", LogisticRegression())])
scores = cross_val_score(pipeline, X, y, cv=5)   # pass the whole pipeline, not just the model
```

### Scenario

**Q: A stakeholder is thrilled about a fraud model's 99% accuracy. How do you respond?**
> A: Ask to see the confusion matrix and recall for the fraud class specifically — if fraud is rare, "always predict not-fraud" already hits 99% while catching nothing. Precision/recall for the minority class tell the real story.

**Q: 99% test accuracy seems suspiciously high. What do you check first?**
> A: Data leakage — was any preprocessing (scaling, encoding, imputation, feature selection) fit on the full dataset before the split? Also check whether the target leaks information (a feature that's basically a proxy for the answer).

### 🚩 Gotcha

**Q: `model.predict([5.1, 3.5, 1.4, 0.2])` errors, but `model.predict([[5.1, 3.5, 1.4, 0.2]])` works. Why?**
> A: `.predict()` always expects a 2D array (rows of samples) — even one prediction needs the extra wrapping list.

**Q: A colleague scales the entire dataset with `.fit_transform(X)` before `train_test_split()`. Why is this a silent bug?**
> A: The scaler's mean/std get computed using data that will become the "unseen" test set — the code runs fine but the resulting score is optimistically biased. Split first, then fit only on train.

---

## 7. Unsupervised Learning & Ensembles

*(Modules 14-15: K-Means, PCA, Random Forest, boosting, hyperparameter search)*

### 🟢 Beginner

**Q: Supervised vs. unsupervised learning?**
> A: Supervised has labeled targets to predict; unsupervised has features only and discovers structure (like natural groupings) with no known answer to check against.

**Q: How does K-Means assign points to clusters?**
> A: Each point goes to its nearest centroid; the algorithm iterates — assign, recompute centroids as the mean of assigned points, repeat until stable.

**Q: What is an ensemble method, in plain terms?**
> A: Combining predictions from multiple models into one more accurate, more stable prediction — like polling a panel of experts instead of trusting one opinion. Random Forest and XGBoost/LightGBM are the two dominant approaches for tabular data.

**Q: Difference between a parameter and a hyperparameter?**
> A: A parameter is learned during training (coefficients, split thresholds); a hyperparameter is chosen before training (number of trees, max depth) and isn't derived from the data.

### 🟡 Intermediate

**Q: Why does inertia always decrease as K increases, and why does that complicate choosing K?**
> A: More clusters means points can always get closer to *some* centroid (zero inertia at one cluster per point) — so you can't just pick the lowest-inertia K. The elbow method looks for where additional clusters stop giving meaningfully large improvement.

**Q: Explain PCA without saying "eigenvector."**
> A: Creates new features (principal components) as weighted combinations of the originals, ordered so the first captures as much variance as possible, the second captures as much of what's left, etc. Keeping the first few can preserve 90%+ of the information while cutting dimensionality dramatically.

**Q: Core difference between bagging and boosting?**
> A: Bagging trains models independently/in parallel on random samples, then averages/votes — reduces variance. Boosting trains sequentially, each model correcting the last one's errors — can reduce bias and variance but is more tuning-sensitive and overfit-prone.

**Q: Why choose `RandomizedSearchCV` over `GridSearchCV`?**
> A: `GridSearchCV` tries every combination — grows combinatorially. `RandomizedSearchCV` samples a fixed budget (`n_iter`) of random combinations, usually finding a comparably good result in far less time.

**Q: A limitation of Random Forest/boosting feature importance?**
> A: Only reflects relative contribution to accuracy — no direction of effect (unlike a regression coefficient's sign), and can be misleading when features are correlated (importance gets "split" between them).

### Practical / Coding

```python
# K-Means + silhouette score
X_scaled = StandardScaler().fit_transform(X)
kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
labels = kmeans.fit_predict(X_scaled)
score = silhouette_score(X_scaled, labels)

# PCA variance preserved
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
variance_preserved = sum(pca.explained_variance_ratio_)

# Random Forest feature importance ranking
importance_df = pd.DataFrame({"feature": X.columns, "importance": model.feature_importances_}) \
    .sort_values("importance", ascending=False)

# RandomizedSearchCV on XGBoost
search = RandomizedSearchCV(xgb.XGBClassifier(random_state=42, eval_metric="logloss"),
    {"max_depth": randint(3, 10), "n_estimators": randint(50, 300)}, n_iter=15, cv=5, random_state=42)
search.fit(X_train, y_train)
```

### Scenario

**Q: A marketing team wants customer segments with no predefined categories. Approach?**
> A: Gather relevant features, scale them, run K-Means using elbow + silhouette to settle on cluster count, then profile each cluster's average feature values into human-readable descriptions the business team can act on.

**Q: Choosing between Random Forest and XGBoost with limited tuning time?**
> A: Random Forest is a safer, lower-effort baseline (reasonable defaults, less prone to bad overfitting). XGBoost can beat it but needs more careful tuning to realize that advantage — start with Random Forest, try a modest randomized search on XGBoost if time allows, compare on held-out data.

### 🚩 Gotcha

**Q: K-Means on unscaled data (one feature 0-1, another 0-100,000) produces clusters that seem to only reflect the second feature. Why?**
> A: Euclidean distance is dominated by the larger-range feature without scaling — differences in the small-range feature become numerically negligible. Fix: scale before clustering.

**Q: Someone picks hyperparameters by evaluating several combos directly against the test set, then reports that score as "final performance." What's wrong?**
> A: The test set became part of model selection — no longer a genuinely held-out evaluation. The reported score is optimistically biased. Select via cross-validation on training data only; touch the test set exactly once, at the end.

---

## 8. Deep Learning Foundations

*(Module 16: neurons, backprop, PyTorch vs. Keras, dropout, early stopping)*

### 🟢 Beginner

**Q: What does a single artificial neuron compute?**
> A: Weighted sum of inputs plus a bias, passed through an activation function. The weighted sum alone is structurally identical to linear regression — the activation function is what adds real modeling power.

**Q: Why are activation functions necessary?**
> A: Without them, stacking layers collapses mathematically into one linear transformation, no matter how many layers — only able to learn a straight-line relationship. Activations introduce the non-linearity that makes depth useful.

### 🔴 Advanced

**Q: Explain backpropagation and gradient descent together.**
> A: Backpropagation computes how much each weight contributed to the loss, working backward via the chain rule. Gradient descent then nudges every weight in the loss-reducing direction, repeated over epochs. Backprop computes *how*; gradient descent performs the *update*.

**Q: How does dropout reduce overfitting, and why disable it at evaluation time?**
> A: Randomly deactivates a fraction of neurons per training step, preventing over-reliance on any narrow combination — forcing more robust, redundant representations (same spirit as Random Forest's bagging). Disabled at eval time because you want the full, best network making the prediction, not a weakened random subset of it.

**Q: PyTorch vs. Keras — practical difference given identical underlying concepts?**
> A: PyTorch requires an explicit training loop (`zero_grad`, forward, loss, `backward`, `step`) — full visibility/control, good for research/custom logic. Keras condenses this into `.compile()`/`.fit()` — much less code, good for rapid prototyping of standard architectures.

### Practical / Coding

```python
# Minimal PyTorch training loop
for epoch in range(100):
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()
```
```python
# Keras: dropout + early stopping
model = keras.Sequential([
    keras.layers.Input(shape=(n_features,)),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(n_classes, activation="softmax")
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
early_stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
model.fit(X_train, y_train, epochs=200, validation_split=0.2, callbacks=[early_stop])
```

### Scenario

**Q: Training accuracy hits 100% fast; test accuracy plateaus much lower. What do you try?**
> A: Classic overfitting — add dropout, consider reducing network capacity relative to dataset size, and use early stopping on a validation split rather than continuing to train an already-overfit model.

### 🚩 Gotcha

**Q: Loss is stuck at a high value across many epochs. Likely causes?**
> A: Learning rate too high (overshoots) or too low (imperceptible progress); in PyTorch specifically, forgetting `optimizer.zero_grad()` causes gradients to wrongly accumulate across steps.

**Q: A PyTorch model performs much worse at eval time than training metrics suggested, with no data leakage. Why?**
> A: Forgot `model.eval()` — dropout is still randomly deactivating neurons during "evaluation," producing noisier, non-deterministic results. Always call `.eval()` before evaluating/predicting.

---

## 9. Computer Vision (CNNs)

*(Module 17: convolution, pooling, transfer learning, augmentation)*

### 🟢 Beginner

**Q: Why not just flatten an image into a plain feedforward network?**
> A: Destroys 2D spatial structure and needs an enormous number of weights (one per pixel per neuron) — wasteful and overfit-prone. Convolution reuses a small set of filters across the whole image, preserving locality and cutting parameters dramatically.

**Q: What does a convolutional filter do?**
> A: A small grid of learned weights sliding across the image, computing a local weighted sum at each position — a reusable pattern detector (edges, corners, textures).

**Q: What is pooling, and why use it?**
> A: Summarizes small regions of a feature map down to one value (commonly max), reducing computation and adding robustness to small positional shifts.

### 🟡 Intermediate

**Q: Explain transfer learning and why it's the standard for most real-world CV projects.**
> A: Start from a model pretrained on a huge, general dataset (e.g. ImageNet), reuse its early general features (edges/textures/shapes), and retrain only a new final layer for your specific task. Most real projects have far too little labeled data to train a large CNN from scratch without severe overfitting.

**Q: How would you adapt a pretrained 1000-class ImageNet model to a 5-class task?**
> A: Freeze all existing layers (`requires_grad=False` / `.trainable=False`), replace the final classification layer with one sized for 5 outputs, and train only that new layer.

**Q: Why does data augmentation help with limited training data?**
> A: Creates varied versions of existing images on the fly (rotated, flipped, zoomed), exposing the model to more diversity without collecting new data — directly reduces overfitting since it can't just memorize a small fixed set.

### Practical / Coding

```python
# Freeze pretrained ResNet18, replace final layer
model = models.resnet18(weights="IMAGENET1K_V1")
for param in model.parameters():
    param.requires_grad = False
model.fc = nn.Linear(model.fc.in_features, 20)
```
```python
# Keras augmentation chosen to preserve label meaning for animal photos
data_augmentation = keras.Sequential([
    keras.layers.RandomFlip("horizontal"),
    keras.layers.RandomRotation(0.1),
    keras.layers.RandomZoom(0.1)
])
```

### Scenario

**Q: Only 300 labeled images for a new product-defect classifier, need production quickly. Approach?**
> A: Transfer learning from a pretrained model (ResNet/MobileNet), freeze the base, train only a new final layer; add realistic augmentation to stretch the effective dataset size; use dropout/early stopping to guard against overfitting the small new layer.

### 🚩 Gotcha

**Q: A CNN throws a shape mismatch at the first `nn.Linear` after the conv layers. Cause?**
> A: `in_features` doesn't match the actual flattened output size of the conv/pooling stack — must be calculated precisely from input dimensions and pooling steps (each 2×2 max pool halves both spatial dims), not guessed.

**Q: `RandomHorizontalFlip` hurts a handwritten-digit classifier. Why?**
> A: Flipping certain digits changes or invalidates their meaning — augmentations must be chosen based on what actually preserves the label for the specific data, not applied as a generic default.

---

## 10. NLP & Transformers

*(Module 18: tokenization, embeddings, self-attention, Hugging Face pipelines)*

### 🟢 Beginner

**Q: What is tokenization, and why subword tokenization over whole-word?**
> A: Splits raw text into model-processable units. Whole-word tokenization hits a hard "unknown word" wall for anything outside a fixed vocabulary; subword tokenization breaks rare/unseen words into familiar fragments, so virtually any input is representable.

**Q: What is a word embedding, and why better than a raw token ID?**
> A: A raw ID is an arbitrary index carrying no meaning. An embedding is a dense learned vector positioned so semantically similar words end up with similar vectors — capturing real relationships.

**Q: What problem does self-attention solve that RNNs struggled with?**
> A: RNNs process sequentially, so information from early tokens fades by the time later ones are reached — hard to capture long-range dependencies. Self-attention lets every word consider every other word directly, regardless of distance.

### 🟡 Intermediate

**Q: Explain Query, Key, Value in self-attention.**
> A: Query = what a word is looking for; Key = what each word advertises about itself; Value = the content contributed once relevant. Q·K produces compatibility scores, softmax-normalized into attention weights that blend each word's Value into the output.

**Q: Encoder-only (BERT) vs. decoder-only (GPT)?**
> A: Encoders read the whole input at once, bidirectional understanding — good for classification/understanding tasks. Decoders generate one token at a time, attending to what's already generated — good for generation tasks.

**Q: What does `pipeline("zero-shot-classification")` do, and why remarkable?**
> A: Classifies text into categories never specifically trained on, by comparing meaning against candidate labels given at request time — showing how much general language understanding pretraining actually captures.

### Practical / Coding

```python
# Sentiment classification without pipeline()
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)
inputs = tokenizer("This movie was fantastic!", return_tensors="pt")
with torch.no_grad():
    logits = model(**inputs).logits
    predicted_class = torch.argmax(logits, dim=1).item()
```
```python
# Self-attention scores from scratch
scores = Q @ K.T / np.sqrt(K.shape[1])
attention_weights = softmax(scores)
output = attention_weights @ V
```

### Scenario

**Q: 15 custom support-ticket categories, no labeled data yet. First try?**
> A: `pipeline("zero-shot-classification")` with the 15 categories as candidate labels — no training data needed, potentially usable immediately; use it to bootstrap labeled data for a dedicated fine-tuned classifier later if accuracy isn't sufficient.

### 🚩 Gotcha

**Q: A pipeline call using `grouped_entities=True` suddenly raises `TypeError` after a library upgrade. Explanation?**
> A: APIs evolve — that NER argument was replaced by `aggregation_strategy="simple"` in newer `transformers` versions. Always check current docs after an upgrade rather than assuming old tutorial code still works.

**Q: A sentiment classifier confidently returns "NEGATIVE" for a genuinely neutral/ambiguous sentence. Why?**
> A: Many sentiment models are strictly binary (no neutral category) — forced to pick a bucket even for lukewarm input. Check what categories a pretrained model actually supports before trusting edge cases.

---

## 11. Generative AI, LLMs & RAG

*(Module 19: prompting, embeddings similarity, RAG architecture)*

### 🟢 Beginner

**Q: What is an LLM, in terms of architecture you already know?**
> A: A very large decoder-only Transformer trained on next-token prediction over enormous text — at sufficient scale this simple objective produces coherent writing, QA, and instruction-following.

**Q: Zero-shot vs. few-shot prompting?**
> A: Zero-shot describes the task in words only; few-shot provides labeled examples in the prompt first, showing the desired format/reasoning — usually more reliable.

**Q: Why never hard-code an API key in source code?**
> A: If committed/shared, the key is exposed to anyone with repo access. Load from an environment variable or secrets manager instead.

### 🟡 Intermediate

**Q: Explain RAG and the specific problem it solves.**
> A: Combines semantic search over your own documents with an LLM's generation — retrieved context is inserted into the prompt so the answer is grounded in that specific data, not just the model's frozen pretraining knowledge (which knows nothing about your private/recent/internal data).

**Q: Why does chunk size matter in a RAG pipeline?**
> A: Too small loses context (awkward mid-sentence splits); too large dilutes retrieval specificity and wastes prompt space. Chunk overlap mitigates the awkward-split problem. Right size is a practical tuning decision.

**Q: Why instruct an LLM to answer "using only the provided context"?**
> A: Without it, the model may blend in its own general knowledge, undermining RAG's grounding/traceability purpose, and may fail to recognize when the context genuinely doesn't answer the question.

### Practical / Coding

```python
# Cosine similarity between two embeddings
similarity = np.dot(embedding_a, embedding_b) / (np.linalg.norm(embedding_a) * np.linalg.norm(embedding_b))

# LangChain FAISS retrieval
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_texts(documents, embeddings)
def retrieve_context(query, k=2):
    results = vectorstore.similarity_search(query, k=k)
    return "\n".join(doc.page_content for doc in results)
```

### Scenario

**Q: An LLM support tool gives confidently wrong answers on topics your documents don't cover. How do you address this?**
> A: Confirm the prompt explicitly instructs "say you don't know if context doesn't help." Add a relevance-score threshold on retrieval — if the top score is below a measured cutoff, treat it as "no relevant info" and skip generation entirely rather than handing irrelevant context to the LLM.

**Q: Company wants an internal HR-policy chatbot. Approach?**
> A: Textbook RAG — chunk the policy docs, embed/index (sentence-transformers + FAISS via LangChain), retrieve top-k relevant chunks per question, hand to an LLM instructed to answer only from that context — grounding answers in current, actual company policy rather than the model's generic knowledge.

### 🚩 Gotcha

**Q: A RAG pipeline retrieves documents for a totally unrelated query. Is this a bug?**
> A: No — standard similarity search (e.g. FAISS `IndexFlatL2`) always returns its top-k *closest* matches by design, with no built-in "no good match" concept unless you check scores against a threshold. This is exactly why RAG prompts need an explicit "say you don't know" instruction, and why production systems add a relevance cutoff.

**Q: Why can higher `temperature` help creative writing but hurt data extraction/classification?**
> A: Higher temperature adds randomness to next-token choices — valuable for creative diversity, harmful for tasks needing one precise, reproducible answer. `temperature=0` is preferred for deterministic, structured tasks.

---

## 12. MLOps & Deployment

*(Module 20: serialization, FastAPI, Docker, monitoring/drift)*

### 🟢 Beginner

**Q: Why save a trained model instead of retraining on every request?**
> A: Training is expensive (minutes to days); a production API needs millisecond responses. Train once, save, then load/reuse for every prediction.

**Q: Why save the entire preprocessing + model pipeline, not just the bare model?**
> A: New data must go through the exact same transformation the model trained on — saving just the model risks inconsistent/missing preprocessing at prediction time.

**Q: What is a REST API, and why natural for serving a model?**
> A: Exposes functionality over HTTP — language-agnostic, so any system able to make an HTTP request can consistently call the same deployed model.

### 🟡 Intermediate

**Q: Why is Docker useful beyond "packaging the code"?**
> A: Packages the entire runtime — exact Python/library versions, system dependencies — into one portable image, eliminating "works on my machine" problems regardless of the host.

**Q: Data drift vs. model (concept) drift?**
> A: Data drift = input feature distribution shifted from training. Concept drift = the actual relationship between features and target changed, even if inputs look similar. Both erode a model's original accuracy but from different causes.

**Q: Why monitor input drift before you even have new ground-truth labels?**
> A: True labels often arrive with significant delay (or never). Input feature/prediction-distribution shifts are available immediately, giving an early warning before a delayed accuracy check could confirm anything.

### Practical / Coding

```python
# Drift detection with KS test
from scipy import stats
def check_drift(training_data, production_data, alpha=0.05):
    stat, p_value = stats.ks_2samp(training_data, production_data)
    return p_value < alpha, stat, p_value
```
```python
# FastAPI endpoint with Pydantic validation
class InputData(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(data: InputData):
    X = np.array(data.features).reshape(1, -1)
    prediction = model.predict(X)
    return {"prediction": int(prediction[0])}   # cast from numpy.int64
```

### Scenario

**Q: A stakeholder says a 6-month-deployed fraud model "feels less accurate," but no recent labels exist yet. How do you investigate?**
> A: Check what's available immediately — input feature drift (KS test vs. training distribution) and shifts in the prediction distribution (e.g. % flagged as fraud). Either supports the concern and helps prioritize retraining even before labels arrive.

**Q: A containerized model API works locally with `uvicorn` but not responding inside Docker. First checks?**
> A: App bound to `0.0.0.0`, not `localhost` (localhost is unreachable from outside the container); the `-p host:container` port mapping matches what the app listens on; `docker logs` for startup errors like a missing dependency.

### 🚩 Gotcha

**Q: A FastAPI endpoint occasionally throws a serialization error on predictions that work fine in a plain script. Why?**
> A: The output is still a NumPy type (`numpy.int64`/`float32`) — FastAPI's default JSON encoder doesn't know how to serialize those. Cast to plain `int`/`float` before returning.

**Q: A drift alert fires and someone retrains immediately without investigating. Risk?**
> A: Drift doesn't automatically mean genuine harmful change — could be a pipeline bug or seasonal effect. Retraining blind risks wasted effort, or worse, training on the very corrupted data that triggered the alert.

---

## 13. Scenario Spotlight — Cross-Cutting System Design

These pull together concepts across multiple modules — the kind of question that reveals whether a candidate can connect the whole pipeline, not just one topic in isolation.

**Q: Walk me through building an end-to-end churn-prediction system from raw data to a monitored production API.**
> A: Pull/clean data (Modules 07-08: handle missing values, fix dtypes, dedupe), EDA to understand drivers and class balance (Module 10), engineer + scale/encode features with train-only fitting (Module 13), try a few models with cross-validation and a hyperparameter search (Modules 12/15), pick based on the metric that matters for the business (likely recall-weighted given churn's cost asymmetry), save the full pipeline (Module 20), wrap it in a FastAPI endpoint with Pydantic validation, containerize with Docker, and monitor input drift plus the prediction distribution post-deployment as an early-warning signal before new labels arrive.

**Q: A tabular ML model and a small custom RAG chatbot both need to ship. How do the engineering concerns differ?**
> A: The tabular model's core risk is train/test leakage and drift over time — solved with disciplined pipelines, cross-validation, and monitoring (Modules 12-13, 20). The RAG chatbot's core risk is ungrounded/hallucinated answers — solved with retrieval-relevance thresholds and explicit "only answer from context" prompting (Module 19), plus logging retrieval scores/fallback rates as its own form of monitoring. Both ultimately need the same discipline: measure before you trust, and monitor because the world will drift out from under any static model.

**Q: How would you decide whether a problem needs classical ML or a deep learning approach at all?**
> A: Start simple — a well-engineered classical model (Random Forest/XGBoost, Modules 12-15) is usually the right first attempt for structured/tabular data, is faster to iterate on, and is easier to explain to stakeholders. Reach for deep learning specifically when the data is unstructured (images, text) and there's enough volume to support it (or a strong pretrained model to transfer-learn from) — training a huge network from scratch on a small tabular dataset is a bad trade versus a tuned ensemble.

**Q: Your model's cross-validated metrics look great, but the team is nervous about deploying it. What would you want to see before shipping?**
> A: A confusion matrix at the actual decision threshold you'll use in production (not just an aggregate metric), a sanity check that there's no leakage anywhere in the pipeline (Module 13), an understanding of the cost of false positives vs. false negatives for this specific business use case, and a monitoring plan (Module 20) so degraded real-world performance gets caught early rather than discovered by a stakeholder complaint months later.

---

## 14. Gotcha Hall of Fame

The traps interviewers reach for most — usually because they reveal whether you've actually run the code, not just read about it.

| # | The Trap | The Fix |
|---|----------|---------|
| 1 | `def f(items=[]):` — mutable default argument | Default values evaluate once at definition time; use `items=None` + create fresh inside the body |
| 2 | `p1 == p2` is `False` for identical-looking objects | No custom `__eq__` → falls back to identity comparison |
| 3 | `5 / 2` gives `2.5`, `5 // 2` gives `2` | `/` always returns float in Python 3; `//` is floor division |
| 4 | `arr[1:3]` modifies the original array | NumPy slices are views, not copies — use `.copy()` |
| 5 | `if arr > 2 and arr < 5:` → `ValueError` | Use `&`/`\|` with parentheses on arrays/Series, not `and`/`or` |
| 6 | `df.drop(columns=[...])` doesn't remove the column | Returns a new DataFrame — reassign, or use `inplace=True` |
| 7 | `df["age"].fillna(mean)` — missing values remain | Same as above — must reassign the result |
| 8 | `df["col"] == np.nan` never matches | `NaN != NaN` by IEEE spec — use `.isna()` |
| 9 | `WHERE AVG(salary) > 90000` fails | Aggregates aren't computed yet when `WHERE` runs — use `HAVING` |
| 10 | `f"...{username}..."` in a SQL string | SQL injection — always use parameterized `?` placeholders |
| 11 | `model.predict([5.1, 3.5, 1.4, 0.2])` errors | scikit-learn always expects a 2D array, even for one sample |
| 12 | Scaling the whole dataset before `train_test_split` | Silent leakage — split first, `fit_transform` only on train |
| 13 | Choosing hyperparameters by peeking at test-set scores | Test set becomes part of model selection — no longer a fair evaluation |
| 14 | K-Means clusters dominated by one large-range feature | Distance-based algorithms need scaling first |
| 15 | Loss stuck high, never decreasing (PyTorch) | Forgot `optimizer.zero_grad()`, or bad learning rate |
| 16 | Worse eval-time performance despite good training metrics | Forgot `model.eval()` — dropout still active |
| 17 | CNN shape mismatch at the first `nn.Linear` | `in_features` must be precisely calculated from conv/pool output size |
| 18 | `grouped_entities=True` suddenly `TypeError`s | Library API evolved — now `aggregation_strategy="simple"` |
| 19 | RAG retrieves irrelevant docs for an unrelated query | Similarity search always returns top-k by design — add a relevance threshold |
| 20 | FastAPI serialization error on a working script's output | NumPy types (`int64`/`float32`) aren't JSON-serializable — cast to plain Python types |
| 21 | `pip install X` succeeds but `import X` fails | venv not activated during install, or wrong interpreter selected |
| 22 | Committed API key to a public repo | Rotate the key immediately — deleting the file doesn't erase git history |

---

## 15. Master Quick-Fire Rapid Review

Blitz through these before an interview — if any answer doesn't come instantly, jump back to that section above.

**Python & OOP**
- List vs. tuple mutability? → **list mutable, tuple immutable**
- `==` vs `is`? → **value equality vs. object identity**
- What does a function with no `return` give back? → **`None`**
- Never use this as a default argument → **a mutable object (`[]`, `{}`)**
- First parameter of every instance method? → **`self`**
- Safer dunder to always define, `__str__` or `__repr__`? → **`__repr__`**

**Tooling, Files, APIs**
- What guarantees a file closes even on error? → **`with` (context manager)**
- File mode that erases existing content? → **`"w"`**
- Does `requests.get()` raise on a 404 by itself? → **No — check `.status_code` / `raise_for_status()`**
- Command to export exact installed packages? → **`pip freeze > requirements.txt`**
- File that tells git what to never track? → **`.gitignore`**

**NumPy & Pandas**
- Why is vectorization faster than a Python loop? → **looping happens in compiled C, not the interpreter**
- Axis that collapses to give per-column results? → **`axis=0`**
- `.loc` vs `.iloc` slice-end behavior? → **inclusive vs. exclusive**
- Default `how` for `pd.merge()`? → **`"inner"`**
- Correct operator for combining array/Series conditions? → **`&` / `|`, not `and`/`or`**

**Cleaning, Viz, Stats**
- Correct way to check for missing values? → **`.isna()`/`.notna()`**
- More robust to outliers, mean or median? → **median**; IQR or z-score? → **IQR**
- Does correlation imply causation? → **No**
- What does a p-value measure? → **P(data this extreme \| H₀ true)**
- What can a p-value NOT tell you alone? → **practical/effect-size importance**

**SQL**
- Filters rows before grouping? → **`WHERE`**; after? → **`HAVING`**
- Join keeping every left-table row? → **`LEFT JOIN`**
- Safe way to include a variable in a query? → **parameterized `?` placeholder**

**Classical ML**
- Metric misleading on imbalanced classes? → **accuracy**
- What must happen before any preprocessing is fit? → **the train/test split**
- High train score + low test score = ? → **overfitting**
- What should you pass to `cross_val_score` — model or pipeline? → **the full pipeline**

**Unsupervised & Ensembles**
- Metric that always decreases as K increases? → **inertia**
- Metric for clustering quality without labels? → **silhouette score**
- Bagging trains models how? → **independently, in parallel**; boosting? → **sequentially, correcting errors**
- Is scaling required before tree-based ensembles? → **No**

**Deep Learning / CV / NLP / GenAI**
- What does an activation function add? → **non-linearity**
- Technique that randomly deactivates neurons in training? → **dropout**
- What must you call before evaluating a PyTorch model? → **`model.eval()`**
- Why reuse a pretrained CNN instead of training from scratch? → **far less data/compute needed (transfer learning)**
- What lets every token attend to every other regardless of distance? → **self-attention**
- What does RAG stand for, and its three steps? → **Retrieval-Augmented Generation — retrieve, augment, generate**
- What does `temperature=0` produce? → **deterministic, reproducible output**

**MLOps**
- What should you save alongside a trained model? → **the full preprocessing pipeline**
- What must NumPy prediction outputs be cast to before an API returns them? → **plain Python types**
- Test used for detecting data drift? → **Kolmogorov-Smirnov (`ks_2samp`)**
- Which is available sooner: input drift detection or ground-truth accuracy? → **input drift detection**

---

**This is the final master file for the course.** See [`master-cheatsheet.md`](master-cheatsheet.md) for quick on-the-job syntax reference, and [`master-references.md`](master-references.md) for curated learning resources to go deeper on any topic above.
