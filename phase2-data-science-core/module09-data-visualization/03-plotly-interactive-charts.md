# Module 09c: Plotly — Interactive Charts

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [02-seaborn-statistical-plots.md](02-seaborn-statistical-plots.md)

## 🎯 Learning Objectives
- [ ] Explain when interactive charts (Plotly) are worth the extra step over static ones (Matplotlib/Seaborn)
- [ ] Create line, bar, scatter, and histogram charts with `plotly.express`
- [ ] Add hover data and color grouping to a Plotly chart
- [ ] Export a Plotly chart to an HTML file

---

## Module Goal

Meet **Plotly**, a library for building **interactive** charts — ones a viewer can hover over, zoom into, and filter, directly in a browser or notebook, without writing any JavaScript. You'll learn `plotly.express`, its fast, high-level interface for building common chart types in one line, mirroring Seaborn's convenience but with interactivity built in.

## Why This Matters on the Job

Static charts (Matplotlib/Seaborn) are perfect for reports, papers, and quick exploration. But when you're sharing an analysis with a stakeholder who wants to explore the data themselves — hover to see exact values, zoom into a busy time range, toggle a category on/off — an interactive chart communicates far more, far faster. Plotly is also the charting engine behind many production dashboarding tools (like Dash), so this module is a direct stepping stone toward building interactive data apps later in your career.

---

## Installing Plotly

```bash
pip install plotly
```

```python
import plotly.express as px   # 'px' is the standard alias for the high-level interface
```

💡 **Tip:** `plotly.express` (what this lesson covers) is the fast, Seaborn-like interface for common charts. There's also a lower-level `plotly.graph_objects` interface for fully custom charts — similar to how Matplotlib's raw Figure/Axes underlies Seaborn's convenience functions. Start with `plotly.express`; it covers the vast majority of real needs.

## Line Chart

```python
import pandas as pd
import plotly.express as px

df = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
    "revenue": [12000, 15000, 11000, 18000, 21000, 19500]
})

fig = px.line(df, x="month", y="revenue", title="Monthly Revenue")
fig.show()   # opens an interactive chart in your browser or notebook
```

**How it works:** `px.line(df, x="col1", y="col2")` mirrors Seaborn's `data=`/column-name calling style exactly — pass the DataFrame and the column names as strings, no manual array extraction needed. `fig.show()` renders the chart; hovering over any point in the resulting chart displays its exact value automatically, with zero extra code.

## Bar Chart with Color Grouping

```python
df2 = pd.DataFrame({
    "month": ["Jan", "Feb", "Mar", "Jan", "Feb", "Mar"],
    "revenue": [12000, 15000, 11000, 9000, 13000, 14000],
    "region": ["East", "East", "East", "West", "West", "West"]
})

fig = px.bar(df2, x="month", y="revenue", color="region", title="Revenue by Region", barmode="group")
fig.show()
```

**How it works:** `color="region"` splits and colors the bars by that column automatically (exactly like Seaborn's `hue`), and `barmode="group"` places same-month bars for different regions side by side rather than stacked. In the interactive chart, clicking a region's name in the legend toggles it on/off — instantly filtering the chart with no extra code.

## Scatter Plot with Hover Data

```python
import numpy as np

np.random.seed(42)
employees = pd.DataFrame({
    "age": np.random.randint(22, 60, 100),
    "salary": np.random.normal(75000, 15000, 100),
    "department": np.random.choice(["Engineering", "Sales"], 100)
})

fig = px.scatter(
    employees, x="age", y="salary", color="department",
    hover_data=["age", "salary"], title="Age vs. Salary"
)
fig.show()
```

**How it works:** `hover_data=[...]` adds extra fields to the tooltip that appears when hovering over any point — beyond just the `x`/`y` values already shown by default. This kind of detail-on-demand is exactly what a static Matplotlib/Seaborn scatter plot can't offer without significant extra code.

## Histogram

```python
fig = px.histogram(employees, x="salary", nbins=20, title="Salary Distribution")
fig.show()
```

🎯 **On the job:** Every chart type from the Matplotlib/Seaborn lessons has a direct `plotly.express` equivalent (`px.line`, `px.bar`, `px.scatter`, `px.histogram`, `px.box`, and more) — once you know one library's grammar, switching to Plotly for interactivity is mostly a matter of translating the function name and argument style, not relearning visualization from scratch.

## Exporting a Plotly Chart

```python
fig.write_html("chart.html")     # a full, self-contained, interactive HTML file -- open it in any browser
fig.write_image("chart.png")       # a STATIC image (requires the `kaleido` package: pip install kaleido)
```

⚠️ **Warning:** `fig.write_image()` requires an extra dependency (`kaleido`) to render a static snapshot — if you only need to *view* the chart interactively (in a notebook, or by opening the saved `.html` file in a browser), `fig.show()` or `write_html()` work with no extra installation.

✅ **Best Practice:** Reach for Plotly specifically when interactivity adds real value — exploratory dashboards, sharing a chart with someone who'll want to zoom/filter themselves, or web apps. For static reports, papers, or a quick "what does this distribution look like" check during your own exploration, Matplotlib/Seaborn are simpler and usually sufficient — don't reach for Plotly by default just because it's fancier.

---

## Hands-On Exercise

**Task:** Write `plotly_practice.py` that:
1. Creates a DataFrame with at least 3 products, 4 quarters, and a `sales` figure for each product-quarter combination (12 rows total).
2. Creates an interactive line chart of `sales` over `quarter`, with one colored line per `product`.
3. Creates an interactive grouped bar chart of the same data.
4. Creates an interactive scatter plot of any two numeric columns from a dataset of your choice, colored by a categorical column, with at least 2 fields in `hover_data`.
5. Saves all three charts to separate `.html` files.

<details>
<summary>✅ Click to see the solution</summary>

```python
import pandas as pd
import numpy as np
import plotly.express as px

sales_data = pd.DataFrame({
    "product": ["Widget", "Gadget", "Gizmo"] * 4,
    "quarter": ["Q1", "Q1", "Q1", "Q2", "Q2", "Q2", "Q3", "Q3", "Q3", "Q4", "Q4", "Q4"],
    "sales": [5000, 7000, 3000, 5500, 7200, 3400, 6000, 7500, 3800, 6800, 8000, 4200]
})

fig1 = px.line(sales_data, x="quarter", y="sales", color="product", title="Quarterly Sales by Product")
fig1.write_html("sales_line.html")

fig2 = px.bar(sales_data, x="quarter", y="sales", color="product", barmode="group", title="Quarterly Sales (Grouped)")
fig2.write_html("sales_bar.html")

np.random.seed(7)
employees = pd.DataFrame({
    "years_experience": np.random.randint(0, 20, 60),
    "salary": np.random.normal(80000, 20000, 60),
    "department": np.random.choice(["Engineering", "Sales", "Marketing"], 60)
})

fig3 = px.scatter(
    employees, x="years_experience", y="salary", color="department",
    hover_data=["years_experience", "salary"], title="Experience vs. Salary"
)
fig3.write_html("employees_scatter.html")
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Using Plotly for every chart by default | Reach for it specifically when interactivity is valuable; Matplotlib/Seaborn are simpler for static needs |
| Calling `fig.write_image()` without `kaleido` installed | Install it (`pip install kaleido`) or use `write_html()`/`fig.show()` instead |
| Passing raw arrays instead of a DataFrame + column names | `plotly.express` is built around the `data=`/column-name style — lean into it |
| Overcrowding a chart with too many `hover_data` fields | Include only what's genuinely useful to inspect on hover |

---

## ✅ Module 09 Completion Checklist
- [ ] Understand when interactive (Plotly) beats static (Matplotlib/Seaborn) visualization, and vice versa
- [ ] Can create line, bar, scatter, and histogram charts with `plotly.express`
- [ ] Can add color grouping and hover data to a chart
- [ ] Can export a chart to HTML
- [ ] Completed the `plotly_practice.py` exercise
- [ ] Reviewed [`module09-cheatsheet.md`](module09-cheatsheet.md)
- [ ] Reviewed [`module09-interview.md`](module09-interview.md)
- [ ] Browsed [`module09-references.md`](module09-references.md)

**Next Step:** Module 10 — EDA & Statistics (`phase2-data-science-core/module10-eda-statistics/`)
