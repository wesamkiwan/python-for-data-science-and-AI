# Progress Tracker: Python for Data Science & AI

This file tracks two separate things — don't confuse them:

1. **Content Status** (right-most column) — whether the material for a module has been *written* yet. This is informational only; you don't edit it.
2. **Your checkboxes** (Learning / Exercise / Cheat Sheet / Interview / References) — these are **for you, the learner**, to check off yourself as you actually work through each piece. They start empty and stay empty until you do the work — nobody pre-fills these for you.

**Content Available:** 15/20 modules written (75%)
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

👉 **Content written through:** Module 15 — Ensemble Methods & Advanced ML (Phase 3: Machine Learning) — 🎉 **Phase 3 complete!**
👉 **Next to write:** Module 16 — Deep Learning Foundations (PyTorch + TensorFlow/Keras) — start of Phase 4

**Resume instructions for next authoring session:** Module 15 is fully written (3 learning files — `01-random-forests-and-bagging.md`, `02-gradient-boosting.md`, `03-hyperparameter-tuning.md` — + cheatsheet + interview + references, all committed and pushed to GitHub; every example executed against scikit-learn 1.9.0, xgboost 3.3.0, and lightgbm 4.7.0, verified against documented output — including reusing Module 13c's exact synthetic overfitting dataset to concretely show Random Forest (test 0.7667) and XGBoost (test 0.8167) both beating a single decision tree (test 0.6333), closing that loop with real numbers). This completes **all of Phase 3** (Modules 12-15). **Decision made without asking the user (low-ambiguity, matches the original founding-session task list order of "Modules 01-20, then 3 capstones, then master files"): capstones will be authored as a batch AFTER all 20 modules are done, not interleaved after each phase** — so proceed directly to Module 16 next, not Capstone 1, despite Capstone 1 now being conceptually "unlockable" per the roadmap. Write Module 16 next in `phase4-deep-learning-and-ai/module16-deep-learning-foundations/` (folder confirmed empty) — this is the biggest module in the course (6h estimate, 🔴 Advanced) and per confirmed course-planning decisions must cover **both PyTorch and TensorFlow/Keras**, not just one: neural network fundamentals (neurons/layers/weights/activation functions/forward pass), backpropagation and gradient descent conceptually, building a simple feedforward network in PyTorch (`torch.nn`, `nn.Module`, training loop) AND the equivalent in TensorFlow/Keras (`tf.keras.Sequential`, `.compile()`/`.fit()`), tying the underlying concepts (loss functions, optimizers, epochs) explicitly back to Module 12's `.fit()`/`.predict()` pattern and Module 13's overfitting/train-test discipline. **IMPORTANT: neither `torch` nor `tensorflow` is installed yet** — run `pip install torch tensorflow` first (may take a while / large download; note Windows-specific install nuances if any arise). Given the scope, expect 4-5 learning files (e.g., neural net fundamentals / PyTorch basics / TensorFlow-Keras basics / training loop deep dive). Build learning file(s) → cheatsheet → interview prep → references → update this module's row to "📗 Content ready" (leave the learner checkboxes empty!) → commit + push → move the two pointers above to Module 17.
