# Progress Tracker: Python for Data Science & AI

This file tracks two separate things — don't confuse them:

1. **Content Status** (right-most column) — whether the material for a module has been *written* yet. This is informational only; you don't edit it.
2. **Your checkboxes** (Learning / Exercise / Cheat Sheet / Interview / References) — these are **for you, the learner**, to check off yourself as you actually work through each piece. They start empty and stay empty until you do the work — nobody pre-fills these for you.

**Content Available:** 19/20 modules written (95%)
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

👉 **Content written through:** Module 19 — Generative AI & LLMs (Phase 4: Deep Learning & AI) — 🎉 **Phase 4 complete!**
👉 **Next to write:** Module 20 — MLOps & Deployment (Docker, FastAPI, monitoring) — final content module, start of Phase 5

**Resume instructions for next authoring session:** Module 19 is fully written (3 learning files — `01-prompting-and-llm-apis.md`, `02-embeddings-and-semantic-search.md`, `03-building-a-rag-pipeline.md` — + cheatsheet + interview + references, all committed and pushed to GitHub). **Important honesty note preserved in the lesson itself:** no LLM API key (Anthropic/OpenAI) is available in this authoring environment, so the live-API-call code in `01-prompting-and-llm-apis.md` and the "real LLM" section of `03-building-a-rag-pipeline.md` was written to match current, verified-correct SDK syntax (confirmed via `inspect.signature()` and checking exception classes exist — `client.messages.create(model=, max_tokens=, temperature=, system=, messages=)`, `anthropic.RateLimitError`, `anthropic.APIError` all confirmed real) but was NOT execution-verified end-to-end like everything else in this course — this was disclosed transparently to the learner at the top of Module 19a rather than silently breaking the course's verification standard. To compensate, the RAG pipeline (Module 19c) also includes a fully local, fully execution-verified alternative using `distilgpt2` for generation (its weak, sometimes-hallucinated answers were left in the lesson honestly, since they concretely demonstrate why a production RAG system needs a real LLM). Packages now installed: `anthropic`, `sentence-transformers`, `faiss-cpu`, `langchain`, `langchain-community`, `langchain-huggingface`, `langchain-text-splitters`. **Another gotcha found:** `langchain.text_splitter` no longer exists — text splitters moved to the standalone `langchain_text_splitters` package; `langchain-community`'s `FAISS`/`HuggingFaceEmbeddings` show a deprecation warning (community package being sunset in favor of standalone integration packages) but still work and were used as-is. This completes **all of Phase 4** (Modules 16-19) and the course now has only ONE content module left. Write Module 20 next in `phase5-deployment/module20-mlops-deployment/` (folder confirmed empty): cover packaging a model for deployment (`pickle`/`joblib` for scikit-learn models, saving PyTorch/Keras models), building a REST API around a model with FastAPI (`pip install fastapi uvicorn` — not yet installed; Docker IS available on this machine, version 29.6.1, confirmed via `docker --version`), containerizing the API with a Dockerfile, and basic production monitoring concepts (logging predictions, tracking model/data drift conceptually, tying back to Module 10's statistical testing for detecting drift). Given the 5h estimate, likely 3-4 learning files. This is the FINAL module (01-20) — after this, update `README.md`'s roadmap checkboxes if any exist, then move to building the 3 capstones (in `capstones/`) as a batch per the earlier sequencing decision, then `master-cheatsheet.md`/`master-interview-prep.md`/`master-references.md` at the repo root, consolidating all 20 modules' cheatsheets/interview prep/references. Build learning file(s) → cheatsheet → interview prep → references → update this module's row to "📗 Content ready" (leave the learner checkboxes empty!) → commit + push → update the Course-Author Log to point at "Capstone 1" as next, noting Modules 01-20 are 100% complete.
