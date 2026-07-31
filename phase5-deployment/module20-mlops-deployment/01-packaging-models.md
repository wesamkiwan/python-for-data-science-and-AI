# Module 20a: Packaging Models for Deployment

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [Module 19 — Generative AI & LLMs](../../phase4-deep-learning-and-ai/module19-genai-llms/03-building-a-rag-pipeline.md)

## 🎯 Learning Objectives
- [ ] Explain why a trained model needs to be saved/packaged for deployment
- [ ] Save and load a scikit-learn model (including a full `Pipeline`) with `joblib`
- [ ] Save and load a PyTorch model's weights
- [ ] Understand what "deployment" actually means in a production context

---

## Module Goal

Welcome to **Phase 5: Deployment** — the final phase of this course! Everything so far has trained models inside a script or notebook. This module teaches you how to take a trained model out of that script and turn it into something real users or systems can actually use: a packaged file, a running API, and a deployed, monitored service.

## Why This Matters on the Job

A model sitting in a Jupyter notebook provides zero business value — it only becomes useful once it's deployed somewhere it can make predictions on new, real-world data as part of an actual product or workflow. "MLOps" (Machine Learning Operations) is the entire discipline built around this — reliably packaging, deploying, and monitoring models in production — and it's an increasingly expected skill for data scientists, not just dedicated ML engineers.

---

## Why You Can't Just Re-Run Your Training Script

Retraining a model every time you need a prediction is wasteful and often impossible in production (training can take minutes to days; a production API needs to respond in milliseconds). Instead, you **train once, save the trained model, then load and reuse it** for every future prediction — exactly the distinction between Module 12's `.fit()` (expensive, done once) and `.predict()` (cheap, done repeatedly, potentially by a live service).

## Packaging a scikit-learn Model with `joblib`

```bash
pip install joblib
```

```python
import joblib
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42
)

pipeline = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("classifier", LogisticRegression(max_iter=1000))
])
pipeline.fit(X_train, y_train)
print(f"Accuracy: {pipeline.score(X_test, y_test):.4f}")

joblib.dump(pipeline, "wine_model.joblib")   # save the ENTIRE trained pipeline to disk
```

**How it works:** `joblib.dump()` serializes the entire trained object — including the fitted `StandardScaler`'s learned mean/std (Module 13a) and the `LogisticRegression`'s learned coefficients — into a single file. Critically, this saves the **whole `Pipeline`** (Module 13b), not just the classifier — meaning the exact same scaling used during training is guaranteed to be applied identically at prediction time, with no risk of the data leakage/inconsistency mistakes flagged in Module 13b.

```python
loaded_pipeline = joblib.load("wine_model.joblib")
print(f"Loaded model accuracy: {loaded_pipeline.score(X_test, y_test):.4f}")

sample = X_test[0:1]
prediction = loaded_pipeline.predict(sample)
print(f"Prediction: {prediction}")
```

**How it works:** `joblib.load()` reconstructs the exact trained object — no retraining needed. This loaded pipeline behaves identically to the original: same `.predict()`, same learned scaling, same everything — this is precisely the artifact you'd deploy in the next lesson's API.

✅ **Best Practice:** Always save the *entire pipeline* (preprocessing + model), never just the bare model — this is the single most common real-world deployment bug: a model deployed without its exact matching preprocessing steps produces silently wrong predictions on new data.

💡 **Tip:** `joblib` is preferred over Python's built-in `pickle` module for scikit-learn objects specifically because it's more efficient for the large NumPy arrays scikit-learn models often contain internally — though `pickle` works too and you'll see both in real code.

## Packaging a PyTorch Model

PyTorch models are typically saved differently — as their learned **weights** (`state_dict`), not the full object:

```python
import torch
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(13, 32)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(32, 3)

    def forward(self, x):
        return self.layer2(self.relu(self.layer1(x)))

model = SimpleNet()
# ... (train the model, as in Module 16b) ...

torch.save(model.state_dict(), "model_weights.pth")
```

```python
# To load: recreate the SAME architecture, then load the saved weights into it
loaded_model = SimpleNet()
loaded_model.load_state_dict(torch.load("model_weights.pth"))
loaded_model.eval()   # switch to evaluation mode (Module 16d) -- disables dropout, etc.

sample = torch.randn(1, 13)
with torch.no_grad():
    prediction = loaded_model(sample)
```

**How it works:** Unlike `joblib`'s "save the whole thing" approach, PyTorch's convention is to save only the learned numeric weights (`state_dict()` — a dictionary mapping each layer's name to its tensor of weights), *not* the class definition itself. This means you must have the exact same `SimpleNet` class definition available when loading — the weights alone don't reconstruct the architecture, only fill in its learned values.

⚠️ **Warning:** If your model's class definition changes (different layer sizes, added/removed layers) between saving and loading, `load_state_dict()` will fail with a shape mismatch error. Keep your model architecture code version-controlled (Module 05b) alongside the saved weights file, so they always stay in sync.

## What "Deployment" Actually Means

**Deployment** is the process of making a trained model available to receive real input and return real predictions, as part of a live system. This usually means:

1. **Package** the trained model (this lesson — `joblib`/`state_dict`).
2. **Serve** it behind an interface other software can call — most commonly a REST API (Module 20b).
3. **Containerize** it so it runs consistently regardless of the underlying machine (Module 20c).
4. **Monitor** it in production to catch problems before they cause real harm (Module 20d).

🎯 **On the job:** This four-step shape — package, serve, containerize, monitor — is essentially universal across companies and model types, whether you're deploying a simple scikit-learn classifier or a large deep learning model. The next three lessons walk through each remaining step in order.

---

## Hands-On Exercise

**Task:** Write `packaging_practice.py` that:
1. Trains a `RandomForestClassifier` (Module 15a) wrapped in a `Pipeline` with a `StandardScaler`, on the `load_breast_cancer()` dataset from `sklearn.datasets` (a built-in binary classification dataset).
2. Saves the trained pipeline with `joblib.dump()`.
3. In the same script (simulating a "fresh" load), loads the pipeline back with `joblib.load()`.
4. Confirms the loaded pipeline's accuracy on a held-out test set matches the original's exactly.
5. Uses the loaded pipeline to predict on a single new sample and prints the result.

<details>
<summary>✅ Click to see the solution</summary>

```python
import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(
    data.data, data.target, test_size=0.2, random_state=42
)

pipeline = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))
])
pipeline.fit(X_train, y_train)
original_accuracy = pipeline.score(X_test, y_test)
print(f"Original accuracy: {original_accuracy:.4f}")

joblib.dump(pipeline, "cancer_model.joblib")

loaded_pipeline = joblib.load("cancer_model.joblib")
loaded_accuracy = loaded_pipeline.score(X_test, y_test)
print(f"Loaded accuracy: {loaded_accuracy:.4f}")
assert original_accuracy == loaded_accuracy, "Loaded model should match exactly!"

sample = X_test[0:1]
prediction = loaded_pipeline.predict(sample)
print(f"Prediction for one new sample: {data.target_names[prediction[0]]}")
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Saving only the bare model, not the full preprocessing pipeline | Always save/deploy the entire `Pipeline` together |
| Loading PyTorch weights into a mismatched architecture | Keep the model class definition version-controlled alongside saved weights |
| Forgetting `model.eval()` after loading a PyTorch model | Always call it before inference — exactly like Module 16d |
| Treating "it works in my notebook" as "it's deployed" | Deployment means packaged + served + accessible to real systems, not just runnable locally |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand why models must be saved/packaged rather than retrained on demand
- [ ] Can save/load a scikit-learn `Pipeline` with `joblib`
- [ ] Can save/load a PyTorch model's `state_dict`
- [ ] Understand the four-step shape of deployment (package, serve, containerize, monitor)
- [ ] Completed the `packaging_practice.py` exercise

**Next:** Continue to [`02-serving-with-fastapi.md`](02-serving-with-fastapi.md)
