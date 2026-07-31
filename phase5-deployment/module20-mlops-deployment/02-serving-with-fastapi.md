# Module 20b: Serving a Model with FastAPI

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [01-packaging-models.md](01-packaging-models.md)

## 🎯 Learning Objectives
- [ ] Explain what a REST API is and why models are typically served this way
- [ ] Build a FastAPI application that loads a model and serves predictions
- [ ] Use Pydantic models to validate incoming request data
- [ ] Test an API locally before deployment

---

## Module Goal

Turn Module 20a's saved model into a real, callable web service using **FastAPI** — the modern, industry-standard Python framework for building APIs, chosen specifically for its speed, simplicity, and automatic data validation.

## Why This Matters on the Job

A saved model file is useless to other systems until it's wrapped in something they can actually call — a web application, a mobile app backend, another internal service. A REST API is the universal, language-agnostic way to expose "send me data, I'll send you a prediction" functionality, and FastAPI has become the dominant choice for exactly this in the Python ML ecosystem, thanks to its speed and built-in request validation.

---

## What Is a REST API?

Recall Module 04's lesson on *calling* an API with `requests` — now you'll build one. A **REST API** exposes functionality over HTTP: a client sends a request (often with data in the body, as JSON) to a specific URL path, and the server responds — exactly the client-server pattern from Module 04, just from the *server* side this time.

## Installing FastAPI

```bash
pip install fastapi uvicorn
```

**FastAPI** is the framework for defining your API's routes and logic. **Uvicorn** is the actual server that runs your FastAPI application and handles incoming network requests.

## Building a Minimal API

```python
# app.py
from fastapi import FastAPI

app = FastAPI(title="Wine Classifier API")

@app.get("/")
def read_root():
    return {"message": "Wine classifier API is running"}
```

**How it works:** `app = FastAPI()` creates the application object. `@app.get("/")` is a **decorator** (you've seen decorators before — `@classmethod`/`@staticmethod` in Module 12a, `@property` in Module 03c) that registers the function below it to handle GET requests to the `/` path — when a client visits this URL, `read_root()` runs and its return value (a dict) is automatically converted to JSON.

Run it locally with:

```bash
uvicorn app:app --reload
```

**How it works:** `app:app` means "in the file `app.py`, use the object named `app`." `--reload` restarts the server automatically whenever you save code changes — extremely useful during development.

## Adding a Prediction Endpoint

```python
# app.py (continued)
from pydantic import BaseModel
import joblib
import numpy as np

model = joblib.load("wine_model.joblib")   # load ONCE, when the app starts -- not per request!

class WineFeatures(BaseModel):
    features: list[float]

@app.post("/predict")
def predict(data: WineFeatures):
    X = np.array(data.features).reshape(1, -1)
    prediction = model.predict(X)
    probabilities = model.predict_proba(X)
    return {
        "prediction": int(prediction[0]),
        "confidence": float(probabilities[0][prediction[0]])
    }
```

**How it works:**
- `model = joblib.load(...)` runs *once*, when the application starts — not on every request. Loading a model is relatively slow; reloading it per-request would make the API needlessly slow for every single call.
- `class WineFeatures(BaseModel):` defines the expected **request body shape** using **Pydantic** — FastAPI's data validation library. `features: list[float]` declares that incoming JSON must have a `"features"` key containing a list of numbers.
- `@app.post("/predict")` registers this function for POST requests (Module 04's distinction between GET and POST) to `/predict`.
- FastAPI automatically validates every incoming request against `WineFeatures` *before* your function even runs — if a client sends malformed data (missing the field, wrong type), FastAPI automatically returns a clear `422` error response, without you writing any validation code yourself.

⚠️ **Warning:** `int(prediction[0])` and `float(probabilities[0][prediction[0]])` explicitly convert NumPy's own number types (like `numpy.int64`) to plain Python `int`/`float` — FastAPI's JSON conversion doesn't natively understand NumPy types, and skipping this conversion is a very common source of confusing serialization errors.

## Testing the API Locally

Before deploying anywhere, always test locally. FastAPI provides a `TestClient` for exactly this, without needing to actually start a running server:

```python
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

response = client.get("/")
print(response.status_code, response.json())
```
```
200 {'message': 'Wine classifier API is running'}
```

```python
sample_features = [13.0, 2.0, 2.4, 15.0, 100.0, 2.5, 2.8, 0.3, 1.8, 5.0, 1.0, 3.0, 1000.0]
response = client.post("/predict", json={"features": sample_features})
print(response.status_code, response.json())
```
```
200 {'prediction': 0, 'confidence': 0.9816125429894987}
```

**How it works:** `TestClient` lets you send requests to your FastAPI app directly in Python (exactly like Module 04's `requests.get()`/`.post()`, but targeting your own in-process app instead of a real network address) — perfect for automated testing before ever deploying anything.

🎯 **On the job:** FastAPI also auto-generates interactive API documentation (visit `/docs` on a running server) directly from your Pydantic models and route definitions — an enormously convenient feature for letting teammates or other teams explore and test your API without reading any of your code.

---

## Hands-On Exercise

**Task:** Write `api_practice.py` (as a FastAPI app) that:
1. Loads the `cancer_model.joblib` pipeline from Module 20a's exercise (retrain and save it first if needed).
2. Defines a Pydantic model `CancerFeatures` with a `features: list[float]` field.
3. Adds a `GET /` endpoint returning a simple status message.
4. Adds a `POST /predict` endpoint that returns the prediction (`"malignant"`/`"benign"`, using the dataset's `target_names`) and confidence score.
5. Uses `TestClient` to test both endpoints, printing the status codes and responses.

<details>
<summary>✅ Click to see the solution</summary>

```python
# First, ensure the model exists (from Module 20a's exercise):
import joblib
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

data = load_breast_cancer()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.2, random_state=42)
pipeline = Pipeline(steps=[("scaler", StandardScaler()), ("classifier", RandomForestClassifier(n_estimators=100, random_state=42))])
pipeline.fit(X_train, y_train)
joblib.dump(pipeline, "cancer_model.joblib")

# api_practice.py
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="Cancer Classifier API")
model = joblib.load("cancer_model.joblib")
target_names = data.target_names

class CancerFeatures(BaseModel):
    features: list[float]

@app.get("/")
def read_root():
    return {"message": "Cancer classifier API is running"}

@app.post("/predict")
def predict(request: CancerFeatures):
    X = np.array(request.features).reshape(1, -1)
    prediction = model.predict(X)
    probabilities = model.predict_proba(X)
    return {
        "prediction": target_names[prediction[0]],
        "confidence": float(probabilities[0][prediction[0]])
    }

client = TestClient(app)

response = client.get("/")
print(response.status_code, response.json())

sample = X_test[0].tolist()
response = client.post("/predict", json={"features": sample})
print(response.status_code, response.json())
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Loading the model inside the endpoint function | Load it once, at module level, when the app starts |
| Returning raw NumPy types (`numpy.int64`, etc.) | Convert explicitly to Python `int`/`float`/`str` before returning |
| Skipping request validation | Use Pydantic models — FastAPI validates automatically, no manual checks needed |
| Deploying without testing locally first | Always test with `TestClient` (or manual requests) before deploying anywhere |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Understand what a REST API is and why models are served this way
- [ ] Can build a FastAPI app with GET and POST endpoints
- [ ] Can use Pydantic models for automatic request validation
- [ ] Can test an API locally with `TestClient`
- [ ] Completed the `api_practice.py` exercise

**Next:** Continue to [`03-containerizing-with-docker.md`](03-containerizing-with-docker.md)
