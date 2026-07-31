# 📋 Module 09 Cheat Sheet: Data Visualization

Fast reference for Matplotlib, Seaborn, and Plotly.

## Matplotlib — Figure/Axes Basics
```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()             # ALWAYS start here, even for one simple plot
fig, axes = plt.subplots(1, 2, figsize=(10, 4))     # grid of subplots -> axes[0], axes[1]

ax.plot(x, y, label="series")     # line
ax.bar(categories, values)          # bar
ax.scatter(x, y)                       # scatter
ax.hist(data, bins=30)                    # histogram

ax.set_title("Title")   ax.set_xlabel("X")   ax.set_ylabel("Y")   ax.legend()
fig.suptitle("Overall Figure Title")

fig.savefig("chart.png", dpi=150, bbox_inches="tight")
plt.show()
```

## Chart Type Decision Table

| Need to show | Use |
|---|---|
| Trend over time / continuous variable | Line plot |
| Compare a metric across categories | Bar chart |
| Relationship between 2 numeric variables | Scatter plot |
| Distribution / shape of 1 numeric variable | Histogram |
| Distribution + outliers, across categories | Box plot (Seaborn) |
| Every pairwise numeric relationship at once | Pairplot (Seaborn) |
| Correlation across many numeric columns | Heatmap (Seaborn) |
| Anything a stakeholder wants to explore interactively | Plotly |

## Seaborn — DataFrame-Native Statistical Plots
```python
import seaborn as sns

sns.histplot(data=df, x="col", kde=True, ax=ax)             # distribution + smoothed curve
sns.boxplot(data=df, x="category_col", y="numeric_col", ax=ax)  # spread + outliers per category
sns.scatterplot(data=df, x="col1", y="col2", hue="category_col", ax=ax)  # scatter, auto-colored
sns.barplot(data=df, x="category_col", y="numeric_col", ax=ax)     # auto-aggregates (mean by default)

corr = df[["a", "b", "c"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)          # correlation matrix, color-coded

sns.pairplot(df[["a", "b", "c"]])     # grid of every pairwise scatter + diagonal histograms
```
⚠️ Limit `pairplot` to the columns you care about — it gets slow/cluttered past ~5-6 columns.

## Plotly — Interactive Charts
```python
import plotly.express as px

fig = px.line(df, x="col1", y="col2", title="Title")
fig = px.bar(df, x="col1", y="col2", color="category_col", barmode="group", title="Title")
fig = px.scatter(df, x="col1", y="col2", color="category_col", hover_data=["col1", "col2"], title="Title")
fig = px.histogram(df, x="col", nbins=20, title="Title")

fig.show()                    # interactive display
fig.write_html("chart.html")     # self-contained interactive file
fig.write_image("chart.png")        # static image (requires: pip install kaleido)
```

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Chart looks unlabeled/confusing | Missing title/axis labels | Always call `.set_title()`/`.set_xlabel()`/`.set_ylabel()` (or `title=` in Plotly) |
| Multiple lines but no legend | Missing `label=` + `.legend()` | Add `label=` to each `.plot()` call, then `ax.legend()` |
| `pairplot` is extremely slow | Too many numeric columns passed | Select only the columns you need first: `df[["a","b","c"]]` |
| `fig.write_image()` fails | Missing `kaleido` package | `pip install kaleido`, or use `write_html()`/`fig.show()` instead |
| Seaborn chart not appearing in a subplot grid | Forgot `ax=ax` | Always pass `ax=ax` when combining Seaborn with `plt.subplots()` |

## The "New Chart" Workflow — do this every time
1. Pick the chart type from the decision table above based on what you're actually showing.
2. Static + simple/exploratory → Matplotlib. Statistical/DataFrame-native → Seaborn. Needs interactivity → Plotly.
3. Always add a title and axis labels before considering a chart "done."
4. Save it (`fig.savefig()` / `fig.write_html()`) if it needs to be shared or reused.
