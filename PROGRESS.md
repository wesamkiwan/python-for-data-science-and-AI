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
- [ ] Capstone 3: LLM-powered RAG application 🔴 (unlocked — Module 19 done) — ⏳ not written yet

## Master Files
- [ ] `master-cheatsheet.md` (built incrementally, finalized after Module 20) — ⏳ not started
- [ ] `master-interview-prep.md` (built incrementally, finalized after Module 20) — ⏳ not started
- [ ] `master-references.md` (built incrementally, finalized after Module 20) — ⏳ not started

---

## 🛠️ Course-Author Log (for resuming content creation — not a learner section)

👉 **Content written through:** Capstone 2 — Deep Learning Image Classifier (CNN) (all 20 modules already complete)
👉 **Next to write:** Capstone 3 — LLM-Powered RAG Application

**Resume instructions for next authoring session:** Capstone 2 is fully written in `capstones/capstone02-deep-learning-vision/`: `README.md`, `starter-guide.md`, `solution.md`, `portfolio-presentation.md`. Scenario: automated product image categorization for a clothing retailer (ThreadLine), using **Fashion-MNIST** (not CIFAR-10 — CIFAR-10's source server at cs.toronto.edu has an EXPIRED SSL CERTIFICATE as of this writing, confirmed failing in both `torchvision.datasets.CIFAR10` and `keras.datasets.cifar10.load_data()` with `CERTIFICATE_VERIFY_FAILED`; re-check this before assuming it's still broken, but don't just disable SSL verification to work around it). Fashion-MNIST downloads fine and is thematically perfect (built by an actual retailer, Zalando, for this exact use case). Every code block was executed and verified: baseline CNN reaches 87.55% test accuracy on an 8k-image subset with a detailed per-class breakdown (Shirt is the weak class at F1=0.68, confused with T-shirt/Coat/Pullover); the data augmentation comparison is a genuinely honest, non-cherry-picked finding — augmentation reduced the train/test overfitting gap (0.0548→0.0350) but did NOT improve raw test accuracy (0.8965→0.8860) at this training budget, and the solution explicitly discusses why that's still a real, useful finding rather than forcing a "clean win" narrative. All committed and pushed to GitHub.

Write Capstone 3 next in `capstones/capstone03-llm-rag-app/` (folder confirmed to exist per scaffold, currently empty): an LLM-powered RAG application, applying Module 19 end to end. **Same no-API-key constraint as Module 19 applies here** — no Anthropic/OpenAI key is available in this sandbox. Use the exact same pattern that worked for Module 19c: build a fully local, fully execution-verified RAG pipeline (sentence-transformers embeddings + FAISS retrieval via LangChain + a local generation model), while also showing the "swap in a real LLM API" code path clearly labeled as unverified-by-execution (matching current SDK syntax, checked via `inspect.signature()`). Consider a concrete scenario (e.g., a "chat with your company's documentation/FAQ" internal tool) and build a small, realistic corpus of documents (synthetic but realistic, similar spirit to Capstone 1's synthetic-but-realistic dataset) for the RAG pipeline to retrieve from. Follow the same package structure: `README.md`, `starter-guide.md`, `solution.md`, `portfolio-presentation.md`.

After Capstone 3, build the 3 master files (`master-cheatsheet.md`, `master-interview-prep.md`, `master-references.md`) at the repo root, organized by category (not just concatenated) per CLAUDE.md's rules, consolidating all 20 modules' cheatsheets/interview prep/references respectively. Update this Course-Author Log after Capstone 3 and again after the master files are done — that marks the ENTIRE course project 100% complete.
