# Module 10b: Correlation & Hypothesis Testing

🟡 **Difficulty:** Intermediate | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [01-descriptive-statistics-and-distributions.md](01-descriptive-statistics-and-distributions.md)

## 🎯 Learning Objectives
- [ ] Interpret a correlation coefficient and explain why correlation isn't causation
- [ ] Explain the logic of hypothesis testing and p-values
- [ ] Run a t-test to compare two groups
- [ ] Compute and interpret a confidence interval

---

## Module Goal

Move from *describing* data (Module 10a) to *making inferences* from it — the core purpose of **inferential statistics**: using a sample of data to draw conclusions (with a stated degree of confidence) about a larger question. This module covers correlation, hypothesis testing, and confidence intervals — the statistical vocabulary behind almost every "is this difference real?" question.

## Why This Matters on the Job

"Is our new website design actually better, or did it just get lucky with this batch of visitors?" "Is there really a relationship between marketing spend and sales, or is it a coincidence?" These are hypothesis-testing questions, and being able to answer them rigorously — with a p-value and a clear statement of confidence — is what separates a data-driven decision from a guess dressed up with a chart.

---

## Correlation: Measuring Linear Relationships

You computed correlation via `.corr()` and visualized it as a heatmap in Module 09. Here's the deeper statistical picture:

```python
import numpy as np
from scipy import stats

np.random.seed(1)
x = np.random.normal(0, 1, 100)
y = x * 2 + np.random.normal(0, 1, 100)   # y is built directly from x, plus some noise

correlation, p_value = stats.pearsonr(x, y)
print(f"Correlation: {correlation:.4f}")
print(f"P-value: {p_value:.6f}")
```
```
Correlation: 0.8961
P-value: 0.000000
```

**How it works:** `stats.pearsonr()` returns both the correlation coefficient (from -1 to +1, same as `.corr()` in Module 09) *and* a p-value testing whether that correlation is statistically significant, or could plausibly have arisen from random chance alone.

## ⚠️ Correlation Is Not Causation

This is one of the most important — and most frequently violated — principles in all of statistics.

💡 **Classic example:** Ice cream sales and drowning deaths are strongly correlated — both rise in summer. Buying ice cream doesn't cause drowning; a third factor (hot weather → more swimming AND more ice cream) drives both. This is called a **confounding variable**.

✅ **Best Practice:** When you find a strong correlation, always ask: "Could a third factor explain both?" Only carefully designed experiments (with random assignment to groups — an **A/B test**, for example) can establish causation with real confidence; observational correlation alone cannot.

🎯 **On the job:** Interviewers frequently present a correlated pair of variables specifically to test whether you'll correctly identify a plausible confounder rather than jumping to "X causes Y."

## Hypothesis Testing: The Core Logic

**Hypothesis testing** is a formal framework for asking "is this observed difference/relationship real, or could it just be random noise?"

1. **Null hypothesis (H₀):** the "boring," skeptical default — usually "there's no real difference/effect."
2. **Alternative hypothesis (H₁):** what you're actually trying to find evidence for — "there IS a difference/effect."
3. **P-value:** the probability of seeing data this extreme (or more extreme) *if the null hypothesis were actually true*.
4. **Significance level (α, commonly 0.05):** your threshold for "small enough to doubt the null hypothesis." If `p-value < α`, you **reject the null hypothesis** — the effect is considered statistically significant.

⚠️ **Warning:** A p-value is *not* "the probability the null hypothesis is true," and it's *not* "the probability your finding is a fluke" — it's specifically "how likely is data this extreme, assuming the null hypothesis." This subtle distinction is one of the most commonly misstated facts in all of statistics, and a favorite interview gotcha.

## The T-Test: Comparing Two Groups

A **t-test** checks whether two groups' means are significantly different from each other.

```python
import numpy as np
from scipy import stats

np.random.seed(42)
group_a_scores = np.random.normal(75, 10, 30)   # control group
group_b_scores = np.random.normal(80, 10, 30)      # group that used a new study method

t_stat, p_value = stats.ttest_ind(group_a_scores, group_b_scores)
print(f"t-statistic: {t_stat:.4f}")
print(f"p-value: {p_value:.4f}")

if p_value < 0.05:
    print("Statistically significant difference between the groups (reject H0).")
else:
    print("No statistically significant difference detected (fail to reject H0).")
```
```
t-statistic: -2.3981
p-value: 0.0197
Statistically significant difference between the groups (reject H0).
```

**How it works:** `stats.ttest_ind()` (independent samples t-test) compares the means of two independent groups, accounting for their variability and sample sizes, and returns a p-value. Here, `p-value < 0.05` means we'd reject H₀ (that the groups have the same true mean) — the observed 5-point difference is unlikely to be pure chance.

⚠️ **Warning:** "Statistically significant" does *not* automatically mean "practically important" — with a large enough sample size, even a tiny, meaningless difference can become statistically significant. Always consider the **effect size** (how large is the actual difference?) alongside the p-value, not the p-value alone.

## Confidence Intervals

A **confidence interval** gives a range of plausible values for a true population statistic, based on your sample — rather than a single point estimate.

```python
import numpy as np
from scipy import stats

np.random.seed(7)
sample = np.random.normal(100, 15, 50)

mean = np.mean(sample)
standard_error = stats.sem(sample)   # standard error of the mean

confidence_interval = stats.t.interval(0.95, len(sample) - 1, loc=mean, scale=standard_error)
print(f"Sample mean: {mean:.2f}")
print(f"95% confidence interval: ({confidence_interval[0]:.2f}, {confidence_interval[1]:.2f})")
```
```
Sample mean: 99.52
95% confidence interval: (95.70, 103.34)
```

**How it works:** A "95% confidence interval" means: if you repeated this sampling process many times and computed a new interval each time, about 95% of those intervals would contain the true population mean. It's a range that quantifies *uncertainty* around your point estimate — a narrower interval (from a larger sample) reflects more confidence in the estimate.

⚠️ **Warning:** A common misinterpretation is "there's a 95% chance the true mean is in this specific interval" — technically, the true mean either is or isn't in any given interval (it's not random); the 95% describes the *procedure's* long-run reliability, not this one interval specifically. This distinction is subtle but frequently tested.

## Chi-Square Test: Comparing Categorical Groups

For categorical (not numeric) data — e.g., "is there a relationship between department and whether someone left the company?" — use a **chi-square test**:

```python
import pandas as pd
from scipy import stats

observed = pd.DataFrame({"Passed": [45, 30], "Failed": [15, 20]}, index=["Group A", "Group B"])

chi2, p_value, dof, expected = stats.chi2_contingency(observed)
print(f"Chi-square statistic: {chi2:.4f}")
print(f"P-value: {p_value:.4f}")
```
```
Chi-square statistic: 2.1794
P-value: 0.1399
```

**How it works:** `chi2_contingency()` compares the *observed* counts in each category combination against what you'd *expect* if the two categorical variables were completely unrelated. Here, `p-value = 0.14 > 0.05`, so there isn't strong evidence of a real relationship between group and pass/fail rate in this particular sample.

| Test | Use when comparing... |
|---|---|
| T-test | Means of two groups (numeric outcome) |
| Chi-square | Two categorical variables (counts/proportions) |
| Pearson correlation | Linear relationship between two numeric variables |

---

## Hands-On Exercise

**Task:** Write `hypothesis_testing_practice.py` that:
1. Simulates two groups of 40 customers each — `control_group` spending amounts and `promo_group` spending amounts (use `np.random.normal()` with different means, e.g., 50 and 58, same std of 12).
2. Runs a t-test comparing the two groups, printing the t-statistic and p-value.
3. Prints a conclusion sentence: is the difference statistically significant at α = 0.05?
4. Computes and prints a 95% confidence interval for the `promo_group`'s mean spending.
5. Computes the Pearson correlation between `control_group` and an unrelated random array of the same length, and confirms (by checking the p-value) that it's *not* statistically significant — illustrating that random data correctly shows no real relationship.

<details>
<summary>✅ Click to see the solution</summary>

```python
import numpy as np
from scipy import stats

np.random.seed(1)
control_group = np.random.normal(50, 12, 40)
promo_group = np.random.normal(58, 12, 40)

t_stat, p_value = stats.ttest_ind(control_group, promo_group)
print(f"t-statistic: {t_stat:.4f}, p-value: {p_value:.4f}")

if p_value < 0.05:
    print("The difference in spending is statistically significant (reject H0).")
else:
    print("No statistically significant difference detected (fail to reject H0).")

mean_promo = np.mean(promo_group)
sem_promo = stats.sem(promo_group)
ci = stats.t.interval(0.95, len(promo_group) - 1, loc=mean_promo, scale=sem_promo)
print(f"Promo group mean: {mean_promo:.2f}, 95% CI: ({ci[0]:.2f}, {ci[1]:.2f})")

unrelated = np.random.normal(0, 1, 40)
corr, corr_p = stats.pearsonr(control_group, unrelated)
print(f"Correlation with unrelated data: {corr:.4f}, p-value: {corr_p:.4f}")
print("Not significant" if corr_p >= 0.05 else "Unexpectedly significant")
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Assuming correlation implies causation | Always consider confounding variables; only controlled experiments establish causation |
| Misreading a p-value as "probability the null hypothesis is true" | It's "probability of data this extreme, IF the null hypothesis is true" |
| Treating "statistically significant" as automatically "practically important" | Also consider effect size, not just the p-value |
| Misinterpreting a confidence interval as "95% chance the true value is in this range" | It describes the reliability of the *procedure* across repeated sampling |
| Using a t-test on categorical data | Use chi-square for categorical comparisons instead |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Understand correlation and can explain why it isn't causation
- [ ] Understand the null/alternative hypothesis and p-value framework
- [ ] Can run and interpret a t-test comparing two groups
- [ ] Can compute and correctly interpret a confidence interval
- [ ] Know when to use a t-test vs. chi-square vs. correlation
- [ ] Completed the `hypothesis_testing_practice.py` exercise

**Next:** Continue to [`03-full-eda-workflow.md`](03-full-eda-workflow.md)
