# 🎤 Module 20 Interview Prep: MLOps & Deployment

## Conceptual Questions

### 🟢 Beginner

**Q: Why do you save a trained model instead of retraining it every time you need a prediction?**
> A: Training is typically expensive (can take minutes to days), while a production API often needs to respond in milliseconds. Saving a trained model lets you separate the expensive, one-time training step from the cheap, repeated prediction step — you train once, save the result, then load and reuse it for every future prediction request.

**Q: Why should you save the entire preprocessing + model pipeline together, rather than just the bare model?**
> A: If a scaler or encoder was fit on the training data, predictions on new data must go through the exact same transformation to be valid — saving just the model risks applying inconsistent or missing preprocessing at prediction time, silently producing wrong results. Saving the entire `Pipeline` object guarantees the same preprocessing steps are applied identically every time.

**Q: What is a REST API, and why is it a natural way to serve a model?**
> A: A REST API exposes functionality over HTTP — a client sends a request (often with data as JSON) to a specific URL, and the server responds. This is a natural way to serve a model because it's language-agnostic (any system that can make an HTTP request can use your model, regardless of what language it's written in) and lets many different applications call the same deployed model consistently.

### 🟡 Intermediate

**Q: Why is Docker useful for deploying an ML model, beyond just "packaging the code"?**
> A: Docker packages not just your code but the entire runtime environment — the exact Python version, exact library versions, and any system-level dependencies — into one portable image. This eliminates "it works on my machine" problems, since the container behaves identically regardless of what's installed (or not installed) on whatever machine actually runs it, whether that's a teammate's laptop, a company server, or a cloud platform.

**Q: What's the difference between data drift and model (concept) drift?**
> A: Data drift means the statistical distribution of input features has changed over time compared to what the model was trained on — e.g., customer ages or order sizes shifting. Model/concept drift means the actual relationship between features and the target has changed, even if the inputs look similar — e.g., what predicts churn genuinely changing as market conditions evolve. Both cause a model's original training-time performance to no longer reflect its current real-world accuracy, but they arise from different underlying causes.

**Q: Why is monitoring input data drift valuable even before you have new ground-truth labels to check accuracy against?**
> A: In many real systems, true labels arrive with a significant delay (e.g., you might not know if a fraud prediction was correct for days or weeks) or may never be fully available. Input feature drift and prediction-distribution shifts are available immediately, providing an early warning signal that something may be wrong well before a delayed, direct accuracy measurement could confirm it.

## Practical/Coding Questions

**Q: Write code to detect whether a production feature's distribution has significantly drifted from its training distribution.**
```python
from scipy import stats

def check_drift(training_data, production_data, alpha=0.05):
    stat, p_value = stats.ks_2samp(training_data, production_data)
    return p_value < alpha, stat, p_value

drifted, stat, p_value = check_drift(training_feature, production_feature)
if drifted:
    print(f"Drift detected (KS stat={stat:.4f}, p={p_value:.4f})")
```
> Explanation: the Kolmogorov-Smirnov test (Module 20d) compares two samples' full distributions and returns a p-value; a value below the significance threshold indicates the distributions differ significantly, following the exact same hypothesis-testing logic as Module 10b's t-test.

**Q: Write a minimal FastAPI endpoint that validates input with Pydantic and returns a model's prediction, being careful about data types.**
```python
from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np

app = FastAPI()

class InputData(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(data: InputData):
    X = np.array(data.features).reshape(1, -1)
    prediction = model.predict(X)
    return {"prediction": int(prediction[0])}   # cast from numpy.int64 to plain int
```
> Explanation: the Pydantic `InputData` model gives FastAPI automatic request validation for free; casting `prediction[0]` to a plain `int` avoids a common JSON serialization error, since FastAPI's default JSON encoder doesn't natively understand NumPy's own number types.

## Scenario Questions

**Q: Your team deployed a fraud-detection model six months ago, and a stakeholder now says it "feels less accurate lately," but you have no recent labeled fraud data to check against. How would you investigate?**
> A: Since ground-truth labels aren't available yet, I'd start with the signals that are available immediately: checking whether the input feature distributions have drifted significantly from the original training data (using a statistical test like KS), and whether the model's prediction distribution (e.g., percentage flagged as fraud) has shifted noticeably from its historical baseline. Either finding would support the stakeholder's concern even without fresh labels, and would help prioritize whether retraining or further investigation is warranted once labels do become available.

**Q: A newly containerized model API works when you run it locally with `uvicorn` directly, but fails to respond when run inside Docker. What would you check first?**
> A: I'd first check that the app is bound to `0.0.0.0` rather than `localhost`/`127.0.0.1` inside the container — binding only to localhost makes the server unreachable from outside the container, even with a port mapping in place. I'd also verify the `docker run -p host_port:container_port` mapping matches the port the app actually listens on, and check `docker logs <container_id>` for any startup errors (e.g., a missing dependency not included in `requirements.txt`).

## "Gotcha" Questions

**Q: A model deployed via a FastAPI endpoint occasionally throws a serialization error when returning predictions, even though it works fine when called directly in a Python script. What's the likely cause?**
> A: The prediction value is probably still a NumPy type (like `numpy.int64` or `numpy.float32`) rather than a plain Python `int`/`float` — FastAPI's default JSON encoder doesn't know how to serialize NumPy's own number types directly. The fix is to explicitly cast model outputs to plain Python types (`int(prediction[0])`, `float(probability)`) before returning them from the endpoint.

**Q: A drift-detection alert fires, and someone immediately retrains the model without further investigation. What's the risk with this reflex?**
> A: Detecting statistical drift doesn't automatically mean the drift represents a genuine, harmful change requiring retraining — it could also reflect a data pipeline bug feeding in corrupted values, a temporary seasonal effect, or another explanation entirely. Retraining immediately without investigating the cause risks wasting effort on an unnecessary retrain, or worse, training a new model on the very bad/corrupted data that triggered the alert in the first place.

## Quick-Fire Rapid Review

- Q: What should you always save alongside a trained model, not just the model itself? → **the full preprocessing pipeline**
- Q: What Python library validates FastAPI request bodies automatically? → **Pydantic**
- Q: Why load a model at module level in a FastAPI app, not inside the endpoint function? → **loading is slow; doing it per-request would needlessly slow every call**
- Q: What must you cast NumPy prediction outputs to before returning them from an API? → **plain Python types (`int`/`float`/`str`)**
- Q: What does a Dockerfile's `EXPOSE` instruction do? → **documents the port the container listens on (informational)**
- Q: What flag maps a container's port to the host machine? → **`-p host_port:container_port` on `docker run`**
- Q: Statistical test used for detecting data drift in this module? → **the Kolmogorov-Smirnov test (`ks_2samp`)**
- Q: Which is available sooner: input drift detection or ground-truth accuracy measurement? → **input drift detection**
