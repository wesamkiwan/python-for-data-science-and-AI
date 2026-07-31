# Progress Tracker: Python for Data Science & AI

This file tracks two separate things — don't confuse them:

1. **Content Status** (right-most column) — whether the material for a module has been *written* yet. This is informational only; you don't edit it.
2. **Your checkboxes** (Learning / Exercise / Cheat Sheet / Interview / References) — these are **for you, the learner**, to check off yourself as you actually work through each piece. They start empty and stay empty until you do the work — nobody pre-fills these for you.

**Content Available:** 7/20 modules written (35%)
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
| 08 | Data Cleaning & Wrangling | 🟡 | 4h | [ ] | [ ] | [ ] | [ ] | [ ] | ⏳ Not written yet |
| 09 | Data Visualization | 🟡 | 4h | [ ] | [ ] | [ ] | [ ] | [ ] | ⏳ Not written yet |
| 10 | EDA & Statistics | 🟡 | 4h | [ ] | [ ] | [ ] | [ ] | [ ] | ⏳ Not written yet |
| 11 | SQL for Data Scientists | 🟡 | 3h | [ ] | [ ] | [ ] | [ ] | [ ] | ⏳ Not written yet |
| 12 | ML Foundations (scikit-learn) | 🟡 | 5h | [ ] | [ ] | [ ] | [ ] | [ ] | ⏳ Not written yet |
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

👉 **Content written through:** Module 07 — Pandas for Data Manipulation (Phase 2: Data Science Core)
👉 **Next to write:** Module 08 — Data Cleaning & Wrangling

**Resume instructions for next authoring session:** Module 07 is fully written (4 learning files — `01-series-and-dataframes.md`, `02-selection-and-filtering.md`, `03-column-operations-and-sorting.md`, `04-groupby-and-merging.md` — + cheatsheet + interview + references, all committed and pushed to GitHub; every code example was executed against pandas 3.0.x and verified, including a note that pandas 3.0+ shows a dedicated `str` dtype for text columns instead of the `object` dtype older tutorials reference — flagged explicitly in the lesson so learners aren't confused by the mismatch with older material they find online). Write Module 08 next in `phase2-data-science-core/module08-data-cleaning/` (folder confirmed empty, ready to use): cover detecting/handling missing data (`.isna()`, `.dropna()`, `.fillna()`), detecting/removing duplicates (`.duplicated()`, `.drop_duplicates()`), fixing data types (`.astype()`, `pd.to_numeric(errors="coerce")`, `pd.to_datetime()`), string cleaning (`.str` accessor methods — `.strip()`, `.lower()`, `.replace()`), and detecting/handling outliers (IQR method, z-score). Frame this module around the reality that real-world data is messy by default — tie back to Module 04's `errors="coerce"` mention and Module 02's error-handling instincts. Build learning file(s) → cheatsheet → interview prep → references → update this module's row to "📗 Content ready" (leave the learner checkboxes empty!) → commit + push → move the two pointers above to Module 09.
