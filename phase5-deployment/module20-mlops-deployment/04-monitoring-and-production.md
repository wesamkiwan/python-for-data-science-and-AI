# Module 20d: Monitoring Models in Production

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [03-containerizing-with-docker.md](03-containerizing-with-docker.md)

## 🎯 Learning Objectives
- [ ] Explain why deploying a model isn't the end of the job
- [ ] Log predictions for later analysis and debugging
- [ ] Explain data drift and model drift
- [ ] Detect data drift statistically, using Module 10's hypothesis testing framework

---

## Module Goal

Close out this course by learning what happens *after* deployment: **monitoring** — the ongoing practice of watching a live model to catch problems (bad predictions, degrading accuracy, changing data) before they cause real business harm.

## Why This Matters on the Job

A model's performance at launch is not guaranteed to hold forever — the real world changes, and a model trained on last year's data can silently become less accurate on this year's data without anyone noticing, unless someone is actively watching for it. Monitoring is what separates "we deployed a model" from "we're running a reliable, trustworthy production ML system" — and it's precisely the kind of ongoing responsibility that makes MLOps a distinct discipline from just training models.

---

## Why Deployment Isn't "Done"

Recall Module 13c's overfitting lesson: a model's test-set performance is only an honest estimate *at the time it was measured*, using data reflecting the world *as it was* during training and testing. Once deployed, a model keeps making predictions on genuinely new data indefinitely — and if the real world shifts (customer behavior changes, a new product category emerges, an economic shock hits), the model's original test-set accuracy no longer guarantees anything about its current, live performance.

## Logging Predictions

The first, most basic monitoring practice: **log every prediction** — what input it received, what it predicted, and how confident it was — so you have a record to investigate later if something seems wrong.

```python
import logging
import json

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("model_monitor")

def log_prediction(features, prediction, confidence):
    log_entry = {
        "features": features,
        "prediction": prediction,
        "confidence": confidence
    }
    logger.info(f"Prediction logged: {json.dumps(log_entry)}")

log_prediction([1.0, 2.0, 3.0], 1, 0.95)
```
```
2026-07-31 10:39:39,497 - Prediction logged: {"features": [1.0, 2.0, 3.0], "prediction": 1, "confidence": 0.95}
```

**How it works:** Python's built-in `logging` module (rather than plain `print()`) is the standard way to record events in a production application — it includes timestamps automatically, supports different severity levels (`INFO`, `WARNING`, `ERROR`), and can be configured to write to files, external logging services, or monitoring dashboards without changing your application code.

🎯 **On the job:** Integrate this directly into your Module 20b FastAPI `/predict` endpoint — log every incoming request and its resulting prediction. When a user or teammate reports "this model gave a weird answer," these logs are what let you actually investigate what happened, rather than being unable to reproduce or even see the problematic case at all.

## Data Drift vs. Model Drift

- **Data drift:** the statistical properties of the *input* data change over time (e.g., customer ages, average order sizes, or feature distributions shift from what the model was trained on).
- **Model drift** (also called concept drift): the actual *relationship* between features and target changes over time, even if the input data's distribution looks the same (e.g., what predicts "customer churn" genuinely changes as market conditions evolve).

Both mean a model's original training-time performance no longer reflects its current, real-world accuracy.

## Detecting Data Drift Statistically

This is a direct, practical extension of Module 10's hypothesis testing: use a statistical test to check whether new production data's distribution differs significantly from the training data's distribution.

```python
import numpy as np
from scipy import stats

np.random.seed(42)
training_data = np.random.normal(50, 10, 1000)        # feature's distribution during training
production_data_no_drift = np.random.normal(50, 10, 200)     # similar distribution -- no drift
production_data_with_drift = np.random.normal(65, 15, 200)      # shifted distribution -- real drift

stat_no_drift, p_no_drift = stats.ks_2samp(training_data, production_data_no_drift)
stat_drift, p_drift = stats.ks_2samp(training_data, production_data_with_drift)

print(f"No drift scenario: KS stat={stat_no_drift:.4f}, p-value={p_no_drift:.4f}")
print(f"Drift scenario: KS stat={stat_drift:.4f}, p-value={p_drift:.4f}")

alpha = 0.05
print(f"No drift detected: {p_no_drift > alpha}")
print(f"Drift detected: {p_drift < alpha}")
```
```
No drift scenario: KS stat=0.0840, p-value=0.1833
Drift scenario: KS stat=0.4960, p-value=0.0000
No drift detected: True
Drift detected: True
```

**How it works:** `stats.ks_2samp()` runs the **Kolmogorov-Smirnov test**, comparing two samples' full distributions (not just their means) and returning a p-value — precisely the same hypothesis-testing logic from Module 10b's t-test, just testing "do these two samples come from the same distribution?" instead of "do these two groups have the same mean?" A p-value below your significance threshold (`α = 0.05`, exactly Module 10b's convention) means the production data's distribution differs significantly from training — a statistically-grounded drift alert, rather than a vague, subjective "this feels off."

✅ **Best Practice:** Run this kind of drift check on a **schedule** (e.g., daily or weekly) comparing recent production data against your original training data for every important feature — automating it into an alert (e.g., a Slack message or dashboard flag) when drift is detected, rather than manually re-running checks and hoping to remember to look.

⚠️ **Warning:** Detecting drift doesn't automatically mean "retrain immediately" — first *investigate* why the distribution shifted (a genuine, meaningful business change? a data pipeline bug feeding in bad values? a seasonal effect?) before deciding what to do about it, exactly the same investigative discipline Module 10's "correlation isn't causation" lesson encouraged.

## Basic Production Monitoring Checklist

| What to monitor | Why |
|---|---|
| Prediction latency (response time) | Slow predictions degrade user experience |
| Prediction distribution (e.g., % positive vs. negative) | A sudden shift can signal a problem, even without labeled ground truth |
| Input feature distributions (drift, this lesson) | Detects when production data no longer resembles training data |
| Model accuracy on newly-labeled data (once available) | The most direct measure, but often delayed (labels arrive later) |
| Error rates / failed requests | Catches outright bugs or infrastructure problems |

🎯 **On the job:** In many real systems, true labels (the actual correct answer) aren't available immediately — you often won't know if a fraud prediction was right for days or weeks. This is exactly why monitoring input drift and prediction-distribution shifts matters so much: they're available *immediately*, as early warning signals, well before delayed ground-truth labels can confirm an actual accuracy drop.

---

## Hands-On Exercise

**Task:** Write `monitoring_practice.py` that:
1. Simulates a `feature_values` array representing a model's training data for one important feature (any reasonable distribution, at least 500 points).
2. Simulates two production batches: one with the *same* distribution (no real drift), and one with a *shifted* distribution (representing genuine drift) — at least 100 points each.
3. Runs `stats.ks_2samp()` comparing training data against each production batch, printing the KS statistic and p-value for both.
4. Writes a function `check_drift(training_data, production_data, alpha=0.05)` that returns `True`/`False` for whether drift was detected, and prints a clear message either way.
5. Adds simple prediction logging (using Python's `logging` module) for at least 3 simulated predictions.

<details>
<summary>✅ Click to see the solution</summary>

```python
import numpy as np
from scipy import stats
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("model_monitor")

def check_drift(training_data, production_data, alpha=0.05):
    stat, p_value = stats.ks_2samp(training_data, production_data)
    drift_detected = p_value < alpha
    if drift_detected:
        print(f"DRIFT DETECTED (KS stat={stat:.4f}, p={p_value:.4f})")
    else:
        print(f"No significant drift (KS stat={stat:.4f}, p={p_value:.4f})")
    return drift_detected

np.random.seed(10)
training_feature = np.random.normal(100, 20, 500)
production_no_drift = np.random.normal(100, 20, 150)
production_with_drift = np.random.normal(130, 25, 150)

print("Checking production batch 1 (expected: no drift):")
check_drift(training_feature, production_no_drift)

print("Checking production batch 2 (expected: drift):")
check_drift(training_feature, production_with_drift)

def log_prediction(features, prediction, confidence):
    logger.info(f"features={features}, prediction={prediction}, confidence={confidence:.4f}")

log_prediction([100.2, 45.1], 1, 0.87)
log_prediction([98.7, 43.9], 0, 0.62)
log_prediction([105.3, 47.2], 1, 0.91)
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Assuming a deployed model needs no further attention | Monitor continuously — real-world data and relationships change over time |
| Only checking accuracy, which requires delayed ground-truth labels | Also monitor input drift and prediction distributions, available immediately |
| Retraining automatically the moment any drift is flagged | Investigate the cause first — could be a genuine shift, a bug, or seasonality |
| Using `print()` instead of proper logging in production code | Use Python's `logging` module for timestamps, severity levels, and configurability |

---

## ✅ Module 20 Completion Checklist
- [ ] Understand why deployment isn't the end of the ML lifecycle
- [ ] Can log predictions using Python's `logging` module
- [ ] Understand the difference between data drift and model/concept drift
- [ ] Can detect data drift statistically using a hypothesis test
- [ ] Completed the `monitoring_practice.py` exercise
- [ ] Reviewed [`module20-cheatsheet.md`](module20-cheatsheet.md)
- [ ] Reviewed [`module20-interview.md`](module20-interview.md)
- [ ] Browsed [`module20-references.md`](module20-references.md)

**Next Step:** Capstone Projects (`capstones/`) — apply everything from this entire course to real, portfolio-worthy projects!

---

## 🎉 All 20 Modules Complete!

Congratulations — you've completed the entire zero-to-hero curriculum, from Python fundamentals through NumPy/Pandas/statistics, classical machine learning, deep learning (CNNs, Transformers, LLMs), and now full production deployment (packaging, APIs, containers, monitoring). You have the complete skillset of a job-ready data scientist / ML engineer. The three capstone projects ahead let you demonstrate all of it, end to end, on real, portfolio-worthy work.
