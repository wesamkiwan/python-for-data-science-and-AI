# Module 20c: Containerizing with Docker

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [02-serving-with-fastapi.md](02-serving-with-fastapi.md)

## 🎯 Learning Objectives
- [ ] Explain what a container is and the problem it solves
- [ ] Write a `Dockerfile` for a FastAPI model-serving application
- [ ] Build and run a Docker image
- [ ] Understand the basic Docker workflow used in real deployment pipelines

---

## ⚠️ A Note on This Lesson's Code

Like Module 19a's live API calls, this lesson has one honest exception to the course's "every example executed and verified" standard: **Docker requires a running Docker daemon**, which needs virtualization support this authoring environment's sandbox doesn't provide (the Docker Desktop backend was tested and confirmed to exit immediately on startup here). The `Dockerfile` and commands below use standard, extremely stable Docker syntax that has worked unchanged for years — but building and running the actual container was not executed in this specific environment. If you have Docker installed locally (Docker Desktop, or Docker Engine on Linux), every command here will work exactly as shown.

## Module Goal

Learn **Docker** — the standard tool for packaging an application (your FastAPI model server, Module 20b) together with everything it needs to run (Python version, libraries, the model file itself) into one portable, consistent unit called a **container**.

## Why This Matters on the Job

"It works on my machine" is one of the most common and costly problems in software deployment — a colleague's laptop has a slightly different Python version, a missing system library, or a different OS entirely, and your perfectly working API breaks the moment it's deployed elsewhere. Docker solves this permanently by packaging the *entire* runtime environment together with your code, guaranteeing it behaves identically no matter where it runs — a laptop, a company server, or a cloud platform.

---

## What Is a Container?

A **container** is a lightweight, isolated package containing your application code, its dependencies, and a minimal runtime environment — everything needed to run it, bundled together. Unlike a full virtual machine, containers share the host machine's operating system kernel, making them dramatically faster to start and lighter on resources.

💡 **Analogy:** Think of a container like a shipping container in global trade — regardless of what's inside (furniture, electronics, food), it has a standard size and interface, so any ship, truck, or crane can handle it identically. A software container standardizes "how to run this application" the same way, regardless of what's actually inside.

## Writing a `Dockerfile`

A **Dockerfile** is a text file with step-by-step instructions for building a container image.

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY wine_model.joblib .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
```

**How it works, line by line:**
- `FROM python:3.11-slim` — start from an official, minimal Python 3.11 base image (exactly Module 05's Python version concept, but as a pre-built, ready-to-use image rather than something you install yourself).
- `WORKDIR /app` — sets the working directory inside the container (everything after this happens relative to `/app`).
- `COPY requirements.txt .` + `RUN pip install ...` — copies your dependency list (Module 05a's `requirements.txt`) into the container and installs it. This is done in its own step, *before* copying your actual code, so Docker can cache this potentially-slow step and skip re-running it if only your code changes later (an important performance optimization for repeated builds).
- `COPY app.py .` and `COPY wine_model.joblib .` — copies your FastAPI app and Module 20a's saved model file into the container.
- `EXPOSE 8000` — documents that the container listens on port 8000 (informational; doesn't actually open the port by itself).
- `CMD [...]` — the command that runs when a container starts from this image: launching `uvicorn` to serve your FastAPI app, exactly like Module 20b, but now running *inside* the isolated container rather than directly on your machine.

## The `requirements.txt` File

```
fastapi
uvicorn
joblib
scikit-learn
numpy
```

💡 **Tip:** This is exactly Module 05a's `requirements.txt` concept — pin these to specific versions (`fastapi==0.115.0`) in a real production deployment, to guarantee the container behaves identically every time it's rebuilt, rather than picking up whatever the latest version happens to be at build time.

## Building and Running the Container

```bash
# Build the image (creates a reusable, packaged artifact from the Dockerfile)
docker build -t wine-classifier-api .

# Run a container from that image
docker run -p 8000:8000 wine-classifier-api
```

**How it works:** `docker build -t wine-classifier-api .` reads the `Dockerfile` in the current directory (`.`) and builds an **image** — a saved, reusable snapshot — tagged (`-t`) with the name `wine-classifier-api`. `docker run -p 8000:8000 wine-classifier-api` starts a running **container** from that image, mapping port 8000 inside the container to port 8000 on your actual machine (`-p host_port:container_port`) — after this, the API is reachable at `http://localhost:8000`, exactly as if you'd run `uvicorn` directly, but now fully isolated and portable.

```bash
# Verify it's running
curl http://localhost:8000/

# Test a prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [13.0, 2.0, 2.4, 15.0, 100.0, 2.5, 2.8, 0.3, 1.8, 5.0, 1.0, 3.0, 1000.0]}'
```

**How it works:** `curl` (a command-line HTTP client, functionally similar to Module 04's `requests` library but usable directly from the terminal) confirms the containerized API responds exactly like the local version did in Module 20b's `TestClient` tests — proof the containerization didn't change the application's actual behavior, only *how* it's packaged and run.

## Useful Docker Commands

```bash
docker images              # list all images you've built/pulled
docker ps                     # list currently running containers
docker ps -a                     # list ALL containers, including stopped ones
docker stop <container_id>          # stop a running container
docker logs <container_id>             # view a container's output/logs
```

⚠️ **Warning:** Every `docker run` without an existing container creates a *new* container from the image — old, stopped containers don't disappear automatically and can accumulate on a development machine. Use `docker ps -a` periodically to check for and clean up ones you no longer need.

## Why This Matters for Real Deployment

🎯 **On the job:** Once your application is a Docker image, deploying it to virtually any cloud platform (AWS, Google Cloud, Azure, or a container orchestration platform like Kubernetes) becomes largely a matter of pushing that image and telling the platform to run it — the platform doesn't need to know or care that it's a Python/FastAPI/scikit-learn application specifically, only that it's a standard container. This is precisely why Docker has become the near-universal packaging format across the entire software industry, not just for ML.

---

## Hands-On Exercise

**Task (requires Docker installed locally to actually run):** Write a `Dockerfile` and `requirements.txt` for the `api_practice.py` FastAPI app from Module 20b's exercise (the breast cancer classifier):
1. Base the image on `python:3.11-slim`.
2. Copy and install a `requirements.txt` covering `fastapi`, `uvicorn`, `joblib`, `scikit-learn`, `numpy`.
3. Copy your application file and the saved `cancer_model.joblib`.
4. Expose port 8000 and set the correct `CMD` to run the app with `uvicorn`.
5. If you have Docker installed, build the image, run the container, and test both endpoints with `curl` — otherwise, walk through each step conceptually and confirm you understand what each line accomplishes.

<details>
<summary>✅ Click to see the solution</summary>

`requirements.txt`:
```
fastapi
uvicorn
joblib
scikit-learn
numpy
```

`Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api_practice.py .
COPY cancer_model.joblib .

EXPOSE 8000

CMD ["uvicorn", "api_practice:app", "--host", "0.0.0.0", "--port", "8000"]
```

```bash
docker build -t cancer-classifier-api .
docker run -p 8000:8000 cancer-classifier-api

# In another terminal:
curl http://localhost:8000/
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]}'
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Copying code before installing dependencies | Copy `requirements.txt` and install first — Docker caches this step, speeding up rebuilds |
| Unpinned dependency versions in production | Pin exact versions (`fastapi==0.115.0`) for reproducible builds |
| Forgetting `--host 0.0.0.0` in the `CMD` | Without it, the server only listens inside the container, unreachable from outside |
| Letting stopped containers accumulate | Periodically check `docker ps -a` and clean up unneeded ones |

---

## ✅ Module Completion Checklist (Part C)
- [ ] Understand what a container is and the problem it solves
- [ ] Can write a `Dockerfile` for a FastAPI application
- [ ] Understand the `docker build`/`docker run` workflow
- [ ] Can test a containerized API with `curl`
- [ ] Completed (or conceptually walked through) the Dockerfile exercise

**Next:** Continue to [`04-monitoring-and-production.md`](04-monitoring-and-production.md)
