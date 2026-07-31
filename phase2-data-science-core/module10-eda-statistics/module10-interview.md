# 🎤 Module 10 Interview Prep: EDA & Statistics

## Conceptual Questions

### 🟢 Beginner

**Q: When is the median a better measure of "typical value" than the mean?**
> A: When the data contains outliers or is significantly skewed — a small number of extreme values can pull the mean far from where most of the data actually sits, while the median (the middle value) stays anchored close to the bulk of the data. Salary and home price data are classic examples: a few very high earners inflate the mean well above what's typical for most people, but the median remains representative.

**Q: What does standard deviation tell you that the mean alone doesn't?**
> A: The mean tells you a "typical" central value, but says nothing about how spread out the data is around that value. Standard deviation measures that spread — two datasets can share the exact same mean but have very different standard deviations, meaning one is tightly clustered and predictable while the other is widely scattered and variable.

**Q: Why is "correlation is not causation" such an important principle?**
> A: Two variables can be strongly correlated because one causes the other, because the relationship runs the other direction, or — very commonly — because a third, unmeasured **confounding variable** influences both. Ice cream sales and drowning deaths both rise in summer (driven by hot weather), not because one causes the other. Concluding causation from correlation alone, without a controlled experiment, is one of the most common analytical mistakes.

### 🟡 Intermediate

**Q: Explain, in plain terms, what a p-value actually represents.**
> A: A p-value is the probability of observing data at least as extreme as what you actually saw, *assuming the null hypothesis is true*. It is not the probability that the null hypothesis itself is true, and it's not the probability your result is a fluke — it specifically answers "how surprising is this data, if there's really no effect?" A small p-value means the observed data would be quite unlikely under the null hypothesis, giving grounds to reject it.

**Q: What's the difference between statistical significance and practical significance?**
> A: Statistical significance (a p-value below your threshold, e.g., 0.05) means an observed effect is unlikely to be pure chance, given your sample size and variability. Practical significance is about whether the effect is actually large enough to matter for a real decision. With a large enough sample, even a trivially small, practically meaningless difference can become statistically significant — so a p-value should always be considered alongside the actual effect size, not in isolation.

**Q: How do you correctly interpret a 95% confidence interval?**
> A: It means: if you repeated the same sampling and estimation procedure many times, approximately 95% of the resulting intervals would contain the true population value. It's a statement about the reliability of the *method* over repeated sampling — not a statement that there's a 95% probability the true value falls within this one specific interval you calculated (the true value either is or isn't in it; there's no probability involved for this single instance).

## Practical/Coding Questions

**Q: Write code to test whether two marketing campaigns produced significantly different average order values, and state the conclusion.**
```python
from scipy import stats

t_stat, p_value = stats.ttest_ind(campaign_a_orders, campaign_b_orders)
alpha = 0.05

if p_value < alpha:
    print(f"Significant difference (p={p_value:.4f}) -- reject H0.")
else:
    print(f"No significant difference detected (p={p_value:.4f}) -- fail to reject H0.")
```
> Explanation: `ttest_ind` compares the means of two independent samples and returns a p-value; comparing it to a pre-chosen significance threshold (`alpha`) determines whether to reject the null hypothesis that the two campaigns perform the same on average.

**Q: Given a DataFrame with `department` (categorical) and `left_company` (boolean), write code to test whether department is associated with attrition.**
```python
import pandas as pd
from scipy import stats

contingency_table = pd.crosstab(df["department"], df["left_company"])
chi2, p_value, dof, expected = stats.chi2_contingency(contingency_table)
print(f"chi2={chi2:.4f}, p={p_value:.4f}")
```
> Explanation: since both variables here are categorical (department, and whether someone left), a chi-square test of independence is the correct tool — `pd.crosstab()` builds the observed counts table that `chi2_contingency()` expects.

## Scenario Questions

**Q: A stakeholder shows you a chart where "Team A" has a higher average performance score than "Team B" and asks you to confirm Team A's process is better. How would you respond?**
> A: I'd first run a formal statistical test (a t-test comparing the two teams' scores) rather than trusting the visual difference alone, since a difference in sample means can easily arise from random variation, especially with smaller teams. If the test shows no statistically significant difference, I'd say so directly rather than confirming a conclusion the data doesn't actually support. Even if it is significant, I'd caution that correlation between "using Team A's process" and "higher scores" doesn't prove the process *caused* the improvement — other differences between the teams (tenure, workload, team composition) could be confounding factors.

**Q: You compute a correlation of 0.85 between ice cream sales and shark attacks in a coastal city dataset. How would you explain this in an interview?**
> A: This is a classic confounding-variable scenario — both ice cream sales and shark attacks increase in summer, driven by a third factor (warm weather leads to both more people buying ice cream and more people swimming in the ocean, which increases shark encounter opportunity). The correlation is real and could even be a useful predictive signal, but it would be a mistake to conclude either variable causes the other; the underlying driver is the shared seasonal factor.

## "Gotcha" Questions

**Q: A p-value of 0.04 is reported for a study with a sample size of 100,000. Does this necessarily mean the finding is practically important?**
> A: Not necessarily. With an extremely large sample size, even a tiny, practically negligible difference between groups can produce a statistically significant p-value, because larger samples make it easier to detect smaller and smaller true effects. It's essential to also look at the effect size (how large is the actual difference in real terms?) before deciding whether a statistically significant finding is actually worth acting on.

**Q: Someone says "there's a 95% probability the true average is between 45 and 55" based on a confidence interval. What's technically imprecise about this statement?**
> A: The true average is a fixed (if unknown) value — it either falls in the interval [45, 55] or it doesn't; there's no probability involved for one specific, already-calculated interval. The 95% figure describes the long-run behavior of the *procedure*: if you repeated the sampling and interval-construction process many times, about 95% of the resulting intervals would contain the true value. It's a subtle distinction, but a frequently tested one.

## Quick-Fire Rapid Review

- Q: More robust to outliers, mean or median? → **median**
- Q: What does skewness near 0 indicate? → **a roughly symmetric distribution**
- Q: Does correlation imply causation? → **No**
- Q: What does a p-value measure? → **probability of data this extreme, assuming H₀ is true**
- Q: Common significance threshold (α)? → **0.05**
- Q: Test for comparing two group means? → **t-test**
- Q: Test for comparing two categorical variables? → **chi-square**
- Q: What does "statistically significant" NOT automatically guarantee? → **practical/real-world importance (check effect size)**
