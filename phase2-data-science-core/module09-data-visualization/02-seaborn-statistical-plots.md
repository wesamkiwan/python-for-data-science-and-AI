# Module 09b: Seaborn — Statistical Visualization

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [01-matplotlib-fundamentals.md](01-matplotlib-fundamentals.md)

## 🎯 Learning Objectives
- [ ] Explain how Seaborn relates to Matplotlib and Pandas DataFrames
- [ ] Create distribution plots (`histplot`) and box plots
- [ ] Create a correlation heatmap
- [ ] Create a scatter plot with a categorical `hue`, and a pairplot for multi-variable exploration

---

## Module Goal

Meet **Seaborn**, a statistical visualization library built directly on top of Matplotlib, designed to work naturally with Pandas DataFrames and produce polished, publication-quality statistical charts with far less code than raw Matplotlib requires.

## Why This Matters on the Job

Seaborn is where data visualization and data analysis truly merge — instead of manually extracting arrays to plot (as in the Matplotlib lesson), you hand Seaborn a DataFrame and column names directly, and it handles grouping, coloring, and statistical summaries for you. Box plots and correlation heatmaps in particular are daily tools during **EDA (Exploratory Data Analysis)** — Module 10's entire focus — for spotting outliers, relationships, and patterns before any modeling begins.

---

## Installing Seaborn

```bash
pip install seaborn
```

```python
import seaborn as sns   # 'sns' is the universal, expected alias
```

💡 **Tip:** Seaborn functions accept a `data=` DataFrame plus column *names* as strings (`x="department"`, `y="salary"`) — a very different, more convenient calling style than Matplotlib's raw-array approach from the last lesson. Underneath, Seaborn is still drawing onto a Matplotlib Figure/Axes, so everything from the last lesson (`fig, ax = plt.subplots()`, `.set_title()`, `fig.savefig()`) still applies — just pass `ax=ax` to tell Seaborn which Axes to draw on.

## Sample Data for This Lesson

```python
import pandas as pd
import numpy as np

np.random.seed(42)
df = pd.DataFrame({
    "department": np.random.choice(["Engineering", "Sales", "Marketing"], 200),
    "salary": np.concatenate([
        np.random.normal(95000, 15000, 70),
        np.random.normal(75000, 12000, 70),
        np.random.normal(65000, 10000, 60)
    ]),
    "age": np.random.randint(22, 65, 200),
    "satisfaction": np.random.randint(1, 6, 200)
})
```

## Distribution Plot: `histplot`

```python
import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
sns.histplot(data=df, x="salary", kde=True, ax=ax)
ax.set_title("Salary Distribution")
plt.show()
```

**How it works:** `kde=True` overlays a smooth **KDE (Kernel Density Estimate)** curve on top of the histogram bars — a smoothed estimate of the underlying distribution's shape, useful for seeing overall skew/symmetry beyond what individual bin heights show.

🎯 **On the job:** This is usually the very first chart you'd make on any new numeric column — "what does this data's distribution actually look like?" — before computing summary statistics or deciding on an outlier-detection strategy (Module 08).

## Box Plot: Comparing Distributions Across Categories

```python
fig, ax = plt.subplots()
sns.boxplot(data=df, x="department", y="salary", ax=ax)
ax.set_title("Salary Distribution by Department")
plt.show()
```

**How it works:** A box plot summarizes a distribution in five numbers: the minimum (excluding outliers), Q1, median, Q3, and maximum (excluding outliers) — drawn as a box (Q1 to Q3, with a line at the median) with "whiskers" extending to the min/max. Points beyond the whiskers are plotted individually as **outliers** — using exactly the same `1.5 × IQR` rule from Module 08c. `x="department"` splits the plot into one box per department automatically.

🎯 **On the job:** Box plots are the fastest way to visually compare a numeric variable's spread *and* spot outliers *and* compare across categories, all in a single chart — a huge amount of information in a compact form, and one of the most common charts in any EDA report.

## Scatter Plot with `hue`: Adding a Categorical Dimension

```python
fig, ax = plt.subplots()
sns.scatterplot(data=df, x="age", y="salary", hue="department", ax=ax)
ax.set_title("Age vs. Salary, by Department")
plt.show()
```

**How it works:** `hue="department"` automatically colors each point by its department value and adds a legend — turning a 2-variable scatter plot (Matplotlib's version, from the last lesson) into a 3-variable one, without any manual color-mapping code.

## Bar Plot: Category Comparison with Automatic Aggregation

```python
fig, ax = plt.subplots()
sns.barplot(data=df, x="department", y="salary", ax=ax)
ax.set_title("Average Salary by Department")
plt.show()
```

**How it works:** Unlike Matplotlib's `ax.bar()` (which plots values you've already computed), Seaborn's `barplot` automatically aggregates — by default, it plots the **mean** of `y` for each category in `x`, with error bars showing a confidence interval. This is a meaningfully more convenient starting point than Matplotlib's bar chart whenever your data isn't already pre-aggregated.

## Correlation Heatmap

```python
corr = df[["salary", "age", "satisfaction"]].corr()
print(corr)

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Matrix")
plt.show()
```

**How it works:** `.corr()` (a DataFrame method) computes the pairwise **correlation coefficient** between every pair of numeric columns — a number from -1 (perfectly inverse relationship) to +1 (perfectly matching relationship), with 0 meaning no linear relationship. `sns.heatmap(..., annot=True)` visualizes that matrix as a color-coded grid with the actual numbers printed in each cell — `cmap="coolwarm"` colors negative correlations cool (blue) and positive ones warm (red), making patterns jump out visually.

🎯 **On the job:** A correlation heatmap is one of the very first charts run on any new dataset with several numeric columns — it immediately flags which variables move together, which is critical context before feature selection in Module 13.

## Pairplot: Every Variable Against Every Other, at Once

```python
g = sns.pairplot(df[["salary", "age", "satisfaction"]])
g.savefig("pairplot.png")
```

**How it works:** `pairplot` creates a grid of scatter plots for every pair of numeric columns, with histograms along the diagonal — an extremely fast way to eyeball every pairwise relationship in a dataset at once, without writing a separate plot for each combination.

⚠️ **Warning:** `pairplot` gets slow and visually cluttered past roughly 5-6 columns (since the number of subplots grows quadratically) — for a wide dataset, select just the columns you care most about first (`df[["col1", "col2", "col3"]]`, as shown above), rather than passing the entire DataFrame.

---

## Hands-On Exercise

**Task:** Write `seaborn_practice.py` using this DataFrame:
```python
import pandas as pd
import numpy as np

np.random.seed(1)
students = pd.DataFrame({
    "study_hours": np.random.uniform(0, 10, 100),
    "sleep_hours": np.random.uniform(4, 9, 100),
    "exam_score": np.random.normal(70, 15, 100),
    "major": np.random.choice(["Math", "History", "Biology"], 100)
})
```
1. Create a `histplot` of `exam_score` with a KDE curve overlaid.
2. Create a `boxplot` comparing `exam_score` across `major`.
3. Create a `scatterplot` of `study_hours` vs. `exam_score`, colored by `major` (`hue`).
4. Compute and print the correlation matrix for `study_hours`, `sleep_hours`, and `exam_score`, then visualize it as a heatmap.
5. Save all four charts as separate `.png` files.

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

np.random.seed(1)
students = pd.DataFrame({
    "study_hours": np.random.uniform(0, 10, 100),
    "sleep_hours": np.random.uniform(4, 9, 100),
    "exam_score": np.random.normal(70, 15, 100),
    "major": np.random.choice(["Math", "History", "Biology"], 100)
})

fig, ax = plt.subplots()
sns.histplot(data=students, x="exam_score", kde=True, ax=ax)
ax.set_title("Exam Score Distribution")
fig.savefig("exam_score_dist.png")
plt.close(fig)

fig, ax = plt.subplots()
sns.boxplot(data=students, x="major", y="exam_score", ax=ax)
ax.set_title("Exam Score by Major")
fig.savefig("exam_score_by_major.png")
plt.close(fig)

fig, ax = plt.subplots()
sns.scatterplot(data=students, x="study_hours", y="exam_score", hue="major", ax=ax)
ax.set_title("Study Hours vs. Exam Score")
fig.savefig("study_vs_score.png")
plt.close(fig)

corr = students[["study_hours", "sleep_hours", "exam_score"]].corr()
print(corr)

fig, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)
ax.set_title("Correlation Matrix")
fig.savefig("correlation_heatmap.png")
plt.close(fig)
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Manually pre-aggregating data before `sns.barplot()` | Pass the raw data — Seaborn aggregates (mean, by default) for you |
| Running `pairplot` on a DataFrame with many columns | Select only the columns you care about first |
| Forgetting `ax=ax` when combining Seaborn with subplots | Always pass it if you need multiple Seaborn charts in one figure |
| Reading correlation as causation | A high correlation shows two variables move together, not that one causes the other |
| Skipping `.corr()` before building a heatmap | `.corr()` on the numeric columns is what produces the matrix `heatmap()` visualizes |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Understand Seaborn's relationship to Matplotlib and Pandas
- [ ] Can create a `histplot` with a KDE overlay
- [ ] Can create a `boxplot` to compare distributions across categories
- [ ] Can create a `scatterplot` with `hue`, a correlation heatmap, and a pairplot
- [ ] Completed the `seaborn_practice.py` exercise

**Next:** Continue to [`03-plotly-interactive-charts.md`](03-plotly-interactive-charts.md)
