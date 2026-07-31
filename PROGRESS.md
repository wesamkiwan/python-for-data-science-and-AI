# Progress Tracker: Python for Data Science & AI

This file tracks two separate things — don't confuse them:

1. **Content Status** (right-most column) — whether the material for a module has been *written* yet. This is informational only; you don't edit it.
2. **Your checkboxes** (Learning / Exercise / Cheat Sheet / Interview / References) — these are **for you, the learner**, to check off yourself as you actually work through each piece. They start empty and stay empty until you do the work — nobody pre-fills these for you.

**Content Available:** 17/20 modules written (85%)
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

👉 **Content written through:** Module 17 — Computer Vision (CNNs) (Phase 4: Deep Learning & AI)
👉 **Next to write:** Module 18 — NLP & Transformers

**Resume instructions for next authoring session:** Module 17 is fully written (3 learning files — `01-cnn-fundamentals.md`, `02-building-cnns.md`, `03-transfer-learning-and-augmentation.md` — + cheatsheet + interview + references, all committed and pushed to GitHub; every example executed and verified in both PyTorch (main env) and Keras (`/c/tf_venv312/Scripts/python.exe`), including a real MNIST CNN in both frameworks and real transfer learning with `resnet18`/`MobileNetV2` showing frozen-vs-trainable parameter counts. `torchvision` is now installed in the main env. **The `C:\tf_venv312` TensorFlow workaround from Module 16 is still needed and still works** — re-verify Python 3.14 TF support before dropping it. Write Module 18 next in `phase4-deep-learning-and-ai/module18-nlp-transformers/` (folder confirmed empty) — per confirmed course decisions this still needs both PyTorch and TensorFlow where relevant, though NLP work will lean heavily on the `transformers` library (Hugging Face) which sits on top of either backend: cover text preprocessing for deep learning (tokenization, embeddings — contrast with Module 18/19's classical NLP if any classical bag-of-words/TF-IDF was covered elsewhere, otherwise introduce fresh), the Transformer architecture conceptually (attention mechanism, encoder/decoder, tying back to Module 16a's forward-pass framing), and using pretrained transformer models via Hugging Face's `transformers` library (`pip install transformers` — not yet installed) for a concrete task like sentiment classification or text classification — this is effectively "transfer learning for text," a nice explicit callback to Module 17c. Given the 5h estimate, likely 3-4 learning files. Build learning file(s) → cheatsheet → interview prep → references → update this module's row to "📗 Content ready" (leave the learner checkboxes empty!) → commit + push → move the two pointers above to Module 19.
