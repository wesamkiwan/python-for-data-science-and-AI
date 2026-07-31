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
- [ ] Capstone 2: Deep learning image classifier (CNN) 🔴 (unlocked — Module 17 done) — 📗 Content ready
- [ ] Capstone 3: LLM-powered RAG application 🔴 (unlocked — Module 19 done) — 📗 Content ready

## Master Files
- [ ] `master-cheatsheet.md` (built incrementally, finalized after Module 20) — ⏳ not started
- [ ] `master-interview-prep.md` (built incrementally, finalized after Module 20) — ⏳ not started
- [ ] `master-references.md` (built incrementally, finalized after Module 20) — ⏳ not started

---

## 🛠️ Course-Author Log (for resuming content creation — not a learner section)

👉 **Content written through:** Capstone 3 — LLM-Powered RAG Application (all 20 modules + all 3 capstones complete!)
👉 **Next to write:** Master files (`master-cheatsheet.md`, `master-interview-prep.md`, `master-references.md`) — the FINAL remaining piece of this entire course.

**Resume instructions for next authoring session:** Capstone 3 is fully written in `capstones/capstone03-llm-rag-app/`: `README.md`, `starter-guide.md`, `solution.md`, `portfolio-presentation.md`. Scenario: an internal HR/IT helpdesk assistant for a fictional company (Alderbrook Corp), built on a synthetic-but-realistic 10-document policy knowledge base. Applies Module 19 end to end (embeddings, FAISS retrieval via LangChain, prompt engineering) plus a genuine enhancement beyond Module 19c: an empirically-measured similarity-score relevance threshold (in-scope questions scored <1.3, out-of-scope scored >1.8 in testing, threshold set at 1.5) that reliably detects out-of-scope questions in code, before generation even runs — more robust than relying on a prompt instruction alone. Same no-API-key transparency as Module 19/Capstone constraint: the local-model (distilgpt2) generation path was fully executed and verified (correctly retrieves context, but produces an incoherent/wrong answer — an expected, honestly-reported limitation of a small model), and the "real LLM API" swap-in code is clearly labeled unverified-by-execution. **One inconsistency was caught and fixed during authoring:** an early test used a reduced 3-document knowledge base for a quick sanity check, and its output was initially, incorrectly pasted into the "Step 5" section meant to reflect the full 10-document knowledge base — this was caught by re-running the full pipeline end-to-end as a final check and the solution was corrected with the actual matching output. All committed and pushed to GitHub.

**ALL 20 MODULES AND ALL 3 CAPSTONES ARE NOW COMPLETE.** The only remaining work for the entire course is the 3 master files at the repo root: `master-cheatsheet.md`, `master-interview-prep.md`, `master-references.md`. Per CLAUDE.md's rules, these must be genuinely consolidated and organized by category/task for fast lookup — NOT simply concatenated module-by-module. Suggested approach: read through all 20 modules' `moduleNN-cheatsheet.md` files and group content by theme (e.g., "Environment & Tooling," "NumPy/Pandas Core," "Visualization," "Classical ML," "Deep Learning," "NLP/LLMs," "Deployment") rather than by module number; same category-based approach for `master-interview-prep.md` (grouped by difficulty 🟢/🟡/🔴 within topic areas, per the interview prep rules in CLAUDE.md) and `master-references.md` (grouped by resource type — YouTube, docs, tutorials, courses, books, communities — per the reference rules, deduplicating resources that appear in multiple modules, e.g. StatQuest/Real Python/Kaggle Learn show up repeatedly). This is a synthesis/organization task, not a code-verification task — no new code needs testing, just careful consolidation of already-written, already-verified content. Once done, update this Course-Author Log one final time to record the ENTIRE course (20 modules + 3 capstones + 3 master files) as 100% complete, and update the "Content Available" summary line and any remaining checkboxes accordingly.
