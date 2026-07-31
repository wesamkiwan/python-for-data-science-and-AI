# 🎤 Module 09 Interview Prep: Data Visualization

## Conceptual Questions

### 🟢 Beginner

**Q: What's the difference between a Matplotlib Figure and an Axes?**
> A: A Figure is the entire canvas/window that contains everything. An Axes is a single plot within that figure — one Figure can contain multiple Axes (subplots). Almost everything you draw (lines, bars, titles, labels) is a method call on a specific Axes object, not on the Figure directly.

**Q: When would you use a line chart instead of a bar chart?**
> A: A line chart is best for showing a trend over a continuous variable, most commonly time (e.g., revenue by month) — the connecting line implies a meaningful order and continuity between points. A bar chart is best for comparing a metric across discrete, unordered (or at least non-continuous) categories, like sales by product — there's no meaningful "in-between" value connecting one bar to the next.

**Q: What does a histogram show that a simple list of numbers doesn't?**
> A: A histogram groups numeric values into bins and shows how many values fall in each bin, revealing the overall *shape* of the distribution — whether it's symmetric, skewed, has multiple peaks, or has outliers — which is very difficult to see just by scanning a column of raw numbers.

### 🟡 Intermediate

**Q: How does a Seaborn box plot relate to the IQR outlier-detection method from Module 08?**
> A: A box plot's box spans from Q1 to Q3 (the interquartile range itself), with a line at the median, and its "whiskers" extend to the furthest points still within `1.5 × IQR` of the box — exactly the same threshold used in Module 08's IQR outlier method. Any points beyond the whiskers are plotted individually and are, by this same definition, statistical outliers — so a box plot is really the *visual* version of the IQR calculation, letting you spot outliers and compare distributions across categories in one glance.

**Q: Why might you choose Plotly over Matplotlib/Seaborn for a specific chart?**
> A: Plotly adds interactivity — hovering to see exact values, zooming into a region, toggling categories on/off via the legend — with very little extra code, which is valuable when the audience will want to explore the data themselves (a stakeholder dashboard, a shared notebook) or when a chart is dense enough that hover detail adds real clarity. For static reports, papers, or my own quick exploratory checks, Matplotlib/Seaborn are simpler and don't need a browser or extra export step.

**Q: What does a correlation heatmap tell you, and what's an important limitation to keep in mind when interpreting it?**
> A: It shows the pairwise correlation coefficient between every numeric column in a dataset, color-coded so strong positive/negative relationships are visually obvious at a glance — extremely useful early in EDA (Module 10) for spotting which variables move together. The key limitation: correlation measures a *linear* relationship's strength and direction, but doesn't imply causation, and can miss strong *non-linear* relationships entirely (two variables can have a clear non-linear pattern and still show a correlation near zero).

## Practical/Coding Questions

**Q: Given a DataFrame `df` with columns `department` and `salary`, write code to create a box plot comparing salary distributions across departments, with a clear title.**
```python
import seaborn as sns
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
sns.boxplot(data=df, x="department", y="salary", ax=ax)
ax.set_title("Salary Distribution by Department")
plt.show()
```
> Explanation: Seaborn's DataFrame-native calling style (`data=df, x="department", y="salary"`) handles the grouping and box-per-category logic automatically — no manual splitting of the data by department is needed.

**Q: Write code to create an interactive scatter plot of `hours_studied` vs. `exam_score`, colored by `passed` (a boolean/categorical column), that a user could open and explore in a browser.**
```python
import plotly.express as px

fig = px.scatter(df, x="hours_studied", y="exam_score", color="passed", title="Study Hours vs. Exam Score")
fig.write_html("study_scores.html")
```
> Explanation: `color="passed"` automatically splits points into colored groups with a legend; `write_html()` produces a fully self-contained interactive file that opens and works in any browser, with no server or extra dependency required.

## Scenario Questions

**Q: A stakeholder asks for "a chart showing how our top 5 products are trending over the last 12 months, that I can explore myself." Which library would you reach for, and what chart type?**
> A: I'd use Plotly for the interactivity requirement ("explore myself" strongly implies hover/zoom/filter capability), and a line chart, since the request is fundamentally about a trend over a continuous time variable — `px.line(df, x="month", y="sales", color="product")` gives one colored line per product, with hover tooltips for exact monthly values and legend-click filtering built in for free.

**Q: You're doing initial exploration on a dataset with 15 numeric columns. How would you efficiently get a first look at relationships between them, given that a full pairplot would be unwieldy?**
> A: I'd start with a correlation heatmap (`df.corr()` + `sns.heatmap(..., annot=True)`) across all 15 columns — it scales far better visually than a pairplot and immediately highlights the strongest relationships. From there, I'd narrow down to the 4-6 columns showing the most interesting correlations and *then* run a pairplot on just that subset, to see the actual shape of those specific relationships (a heatmap only shows linear correlation strength, not the relationship's actual shape).

## "Gotcha" Questions

**Q: Why might two variables have a correlation coefficient near zero, yet clearly be related when you look at a scatter plot of them?**
> A: The correlation coefficient (as computed by `.corr()`) specifically measures *linear* relationship strength. A strong *non-linear* relationship — for example, a U-shaped or cyclical pattern — can produce a correlation near zero even though the variables are clearly, visibly related on a scatter plot. This is exactly why visualizing data (not just computing summary statistics) is an essential complement to numerical analysis, never a replacement for it.

**Q: A colleague's Seaborn chart inside a `plt.subplots(1, 2)` grid keeps showing up as a separate, extra figure instead of appearing in the intended subplot slot. What's the likely bug?**
> A: They almost certainly forgot to pass `ax=ax` (or `ax=axes[i]`) to the Seaborn function call. Without it, Seaborn creates and draws on its own new Figure/Axes instead of the one already created by `plt.subplots()`, producing a stray extra figure rather than filling the intended subplot slot.

## Quick-Fire Rapid Review

- Q: Chart type for trend over time? → **line plot**
- Q: Chart type for comparing categories? → **bar chart**
- Q: Chart type for relationship between two numeric variables? → **scatter plot**
- Q: Chart type for distribution of one numeric variable? → **histogram**
- Q: What does a box plot's whiskers represent? → **the range within 1.5 × IQR of the box (Q1-Q3), same rule as Module 08's outlier detection**
- Q: Seaborn parameter that adds automatic color-grouping by category? → **`hue=`**
- Q: Plotly equivalent of Seaborn's `hue=`? → **`color=`**
- Q: Does correlation imply causation? → **No**
- Q: Method to export a Plotly chart as an interactive file? → **`fig.write_html()`**
