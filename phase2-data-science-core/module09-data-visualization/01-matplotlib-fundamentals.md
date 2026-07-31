# Module 09a: Matplotlib Fundamentals

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [Module 08 — Data Cleaning & Wrangling](../module08-data-cleaning/03-string-cleaning-and-outliers.md)

## 🎯 Learning Objectives
- [ ] Explain the Figure/Axes model Matplotlib is built on
- [ ] Create line, bar, scatter, and histogram plots
- [ ] Add titles, axis labels, and legends
- [ ] Create multiple plots in one figure with subplots
- [ ] Save a plot to a file

---

## Module Goal

Meet **Matplotlib**, the foundational Python plotting library that nearly every other visualization tool (including Seaborn and Pandas' own `.plot()` method) is built on top of. You'll learn its core mental model and the handful of chart types you'll reach for constantly.

## Why This Matters on the Job

A number in a table rarely convinces anyone of anything — a chart usually does. Every data scientist needs to visualize distributions, trends, and comparisons daily, both to understand data themselves during exploration and to communicate findings to non-technical stakeholders. Matplotlib is the lowest-level, most customizable tool for this, and understanding its Figure/Axes model makes every higher-level tool (Seaborn in the next lesson, Plotly after that) click faster, since they all speak the same underlying vocabulary.

---

## Installing Matplotlib

```bash
pip install matplotlib
```

```python
import matplotlib.pyplot as plt   # 'plt' is the universal, expected alias
```

## The Figure/Axes Model

Matplotlib organizes every plot around two objects:
- A **Figure** is the entire window/canvas — the overall container.
- An **Axes** is a single plot *within* that figure (confusingly, not the same as "axis" — one Figure can contain multiple Axes, i.e., multiple subplots).

```python
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)
y = np.sin(x)

fig, ax = plt.subplots()   # creates ONE Figure containing ONE Axes
ax.plot(x, y)
ax.set_title("Sine Wave")
ax.set_xlabel("x")
ax.set_ylabel("sin(x)")

plt.show()   # display the plot (in a script/terminal); in Jupyter, often not even needed
```

**How it works:** `plt.subplots()` (even with no arguments) is the standard, recommended way to start any plot — it returns both the Figure (`fig`) and an Axes (`ax`) in one call, ready to draw on. Everything you draw — the line, the title, the labels — is a method called on `ax`, not on `plt` directly.

💡 **Tip:** You'll often see older tutorials/code use `plt.plot(x, y)` directly, skipping `fig, ax = plt.subplots()` entirely — this "pyplot" shortcut style still works for simple, single plots, but the explicit `fig, ax` style (called the "object-oriented" style) scales much better once you need subplots or fine-grained control, and is what this course uses throughout. ✅ **Best Practice:** default to `fig, ax = plt.subplots()`, even for a single simple plot — it builds the habit that pays off the moment you need anything more complex.

## Core Chart Types

### Line Plot — Trends Over a Continuous Variable

```python
fig, ax = plt.subplots()
ax.plot(x, y, label="sin(x)")
ax.plot(x, np.cos(x), label="cos(x)")   # a second line on the SAME axes
ax.set_title("Trigonometric Functions")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.legend()          # shows the label for each line, based on the label= passed to .plot()
plt.show()
```

🎯 **On the job:** Line plots are the default choice for anything measured *over time* — stock prices, daily active users, temperature readings.

### Bar Chart — Comparing Categories

```python
fig, ax = plt.subplots()
categories = ["Product A", "Product B", "Product C", "Product D"]
sales = [23000, 45000, 12000, 36000]

ax.bar(categories, sales)
ax.set_title("Sales by Product")
ax.set_ylabel("Sales ($)")
plt.show()
```

🎯 **On the job:** Bar charts are the default choice for comparing a metric *across discrete categories* — sales by product, headcount by department.

### Scatter Plot — Relationship Between Two Numeric Variables

```python
fig, ax = plt.subplots()
hours_studied = np.random.uniform(0, 10, 50)
exam_score = hours_studied * 8 + np.random.normal(0, 10, 50)

ax.scatter(hours_studied, exam_score)
ax.set_title("Hours Studied vs. Exam Score")
ax.set_xlabel("Hours Studied")
ax.set_ylabel("Exam Score")
plt.show()
```

🎯 **On the job:** Scatter plots are the go-to first check for a relationship (correlation) between two numeric variables — the very first thing you'd plot before running a correlation calculation or fitting a regression model (Module 12).

### Histogram — Distribution of a Single Numeric Variable

```python
fig, ax = plt.subplots()
data = np.random.normal(loc=70, scale=10, size=1000)   # simulated exam scores

ax.hist(data, bins=30)
ax.set_title("Distribution of Exam Scores")
ax.set_xlabel("Score")
ax.set_ylabel("Frequency")
plt.show()
```

**How it works:** `bins=30` divides the data's range into 30 equal-width buckets and counts how many values fall into each — this is the standard way to visualize a single numeric column's overall shape (is it symmetric? skewed? does it have multiple peaks?). This directly connects to Module 08's outlier detection — a histogram is often the fastest visual way to *spot* an outlier before ever running the IQR calculation.

## Subplots: Multiple Charts, One Figure

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4))   # 1 row, 2 columns of Axes

axes[0].plot(x, y)
axes[0].set_title("Sine")

axes[1].plot(x, np.cos(x))
axes[1].set_title("Cosine")

fig.suptitle("Trigonometric Functions Side by Side")
plt.show()
```

**How it works:** `plt.subplots(1, 2)` creates a Figure with a 1x2 grid of Axes, returned as an array (`axes`) you index into (`axes[0]`, `axes[1]`) just like a NumPy array (Module 06) — each behaves exactly like the single `ax` from before. `figsize=(width, height)` (in inches) controls the overall Figure size.

## Saving a Plot

```python
fig.savefig("my_chart.png", dpi=150, bbox_inches="tight")
```

**How it works:** `dpi=150` controls image resolution (higher = sharper, larger file); `bbox_inches="tight"` trims excess whitespace around the plot. This is how you'd export a chart for a report, presentation, or README rather than just viewing it interactively.

✅ **Best Practice:** Always add a title and axis labels — an unlabeled chart forces the viewer to guess what they're looking at, which undermines the entire point of visualizing data in the first place.

---

## Hands-On Exercise

**Task:** Write `matplotlib_practice.py` that:
1. Creates a NumPy array of 12 monthly revenue figures (any reasonable numbers).
2. Creates a bar chart of revenue by month (label months 1-12 on the x-axis), with a title and y-axis label.
3. Creates a separate line plot of the same data, to compare how the same data looks as a trend vs. a comparison.
4. Combines both into one figure with two subplots side by side (`1, 2` layout), each with its own title.
5. Saves the combined figure to `monthly_revenue.png`.

<details>
<summary>✅ Click to see the solution</summary>

```python
import matplotlib.pyplot as plt
import numpy as np

months = np.arange(1, 13)
revenue = np.array([12000, 15000, 11000, 18000, 21000, 19500,
                     23000, 22000, 20500, 24000, 26000, 30000])

fig, axes = plt.subplots(1, 2, figsize=(12, 4))

axes[0].bar(months, revenue)
axes[0].set_title("Monthly Revenue (Bar)")
axes[0].set_xlabel("Month")
axes[0].set_ylabel("Revenue ($)")

axes[1].plot(months, revenue, marker="o")
axes[1].set_title("Monthly Revenue (Trend)")
axes[1].set_xlabel("Month")
axes[1].set_ylabel("Revenue ($)")

fig.suptitle("Monthly Revenue — Bar vs. Line")
fig.savefig("monthly_revenue.png", dpi=150, bbox_inches="tight")
```

**Expected outcome:** A saved `monthly_revenue.png` showing two side-by-side charts of the same 12 monthly values — a bar chart (easy to compare individual months) and a line chart (easy to see the overall upward trend), each properly labeled.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Skipping titles/axis labels | Always label — an unlabeled chart forces guesswork |
| Confusing Figure with Axes | Figure = the whole canvas; Axes = one plot within it (can have several) |
| Choosing the wrong chart type (e.g., a line plot for unordered categories) | Line = trend over a continuous variable; bar = compare categories; scatter = relationship between two numeric variables; histogram = distribution of one variable |
| Forgetting `label=` and `.legend()` when plotting multiple series | Always add both when more than one line/series shares a plot |
| Not reusing `fig, ax = plt.subplots()` for anything beyond the simplest plot | Default to this pattern from the start — it scales to subplots without rework |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand the Figure/Axes model
- [ ] Can create line, bar, scatter, and histogram plots
- [ ] Can add titles, axis labels, and legends
- [ ] Can create subplots and save a figure to a file
- [ ] Completed the `matplotlib_practice.py` exercise

**Next:** Continue to [`02-seaborn-statistical-plots.md`](02-seaborn-statistical-plots.md)
