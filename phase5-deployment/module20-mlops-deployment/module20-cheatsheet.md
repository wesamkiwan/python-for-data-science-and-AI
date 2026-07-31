# 📋 Module 20 Cheat Sheet: MLOps & Deployment

Fast reference for packaging, serving, containerizing, and monitoring models.

## Packaging Models
```python
import joblib

joblib.dump(pipeline, "model.joblib")     # save the ENTIRE pipeline (preprocessing + model)
loaded = joblib.load("model.joblib")         # load it back, ready to .predict()
```
```python
# PyTorch: save/load only the weights (state_dict), not the full object
torch.save(model.state_dict(), "weights.pth")
model.load_state_dict(torch.load("weights.pth"))
model.eval()   # always, before inference
```
✅ Always package the full pipeline (scaling + model together) — never just the bare model.

## Serving with FastAPI
```python
from fastapi import FastAPI
from pydantic import BaseModel
import joblib

app = FastAPI()
model = joblib.load("model.joblib")   # load ONCE at startup, not per-request

class Features(BaseModel):
    features: list[float]

@app.get("/")
def root():
    return {"status": "running"}

@app.post("/predict")
def predict(data: Features):
    X = np.array(data.features).reshape(1, -1)
    prediction = model.predict(X)
    return {"prediction": int(prediction[0])}   # cast NumPy types to plain Python types!
```
```bash
uvicorn app:app --reload         # run locally
```
```python
from fastapi.testclient import TestClient
client = TestClient(app)
client.get("/")
client.post("/predict", json={"features": [...]})
```

## Containerizing with Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
COPY model.joblib .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```
```bash
docker build -t my-api .
docker run -p 8000:8000 my-api
docker ps                  # running containers
docker ps -a                  # all containers, including stopped
docker logs <container_id>       # view logs
```

## Monitoring
```python
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
logger = logging.getLogger("model_monitor")
logger.info(f"prediction={prediction}, confidence={confidence}")
```

### Data Drift Detection
```python
from scipy import stats

stat, p_value = stats.ks_2samp(training_data, production_data)
drift_detected = p_value < 0.05   # same alpha convention as Module 10b
```
| Concept | Definition |
|---|---|
| Data drift | Input feature distributions change over time |
| Model/concept drift | The relationship between features and target changes, even if inputs look similar |

## What to Monitor

| Signal | Available immediately? |
|---|---|
| Prediction latency | Yes |
| Prediction distribution | Yes |
| Input feature drift (KS test) | Yes |
| Actual accuracy on new labels | Usually delayed |
| Error/failure rates | Yes |

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| API returns a serialization error | Returning raw NumPy types | Convert to plain `int`/`float`/`str` before returning |
| `422 Unprocessable Entity` from FastAPI | Request body doesn't match the Pydantic model | Check field names/types match exactly |
| Model loads correctly locally but fails in Docker | Missing dependency in `requirements.txt`, or model file not copied | Check `Dockerfile` COPY lines and pinned dependencies |
| Container unreachable from host | Missing `-p host:container` port mapping, or `--host 0.0.0.0` | Always bind `0.0.0.0` inside the container; map the port on `docker run` |
| Drift check always says "drift" or never does | Threshold (`alpha`) too strict/loose for your data's natural variability | Calibrate against historical known-stable periods first |

## The "Deploy a Model" Workflow
1. Package: save the full pipeline (`joblib`) or model weights (PyTorch `state_dict`).
2. Serve: wrap it in a FastAPI app, load the model once at startup, validate input with Pydantic.
3. Test locally with `TestClient` before deploying anywhere.
4. Containerize: write a `Dockerfile`, build, and run — verify with `curl`.
5. Monitor: log every prediction; run scheduled drift checks (`ks_2samp`) on key features.
