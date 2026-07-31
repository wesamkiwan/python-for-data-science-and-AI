# Module 10c: The Full EDA Workflow

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [02-correlation-and-hypothesis-testing.md](02-correlation-and-hypothesis-testing.md)

## 🎯 Learning Objectives
- [ ] Execute a complete, end-to-end EDA workflow on a realistic dataset
- [ ] Combine skills from Modules 06-10 into one coherent analysis
- [ ] Write up findings clearly, distinguishing description from inference
- [ ] Recognize this workflow as a repeatable habit for any new dataset

---

## Module Goal

This lesson has no major new concepts — instead, it's a **capstone-style walkthrough** that combines everything from Modules 06 (NumPy) through 10 (Statistics) into one realistic, end-to-end **Exploratory Data Analysis (EDA)**. This is exactly the shape of work you'll do at the start of nearly every real data science project.

## Why This Matters on the Job

Nobody hands you a clean dataset and a pre-defined question. Real work starts with a messy file and a vague business question ("how are we doing on compensation across departments?"), and *you* have to load it, clean it, explore it, test your hunches statistically, visualize the story, and write up what you actually found — in that order, as a repeatable habit. This lesson is that habit, demonstrated start to finish.

---

## The Scenario

You've been given employee data and asked: **"Is there a meaningful salary difference between departments, and what does the overall salary picture look like?"**

```python
import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(123)
n = 300
df = pd.DataFrame({
    "employee_id": range(1, n + 1),
    "department": np.random.choice(
        ["Engineering", "Sales", "Marketing", "Support"], n, p=[0.35, 0.25, 0.2, 0.2]
    ),
    "years_experience": np.random.randint(0, 25, n),
    "salary": np.concatenate([
        np.random.normal(95000, 18000, int(n * 0.35)),
        np.random.normal(70000, 12000, int(n * 0.25)),
        np.random.normal(65000, 10000, int(n * 0.2)),
        np.random.normal(55000, 8000, n - int(n * 0.35) - int(n * 0.25) - int(n * 0.2))
    ]),
    "satisfaction_score": np.random.randint(1, 11, n),
})
df.loc[5:10, "salary"] = np.nan     # simulate some missing records
df.loc[0, "salary"] = 800000          # simulate a data-entry error
```

## Step 1: First Look (Module 07)

```python
print(df.head())
print(df.shape)               # (300, 5)
print(df.isna().sum())           # salary: 6 missing, everything else: 0
```

**How it works:** Exactly the "first three commands on any dataset" habit from Module 07 — before touching the actual question, confirm what you're working with.

## Step 2: Clean the Data (Module 08)

```python
q1 = df["salary"].quantile(0.25)
q3 = df["salary"].quantile(0.75)
iqr = q3 - q1
lower_bound, upper_bound = q1 - 1.5 * iqr, q3 + 1.5 * iqr

outliers = df[(df["salary"] < lower_bound) | (df["salary"] > upper_bound)]
print(outliers[["employee_id", "salary"]])
```
```
    employee_id         salary
0             1  800000.000000
73           74  133799.075581
77           78  144273.380855
82           83  131780.596223
98           99  128413.285010
```

**How it works:** The IQR method flags the obvious `800000` data-entry error *and* four other genuinely high (but plausible) salaries. This is exactly the judgment call from Module 08c — the `800000` value is almost certainly an error, but the other four might be legitimate senior salaries worth keeping. For this analysis, we'll treat all five as outliers to exclude from the main statistical picture, but a real analysis would investigate each one individually before deciding.

```python
df_clean = df[
    df["salary"].isna() | ((df["salary"] >= lower_bound) & (df["salary"] <= upper_bound))
].copy()

df_clean["salary"] = df_clean["salary"].fillna(df_clean["salary"].median())
print(df_clean.isna().sum())   # all zero now
```

**How it works:** The filter keeps rows that are either still missing (to be filled next) or within the acceptable range — dropping the 5 outlier rows. Then, missing `salary` values are filled with the *median* (Module 10a's lesson: robust to outliers, and salary data is a classic right-skewed case).

## Step 3: Descriptive Statistics (Module 10a)

```python
print(df_clean["salary"].describe())
print(f"Skewness: {df_clean['salary'].skew():.2f}")
```
```
count       295.000000
mean      74357.708885
std       19772.669580
min       38719.246738
25%       60035.471091
50%       69971.552661
75%       84805.148347
max      126591.579298
Skewness: 0.61
```

**How it works:** A skewness of `0.61` confirms a moderate right skew — consistent with salary data generally (a majority of typical salaries, with a longer tail toward higher earners), reinforcing that the median (not just the mean) deserves attention in any writeup.

## Step 4: Visualize (Module 09)

```python
import seaborn as sns
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(12, 4))
sns.histplot(data=df_clean, x="salary", kde=True, ax=axes[0])
axes[0].set_title("Salary Distribution")

sns.boxplot(data=df_clean, x="department", y="salary", ax=axes[1])
axes[1].set_title("Salary by Department")
fig.savefig("eda_salary_overview.png", dpi=150, bbox_inches="tight")
```

**How it works:** The histogram visually confirms the right-skew already measured numerically; the box plot gives an immediate visual sense of whether departments' salary ranges actually overlap much, ahead of any formal statistical test.

## Step 5: Group Comparison (Module 07 + Module 10a)

```python
print(df_clean.groupby("department")["salary"].agg(["mean", "median", "std", "count"]))
```
```
                     mean        median           std  count
department
Engineering  74939.173838  72533.153331  20227.275277     99
Marketing    79721.906147  77967.449003  22312.223201     57
Sales        71901.592347  67862.390944  17716.964812     83
Support      71510.090996  68772.467802  18389.501723     56
```

**How it works:** Marketing shows the highest average, but the standard deviations are all fairly large *relative to* the differences between department means — a strong hint (before running any formal test) that these differences might not hold up statistically.

## Step 6: Correlation Check (Module 09/10b)

```python
print(df_clean[["years_experience", "salary", "satisfaction_score"]].corr())
```
```
                    years_experience    salary  satisfaction_score
years_experience            1.000000  0.060563            0.057593
salary                      0.060563  1.000000           -0.014314
satisfaction_score          0.057593 -0.014314            1.000000
```

**How it works:** All correlations here are very close to zero — in this dataset, years of experience barely relates to salary or satisfaction at all. That's a real, useful (if slightly anticlimactic) finding — not every dataset has strong relationships, and reporting "we found no meaningful relationship" honestly is just as valuable as reporting a strong one.

## Step 7: Formal Hypothesis Test (Module 10b)

The box plot suggested Engineering and Support might differ — let's test that specific comparison formally:

```python
engineering_salaries = df_clean[df_clean["department"] == "Engineering"]["salary"]
support_salaries = df_clean[df_clean["department"] == "Support"]["salary"]

t_stat, p_value = stats.ttest_ind(engineering_salaries, support_salaries)
print(f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}")
```
```
t-statistic: 1.0470, p-value: 0.2967
```

**How it works:** `p-value = 0.30`, well above the conventional `α = 0.05` threshold — we **fail to reject the null hypothesis**. Despite Engineering's higher sample mean, the difference isn't statistically significant given the amount of variability in the data. This is an important, honest conclusion: eyeballing a bar chart or a groupby table alone would have been misleading here without the formal test.

## Step 8: Write Up Findings

A real EDA concludes with a clear, honest summary — here's what a professional writeup of this analysis would say:

> **Findings:** After removing 5 salary outliers (including one likely data-entry error of $800,000) and filling 6 missing salary values with the dataset median, the cleaned salary distribution shows a moderate right skew (0.61), consistent with typical salary data. While Marketing showed the highest average salary ($79,722) and Support the lowest ($71,510) across departments, a t-test comparing Engineering and Support specifically found this difference is **not statistically significant** (p = 0.30) given the variability within each department. No meaningful correlation was found between years of experience and either salary or satisfaction score in this dataset (all correlations near 0). **Recommendation:** the apparent department salary differences do not currently have strong statistical support and should not be treated as a confirmed pattern without a larger sample or further investigation into the specific outlier salaries flagged during cleaning.

✅ **Best Practice:** Notice this writeup explicitly separates **description** ("Marketing's average is highest") from **inference** ("but this isn't statistically significant") — this distinction, made clearly and honestly, is the single biggest marker of a trustworthy analysis versus a misleading one.

---

## Hands-On Exercise

**Task:** Using the `df_clean` DataFrame built throughout this lesson, write `full_eda_capstone.py` that additionally:
1. Runs a t-test comparing `satisfaction_score` between employees with `years_experience > 10` vs. `<= 10`.
2. Creates a Seaborn scatter plot of `years_experience` vs. `salary`, colored by `department`, and saves it.
3. Writes a 3-4 sentence findings summary (as a Python multi-line string or comment) covering: what you tested, the result (with the actual p-value), and a recommendation — following the same description-vs-inference discipline from Step 8 above.

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd
import numpy as np
from scipy import stats
import seaborn as sns
import matplotlib.pyplot as plt

# (Assumes df_clean has already been built as shown earlier in this lesson)

experienced = df_clean[df_clean["years_experience"] > 10]["satisfaction_score"]
less_experienced = df_clean[df_clean["years_experience"] <= 10]["satisfaction_score"]

t_stat, p_value = stats.ttest_ind(experienced, less_experienced)
print(f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}")

fig, ax = plt.subplots()
sns.scatterplot(data=df_clean, x="years_experience", y="salary", hue="department", ax=ax)
ax.set_title("Years of Experience vs. Salary, by Department")
fig.savefig("experience_vs_salary.png", dpi=150, bbox_inches="tight")

findings = f"""
Findings: A t-test comparing satisfaction scores between more-experienced
(>10 years) and less-experienced (<=10 years) employees found
p={p_value:.4f}, which is {'below' if p_value < 0.05 else 'above'} the
0.05 significance threshold -- meaning the observed difference in
satisfaction is {'statistically significant' if p_value < 0.05 else
'not statistically significant'} in this sample. Recommendation:
{'investigate further, as tenure appears related to satisfaction' if
p_value < 0.05 else 'do not treat experience level as a meaningful driver of satisfaction based on this data alone'}.
"""
print(findings)
```

**Expected outcome:** Given the dataset was generated with `satisfaction_score` fully independent of `years_experience`, the t-test should show no statistically significant difference (a p-value comfortably above 0.05) — the correct, honest conclusion for randomly-generated, unrelated data.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Jumping straight to a groupby/chart without first checking for missing data/outliers | Always run the Module 07-08 cleaning steps before trusting any statistic |
| Reporting a group difference from `.groupby()` as fact without testing it | Follow up any apparent difference with a formal test (t-test, chi-square) |
| Blending description and inference in a writeup without distinguishing them | Explicitly separate "here's what the data shows" from "here's what's statistically supported" |
| Skipping the writeup step entirely | A finding that isn't communicated clearly didn't accomplish its purpose |

---

## ✅ Module 10 Completion Checklist
- [ ] Can execute a complete EDA workflow: inspect → clean → describe → visualize → test → conclude
- [ ] Can combine skills from Modules 06-10 into one coherent analysis
- [ ] Can write a findings summary that clearly separates description from statistical inference
- [ ] Completed the `full_eda_capstone.py` exercise
- [ ] Reviewed [`module10-cheatsheet.md`](module10-cheatsheet.md)
- [ ] Reviewed [`module10-interview.md`](module10-interview.md)
- [ ] Browsed [`module10-references.md`](module10-references.md)

**Next Step:** Module 11 — SQL for Data Scientists (`phase2-data-science-core/module11-sql-for-data-science/`)

---

## 🎉 Almost There!

This module wraps up the analytical core of Phase 2 — you can now take a raw, messy dataset all the way to a statistically-grounded, honestly-communicated finding. Module 11 (SQL) rounds out Phase 2 by teaching you how to *retrieve* the data you'll analyze this way directly from a database, which is how most real-world datasets actually originate.
