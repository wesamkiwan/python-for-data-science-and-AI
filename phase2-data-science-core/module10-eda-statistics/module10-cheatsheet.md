# 📋 Module 10 Cheat Sheet: EDA & Statistics

Fast reference for descriptive stats, distributions, correlation, and hypothesis testing.

## Descriptive Statistics
```python
series.mean()      series.median()      series.mode()
series.var()          series.std()
series.skew()            # near 0 = symmetric; >0 right-skewed; <0 left-skewed
```
✅ On skewed/outlier-prone data, prefer the **median** over the mean as the "typical value."

## Distributions
| Skewness | Meaning |
|---|---|
| ≈ 0 | Roughly symmetric (normal-like) |
| > 0 | Right-skewed (long tail of high values — e.g. income) |
| < 0 | Left-skewed (long tail of low values) |

## Correlation
```python
from scipy import stats
corr, p_value = stats.pearsonr(x, y)     # -1 to +1, plus significance
df[["a","b","c"]].corr()                     # full pairwise matrix (Module 09's heatmap input)
```
⚠️ Correlation ≠ causation — always consider confounding variables.

## Hypothesis Testing Framework
1. **H₀ (null):** no real difference/effect.
2. **H₁ (alternative):** there IS a difference/effect.
3. **p-value:** P(data this extreme | H₀ is true).
4. **α (typically 0.05):** if p-value < α → reject H₀ (statistically significant).

⚠️ p-value is NOT "probability H₀ is true." It's "probability of this data, assuming H₀."

## T-Test (compare two group means)
```python
from scipy import stats
t_stat, p_value = stats.ttest_ind(group_a, group_b)
significant = p_value < 0.05
```

## Confidence Interval (for a mean)
```python
mean = data.mean()
sem = stats.sem(data)                                    # standard error of the mean
ci = stats.t.interval(0.95, len(data) - 1, loc=mean, scale=sem)
```
💡 A 95% CI means: repeating this sampling many times, ~95% of such intervals would contain the true mean — not "95% chance this specific interval contains it."

## Chi-Square Test (compare categorical variables)
```python
chi2, p_value, dof, expected = stats.chi2_contingency(observed_counts_table)
```

## Which Test to Use

| Comparing | Test |
|---|---|
| Means of two groups (numeric outcome) | T-test |
| Two categorical variables (counts) | Chi-square |
| Linear relationship, two numeric variables | Pearson correlation |

## The Full EDA Workflow — do this every time
1. **Inspect** — `.head()`, `.info()`, `.shape`, `.isna().sum()` (Module 07).
2. **Clean** — handle missing data, duplicates, dtypes, outliers (Module 08).
3. **Describe** — mean/median/std/skew on key numeric columns (Module 10a).
4. **Visualize** — histograms, box plots, correlation heatmap (Module 09).
5. **Test** — formalize any apparent pattern with a t-test/chi-square/correlation p-value (Module 10b).
6. **Conclude** — write findings that clearly separate description from statistical inference.

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Mean and median very different | Skewed data / outliers present | Report both; consider median as the "typical" value |
| "Significant" result but tiny practical difference | Large sample size inflating significance | Check effect size, not just p-value |
| Strong correlation assumed to mean causation | Confounding variable not considered | Ask "could a third factor explain both?" |
| Misreading a 95% CI as "95% chance true value is here" | CI describes procedure reliability, not this one interval | Reframe: repeated sampling would capture the true value ~95% of the time |

