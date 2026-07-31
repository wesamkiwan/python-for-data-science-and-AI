# Progress Tracker: Python for Data Science & AI

This file tracks two separate things — don't confuse them:

1. **Content Status** (right-most column) — whether the material for a module has been *written* yet. This is informational only; you don't edit it.
2. **Your checkboxes** (Learning / Exercise / Cheat Sheet / Interview / References) — these are **for you, the learner**, to check off yourself as you actually work through each piece. They start empty and stay empty until you do the work — nobody pre-fills these for you.

**Content Available:** 14/20 modules written (70%)
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

👉 **Content written through:** Module 14 — Unsupervised Learning & Clustering (Phase 3: Machine Learning)
👉 **Next to write:** Module 15 — Ensemble Methods & Advanced ML (XGBoost/LightGBM)

**Resume instructions for next authoring session:** Module 14 is fully written (2 learning files — `01-kmeans-clustering.md`, `02-hierarchical-clustering-and-pca.md` — + cheatsheet + interview + references, all committed and pushed to GitHub; every example executed against scikit-learn 1.9.0/scipy 1.18.0 and verified, including a K-Means-vs-true-species crosstab sanity check on Iris and a PCA variance-preservation check on both Iris (~96% in 2 components) and Wine (~55% in 2 components — correctly predicted in the exercise text to be lower than Iris before verifying). Write Module 15 next in `phase3-machine-learning/module15-ensemble-advanced-ml/` (folder confirmed empty) — this is a 🔴 Advanced module (4h estimate), the last of Phase 3: cover ensemble methods conceptually (bagging vs. boosting), Random Forest (`sklearn.ensemble.RandomForestClassifier/Regressor` — ties back to Module 13c's single-decision-tree overfitting demo, showing how averaging many trees reduces variance), then gradient boosting via XGBoost and/or LightGBM per the roadmap (**IMPORTANT: neither `xgboost` nor `lightgbm` is installed yet** — run `pip install xgboost lightgbm` first), feature importance (`.feature_importances_`, tying back to Module 12c's linear coefficient interpretation lesson for a nice contrast), and hyperparameter tuning basics (`GridSearchCV` or `RandomizedSearchCV`, building on Module 13's cross-validation). After this module, Capstone 1 (End-to-end EDA + ML project) unlocks per the roadmap, and Phase 4 (Deep Learning & AI) begins at Module 16. Build learning file(s) → cheatsheet → interview prep → references → update this module's row to "📗 Content ready" (leave the learner checkboxes empty!) → commit + push → move the two pointers above to Module 16, and flag that Capstone 1 is now unlockable (use judgment on whether to build it immediately or continue to Phase 4 first — ask the user only if genuinely ambiguous).
