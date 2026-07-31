# Progress Tracker: Python for Data Science & AI

This file tracks two separate things — don't confuse them:

1. **Content Status** (right-most column) — whether the material for a module has been *written* yet. This is informational only; you don't edit it.
2. **Your checkboxes** (Learning / Exercise / Cheat Sheet / Interview / References) — these are **for you, the learner**, to check off yourself as you actually work through each piece. They start empty and stay empty until you do the work — nobody pre-fills these for you.

**Content Available:** 18/20 modules written (90%)
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

👉 **Content written through:** Module 18 — NLP & Transformers (Phase 4: Deep Learning & AI)
👉 **Next to write:** Module 19 — Generative AI & LLMs (prompting, embeddings, RAG)

**Resume instructions for next authoring session:** Module 18 is fully written (3 learning files — `01-text-preprocessing-and-embeddings.md`, `02-transformer-architecture.md`, `03-using-pretrained-transformers.md` — + cheatsheet + interview + references, all committed and pushed to GitHub; every example executed and verified, including a real manual self-attention computation in NumPy and real Hugging Face `pipeline()` calls (sentiment-analysis, zero-shot-classification, ner). `transformers` (5.14.1) is now installed. **IMPORTANT gotcha found and fixed:** this transformers version's `pipeline()` task registry does NOT support `"summarization"`/`"translation"`/`"text2text-generation"` at all (raises `KeyError: Unknown task`) — that content was removed from the lesson rather than left broken; also `pipeline("ner", grouped_entities=True)` fails in this version — the correct current parameter is `aggregation_strategy="simple"`, used throughout instead. If a future session re-tests any pipeline task, verify against `pipeline(...)`'s actual error message / the installed version's supported task list before assuming older tutorial syntax still works. Write Module 19 next in `phase4-deep-learning-and-ai/module19-genai-llms/` (folder confirmed empty) — this is the module where the confirmed **LangChain decision** applies (see this memory file's earlier note): cover prompting/prompt engineering basics, calling an LLM API directly (likely via the `anthropic` or `openai` Python SDK — pick one, note it needs an API key which this environment likely doesn't have; may need to either mock/describe expected output honestly if no key is available, or ask the user for one), embeddings for semantic search (`sentence-transformers` or similar, tying back to Module 18a's embeddings concept), and building a basic RAG (Retrieval-Augmented Generation) pipeline using LangChain, explicitly setting up Capstone 3 (LLM-powered RAG application). This is the last content module before Module 20 (MLOps & Deployment) and marks the point Capstone 3 becomes conceptually relevant (though capstones are still deferred as a batch per the earlier sequencing decision). Given the 5h estimate and this module's real external-dependency complexity (API keys, possibly no internet-callable LLM in this sandboxed environment), verify carefully what's actually runnable before claiming "verified" — if live API calls aren't possible, say so explicitly rather than fabricating output. Build learning file(s) → cheatsheet → interview prep → references → update this module's row to "📗 Content ready" (leave the learner checkboxes empty!) → commit + push → move the two pointers above to Module 20.
