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
- [ ] Capstone 1: End-to-end EDA + ML project 🟡 (unlocked — Module 15 done) — 📗 Content ready
- [ ] Capstone 2: Deep learning image classifier (CNN) 🔴 (unlocked — Module 17 done) — ⏳ not written yet
- [ ] Capstone 3: LLM-powered RAG application 🔴 (unlocked — Module 19 done) — ⏳ not written yet

## Master Files
- [ ] `master-cheatsheet.md` (built incrementally, finalized after Module 20) — ⏳ not started
- [ ] `master-interview-prep.md` (built incrementally, finalized after Module 20) — ⏳ not started
- [ ] `master-references.md` (built incrementally, finalized after Module 20) — ⏳ not started

---

## 🛠️ Course-Author Log (for resuming content creation — not a learner section)

👉 **Content written through:** Capstone 1 — End-to-end EDA + ML Project (all 20 modules already complete)
👉 **Next to write:** Capstone 2 — Deep Learning Image Classifier (CNN)

**Resume instructions for next authoring session:** Capstone 1 is fully written in `capstones/capstone01-eda-ml-project/`: `README.md` (scenario + requirements), `generate_dataset.py` (reproducible synthetic customer-churn dataset generator, already run to produce `customer_churn.csv`, 2,008 rows with intentionally injected duplicates/missing values/outliers/inconsistent text casing), `starter-guide.md` (scaffolded questions, no answers), `solution.md` (complete reference solution — cleaning, EDA, leakage-safe pipeline, 3-model comparison via cross-validated AUC, hyperparameter tuning, the precision/recall tradeoff via `class_weight="balanced"`, coefficient interpretation, business writeup), and `portfolio-presentation.md`. Every single code block in `solution.md` was executed end-to-end as one script and its exact output verified (confusion matrices, coefficients, etc. all match precisely) — this was NOT a "write plausible-looking numbers" exercise, the whole pipeline is genuinely reproducible. All committed and pushed to GitHub.

Write Capstone 2 next in `capstones/capstone02-deep-learning-vision/` (folder confirmed to exist per scaffold, currently empty): an end-to-end deep learning image classifier (CNN) project, applying Modules 16-17 (neural network fundamentals, PyTorch and/or TensorFlow/Keras, CNNs, transfer learning, data augmentation). Follow the same package structure as Capstone 1: `README.md` (scenario — e.g., a realistic image classification business problem), a way to obtain/generate the dataset (a real small image dataset like a subset of CIFAR-10/MNIST via `torchvision.datasets`, or a synthetic-but-realistic scenario — decide based on what's genuinely available and downloadable in this environment, both `torchvision` and Keras' built-in datasets are already confirmed working from Module 17), `starter-guide.md`, `solution.md` (fully executed and verified, following Capstone 1's rigor), `portfolio-presentation.md`. Given CNN training can be slow, consider using a reasonably-sized subset (as Module 17b did) so the full solution runs and verifies in reasonable time. Then Capstone 3 (`capstones/capstone03-llm-rag-app/`) — apply Module 19's RAG pipeline to a fuller, more realistic scenario; will have the same no-API-key transparency requirement as Module 19 (use the same local-model-fallback pattern that made Module 19c's RAG pipeline fully verifiable). After all 3 capstones, build the 3 master files (`master-cheatsheet.md`, `master-interview-prep.md`, `master-references.md`) at the repo root, organized by category (not just concatenated) per CLAUDE.md's rules, consolidating all 20 modules. Update this Course-Author Log after each capstone and after the master files — that marks the entire course complete.
