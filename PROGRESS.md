# Progress Tracker: Python for Data Science & AI

This file tracks two separate things — don't confuse them:

1. **Content Status** (right-most column) — whether the material for a module has been *written* yet. This is informational only; you don't edit it.
2. **Your checkboxes** (Learning / Exercise / Cheat Sheet / Interview / References) — these are **for you, the learner**, to check off yourself as you actually work through each piece. They start empty and stay empty until you do the work — nobody pre-fills these for you.

**Content Available:** 12/20 modules written (60%)
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
| 13 | Feature Engineering & Model Evaluation | 🟡 | 4h | [ ] | [ ] | [ ] | [ ] | [ ] | ⏳ Not written yet |
| 14 | Unsupervised Learning & Clustering | 🟡 | 3h | [ ] | [ ] | [ ] | [ ] | [ ] | ⏳ Not written yet |
| 15 | Ensemble Methods & Advanced ML | 🔴 | 4h | [ ] | [ ] | [ ] | [ ] | [ ] | ⏳ Not written yet |
| 16 | Deep Learning Foundations (PyTorch + TF/Keras) | 🔴 | 6h | [ ] | [ ] | [ ] | [ ] | [ ] | ⏳ Not written yet |
| 17 | Computer Vision (CNNs) | 🔴 | 4h | [ ] | [ ] | [ ] | [ ] | [ ] | ⏳ Not written yet |
| 18 | NLP & Transformers | 🔴 | 5h | [ ] | [ ] | [ ] | [ ] | [ ] | ⏳ Not written yet |
| 19 | Generative AI & LLMs | 🔴 | 5h | [ ] | [ ] | [ ] | [ ] | [ ] | ⏳ Not written yet |
| 20 | MLOps & Deployment | 🔴 | 5h | [ ] | [ ] | [ ] | [ ] | [ ] | ⏳ Not written yet |

## Capstone Projects
- [ ] Capstone 1: End-to-end EDA + ML project 🟡 (unlocks after Module 15) — ⏳ not written yet
- [ ] Capstone 2: Deep learning image classifier (CNN) 🔴 (unlocks after Module 17) — ⏳ not written yet
- [ ] Capstone 3: LLM-powered RAG application 🔴 (unlocks after Module 19) — ⏳ not written yet

## Master Files
- [ ] `master-cheatsheet.md` (built incrementally, finalized after Module 20) — ⏳ not started
- [ ] `master-interview-prep.md` (built incrementally, finalized after Module 20) — ⏳ not started
- [ ] `master-references.md` (built incrementally, finalized after Module 20) — ⏳ not started

---

## 🛠️ Course-Author Log (for resuming content creation — not a learner section)

👉 **Content written through:** Module 12 — ML Foundations (scikit-learn) (Phase 3: Machine Learning)
👉 **Next to write:** Module 13 — Feature Engineering & Model Evaluation

**Resume instructions for next authoring session:** Module 12 is fully written (3 learning files — `01-supervised-learning-basics.md`, `02-classification-with-sklearn.md`, `03-regression-with-sklearn.md` — + cheatsheet + interview + references, all committed and pushed to GitHub; every example executed against scikit-learn 1.9.0 and verified, including catching a real `ConvergenceWarning` on the Wine dataset's `LogisticRegression` exercise and correcting the lesson text — raising `max_iter` alone does NOT fix it, feature scaling does, and the lesson now says so honestly rather than claiming a fix that doesn't actually work). `fetch_california_housing()` downloads on first use (then caches) — unlike `load_iris`/`load_wine` which are bundled; this was noted in the lesson. `scikit-learn` is now installed (1.9.0). Write Module 13 next in `phase3-machine-learning/module13-feature-engineering-evaluation/` (folder confirmed empty): cover feature scaling (`StandardScaler`/`MinMaxScaler` — directly resolves the Module 12b convergence warning, close that loop explicitly), encoding categorical variables (`OneHotEncoder`, `pd.get_dummies` from Module 07), handling the train/test-split-before-preprocessing rule properly via `Pipeline`/`ColumnTransformer` (to avoid data leakage, flagged as a risk back in Module 12a), cross-validation (`cross_val_score`, k-fold), and overfitting/underfitting/bias-variance tradeoff (tie back to Module 12's train-vs-test R² gap scenario). This is a meaty module (4h estimate) — likely 3 learning files. Build learning file(s) → cheatsheet → interview prep → references → update this module's row to "📗 Content ready" (leave the learner checkboxes empty!) → commit + push → move the two pointers above to Module 14.
