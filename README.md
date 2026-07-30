# Python for Data Science & AI — Zero to Hero

A complete, production-ready learning path that takes you from **absolute beginner** to **job-ready Data Scientist / AI practitioner**, using modern, industry-standard tools.

## 🎯 What You'll Be Able to Do

By the end of this course, you will be able to:

- Write clean, idiomatic Python and design object-oriented programs
- Manipulate, clean, and analyze real-world data with NumPy, Pandas, and SQL
- Build clear, publication-quality visualizations and full exploratory data analyses (EDA)
- Train, evaluate, and tune classical machine learning models with scikit-learn
- Build and train deep learning models with **both PyTorch and TensorFlow/Keras**
- Build computer vision (CNN) and NLP/transformer-based models
- Work with modern Generative AI: embeddings, prompting, and Retrieval-Augmented Generation (RAG)
- Package, deploy, and monitor a model in production (Docker, FastAPI, MLOps basics)
- Walk into a data science / ML engineering interview and confidently answer conceptual, coding, and system-design questions
- Present portfolio-worthy capstone projects that mirror real job tasks

## ✅ Prerequisites

**None.** This course assumes zero prior programming experience. If you already know some Python, feel free to skim Phase 1 and jump to Phase 2 (Module 06).

Everything you need to install is covered in the **Environment Setup** section below and in `phase1-python-foundations/module05-tooling-environments/`.

## 🗺️ Course Roadmap

| Phase | Module | Difficulty | Est. Time |
|-------|--------|:----------:|:---------:|
| 1 — Python Foundations | 01. Python Fundamentals | 🟢 | 4h |
| 1 | 02. Functions, Modules & Error Handling | 🟢 | 3h |
| 1 | 03. Object-Oriented Programming (OOP) | 🟢 | 3h |
| 1 | 04. File I/O, JSON/CSV & Working with APIs | 🟢 | 2h |
| 1 | 05. Python Tooling & Environments (venv, pip, git) | 🟢 | 2h |
| 2 — Data Science Core | 06. NumPy Fundamentals | 🟡 | 3h |
| 2 | 07. Pandas for Data Manipulation | 🟡 | 5h |
| 2 | 08. Data Cleaning & Wrangling | 🟡 | 4h |
| 2 | 09. Data Visualization (Matplotlib, Seaborn, Plotly) | 🟡 | 4h |
| 2 | 10. Exploratory Data Analysis & Statistics | 🟡 | 4h |
| 2 | 11. SQL for Data Scientists | 🟡 | 3h |
| 3 — Machine Learning | 12. ML Foundations (scikit-learn) | 🟡 | 5h |
| 3 | 13. Feature Engineering & Model Evaluation | 🟡 | 4h |
| 3 | 14. Unsupervised Learning & Clustering | 🟡 | 3h |
| 3 | 15. Ensemble Methods & Advanced ML (XGBoost/LightGBM) | 🔴 | 4h |
| 4 — Deep Learning & AI | 16. Deep Learning Foundations (PyTorch + TensorFlow/Keras) | 🔴 | 6h |
| 4 | 17. Computer Vision (CNNs) | 🔴 | 4h |
| 4 | 18. NLP & Transformers | 🔴 | 5h |
| 4 | 19. Generative AI & LLMs (prompting, embeddings, RAG) | 🔴 | 5h |
| 5 — Deployment | 20. MLOps & Deployment (Docker, FastAPI, monitoring) | 🔴 | 5h |

**Total estimated time: ~78 hours**

### 🏆 Capstone Projects
- [ ] Capstone 1: End-to-end EDA + ML project on a real dataset 🟡
- [ ] Capstone 2: Deep learning image classifier (CNN) 🔴
- [ ] Capstone 3: LLM-powered RAG application 🔴

👉 **Track your progress in [`PROGRESS.md`](PROGRESS.md)** — it's updated after every module and always shows exactly where you left off.

## 🛠️ Environment Setup

1. **Install Python 3.11+**
   - Windows: download from [python.org/downloads](https://www.python.org/downloads/) and check "Add Python to PATH" during install.
   - Verify: open a terminal and run `python --version`.
2. **Install a code editor**: [VS Code](https://code.visualstudio.com/) (free, industry-standard) + the official Python extension.
3. **Create a virtual environment** (isolates project dependencies — covered in depth in Module 05):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```
4. **Install the core data science stack** (you'll install specific libraries per-module, but this covers Phase 2-3):
   ```bash
   pip install numpy pandas matplotlib seaborn plotly scikit-learn jupyter
   ```
5. **Deep learning stack** (needed from Module 16 onward):
   ```bash
   pip install torch tensorflow
   ```

💡 **Tip:** Don't install everything up front. Each module tells you exactly what to `pip install` when you need it — this mirrors how you'll actually work on the job.

## 📂 Repository Structure

```
python-for-data-science-and-ai/
├── README.md                          # you are here
├── PROGRESS.md                        # trackable checklist — always up to date
├── phase1-python-foundations/
│   └── module01-python-fundamentals/
│       ├── 01-getting-started.md
│       ├── 02-data-types-and-operators.md
│       ├── 03-control-flow-and-collections.md
│       ├── module01-cheatsheet.md
│       ├── module01-interview.md
│       └── module01-references.md
│   └── ... (modules 02-05)
├── phase2-data-science-core/           # modules 06-11
├── phase3-machine-learning/            # modules 12-15
├── phase4-deep-learning-and-ai/        # modules 16-19
├── phase5-deployment/                  # module 20
├── capstones/                          # 3 portfolio projects
├── master-cheatsheet.md
├── master-interview-prep.md
└── master-references.md
```

## 📖 How to Use This Course

1. Work through modules **in order** — each builds on the last.
2. For each module: read the learning file(s) → do the hands-on exercise → check your solution → skim the cheat sheet → review interview prep questions.
3. Tick off checkboxes in `PROGRESS.md` as you complete each piece.
4. When you finish a phase, attempt the related capstone before moving to the next phase.
5. Use the **master cheat sheet** as your on-the-job quick reference once you're working.

---
👉 **Start here:** [`phase1-python-foundations/module01-python-fundamentals/01-getting-started.md`](phase1-python-foundations/module01-python-fundamentals/01-getting-started.md)
