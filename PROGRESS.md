# Progress Tracker: Python for Data Science & AI

This file tracks two separate things — don't confuse them:

1. **Content Status** (right-most column) — whether the material for a module has been *written* yet. This is informational only; you don't edit it.
2. **Your checkboxes** (Learning / Exercise / Cheat Sheet / Interview / References) — these are **for you, the learner**, to check off yourself as you actually work through each piece. They start empty and stay empty until you do the work — nobody pre-fills these for you.

**Content Available:** 20/20 modules written (100%) — all modules complete! Capstones and master files remain.
**Your Progress:** 0/20 modules complete (0%) — check boxes below as you go!

| # | Module | Difficulty | Est. Time | Learning | Exercise | Cheat Sheet | Interview | References | Content Status |
|---|--------|:----------:|:---------:|:--------:|:--------:|:-----------:|:---------:|:----------:|--------|
| 01 | Python Fundamentals | 🟢 | 4h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 02 | Functions, Modules & Error Handling | 🟢 | 3h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 03 | Object-Oriented Programming (OOP) | 🟢 | 3h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 04 | File I/O, JSON/CSV & APIs | 🟢 | 2h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 05 | Python Tooling & Environments | 🟢 | 2h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 06 | NumPy Fundamentals | 🟡 | 3h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 07 | Pandas for Data Manipulation | 🟡 | 5h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 08 | Data Cleaning & Wrangling | 🟡 | 4h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 09 | Data Visualization | 🟡 | 4h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 10 | EDA & Statistics | 🟡 | 4h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 11 | SQL for Data Scientists | 🟡 | 3h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 12 | ML Foundations (scikit-learn) | 🟡 | 5h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 13 | Feature Engineering & Model Evaluation | 🟡 | 4h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 14 | Unsupervised Learning & Clustering | 🟡 | 3h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 15 | Ensemble Methods & Advanced ML | 🔴 | 4h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 16 | Deep Learning Foundations (PyTorch + TF/Keras) | 🔴 | 6h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 17 | Computer Vision (CNNs) | 🔴 | 4h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 18 | NLP & Transformers | 🔴 | 5h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 19 | Generative AI & LLMs | 🔴 | 5h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |
| 20 | MLOps & Deployment | 🔴 | 5h | [ ] | [ ] | [ ] | [ ] | [ ] | 📗 Content ready |

## Capstone Projects
- [ ] Capstone 1: End-to-end EDA + ML project 🟡 (unlocked — Module 15 done) — ⏳ not written yet
- [ ] Capstone 2: Deep learning image classifier (CNN) 🔴 (unlocked — Module 17 done) — ⏳ not written yet
- [ ] Capstone 3: LLM-powered RAG application 🔴 (unlocked — Module 19 done) — ⏳ not written yet

## Master Files
- [ ] `master-cheatsheet.md` (built incrementally, finalized after Module 20) — ⏳ not started
- [ ] `master-interview-prep.md` (built incrementally, finalized after Module 20) — ⏳ not started
- [ ] `master-references.md` (built incrementally, finalized after Module 20) — ⏳ not started

---

## 🛠️ Course-Author Log (for resuming content creation — not a learner section)

👉 **Content written through:** Module 20 — MLOps & Deployment (Phase 5: Deployment) — 🎉 **ALL 20 MODULES COMPLETE!**
👉 **Next to write:** Capstone 1 — End-to-end EDA + ML Project

**Resume instructions for next authoring session:** Module 20 is fully written (4 learning files — `01-packaging-models.md`, `02-serving-with-fastapi.md`, `03-containerizing-with-docker.md`, `04-monitoring-and-production.md` — + cheatsheet + interview + references, all committed and pushed to GitHub). **Two honesty notes preserved in the lessons themselves, matching the Module 19 pattern:** (1) Docker — `docker --version` works but the Docker Desktop backend was tested and confirmed to exit immediately on startup in this sandbox (likely missing WSL2/Hyper-V virtualization support), so `03-containerizing-with-docker.md`'s Dockerfile/build/run content uses standard, stable, long-unchanged Docker syntax but was NOT execution-verified — disclosed transparently at the top of that lesson. (2) Everything else in Module 20 (joblib/PyTorch packaging, FastAPI with `TestClient`, `logging`, `scipy.stats.ks_2samp` drift detection) WAS fully executed and verified, including a real FastAPI app tested end-to-end with `TestClient` and a real KS-test drift detection demo showing correct true-negative (no drift) and true-positive (drift) results. Packages now installed: `fastapi`, `uvicorn`, `pydantic`, `joblib` (joblib was likely already present via scikit-learn's dependencies).

**ALL 20 MODULES (01-20) ARE NOW COMPLETE.** Per the sequencing decision made after Module 15 (see this file's git history / the project memory file): capstones are authored as a batch now, followed by the three master files. Build, in order: (1) **Capstone 1** (`capstones/capstone01-eda-ml-project/`) — an end-to-end EDA + ML project on a real dataset, applying Modules 06-15 (NumPy/Pandas/cleaning/viz/stats/SQL/classical ML/ensembles); (2) **Capstone 2** (`capstones/capstone02-deep-learning-vision/`) — a deep learning image classifier (CNN), applying Module 16-17; (3) **Capstone 3** (`capstones/capstone03-llm-rag-app/`) — an LLM-powered RAG application, applying Module 19 (note: will have the same no-API-key limitation as Module 19 — handle identically, transparently). Each capstone per the CLAUDE.md spec needs: a real-world scenario, clear requirements, starter guidance, a complete reference solution, and portfolio/interview presentation guidance. After all 3 capstones, build `master-cheatsheet.md`, `master-interview-prep.md`, `master-references.md` at the repo root, consolidating (not just concatenating — organize by category for fast lookup per CLAUDE.md's cheat sheet rules) all 20 modules' cheatsheets/interview prep/references. Update this Course-Author Log after each capstone and after the master files are done — that will mark the entire course project complete.
