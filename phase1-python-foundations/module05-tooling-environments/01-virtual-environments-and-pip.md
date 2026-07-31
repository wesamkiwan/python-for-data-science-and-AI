# Module 05a: Virtual Environments & pip

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 45min | **Prerequisites:** [Module 04 — File I/O, JSON/CSV & Working with APIs](../module04-file-io-apis/03-working-with-apis.md)

## 🎯 Learning Objectives
- [ ] Explain why virtual environments exist and what problem they solve
- [ ] Create, activate, and deactivate a virtual environment with `venv`
- [ ] Install, upgrade, and uninstall packages with `pip`
- [ ] Generate and use a `requirements.txt` file to reproduce an environment

---

## Module Goal

Learn to properly isolate a Python project's dependencies using **virtual environments**, and manage the packages inside them with **pip**. This is boring-sounding but absolutely essential — it's the difference between "works on my machine" chaos and a project anyone (including future you) can reliably set up and run.

## Why This Matters on the Job

Every real Python project — a data science notebook, a production ML pipeline, a web app — depends on specific versions of specific packages. Without isolation, installing one project's dependencies can silently break another project on the same machine. Every job posting that mentions Python assumes you already know this workflow; it's assumed baseline knowledge, not something taught in the interview.

---

## The Problem: Why Isolate Dependencies?

Imagine you have two projects on your computer:
- **Project A** needs `pandas` version 1.5
- **Project B** needs `pandas` version 2.1

If you install packages **globally** (system-wide), there's only one Python installation and one set of installed packages — you can't have both versions of `pandas` installed at once. Installing Project B's `pandas` would silently break Project A.

💡 **Analogy:** A virtual environment is like giving each project its own separate toolbox, instead of one shared toolbox for your entire house. Project A gets its own `pandas` in its own toolbox; Project B gets a completely different `pandas` in its own toolbox. Neither project's tools interfere with the other's.

A **virtual environment** solves this by creating an isolated, self-contained Python installation (with its own `pip` and its own installed packages) for each individual project.

## Creating a Virtual Environment with `venv`

`venv` is Python's built-in tool for creating virtual environments — no extra installation needed.

```bash
# Navigate to your project folder first
cd my_project

# Create a virtual environment named "venv" (the name is convention, not required)
python -m venv venv
```

**How it works:** `python -m venv venv` runs the built-in `venv` module, creating a new folder named `venv/` containing a private copy of the Python interpreter and an empty `site-packages` directory ready for your project's own packages.

⚠️ **Warning:** Never commit the `venv/` folder to git — it's large, platform-specific, and fully reproducible from `requirements.txt` (covered below). Always add it to `.gitignore` (covered in the next lesson).

## Activating and Deactivating

Creating the environment isn't enough — you must **activate** it so your terminal actually uses its isolated Python and pip instead of the global ones.

```bash
# Windows (PowerShell)
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

Once activated, your terminal prompt shows the environment name, e.g. `(venv) C:\my_project>` — this is your visual confirmation it's active.

```bash
# Deactivate when you're done (returns to the global Python)
deactivate
```

⚠️ **Warning:** Forgetting to activate your virtual environment before running `pip install` is one of the most common beginner mistakes — the package silently installs globally instead, and your project still can't find it when you actually run your script inside the (unactivated) environment.

✅ **Best Practice:** Activate your project's virtual environment every time you open a terminal to work on it — this should become an automatic habit, like unlocking your front door before walking in.

## Installing Packages with `pip`

With the virtual environment **activated**:

```bash
pip install pandas               # installs the latest version
pip install pandas==2.1.0          # installs a specific version
pip install pandas numpy scikit-learn   # installs multiple packages at once
pip install --upgrade pandas          # upgrades an already-installed package
pip uninstall pandas                    # removes a package
```

Check what's currently installed:

```bash
pip list                  # lists every installed package and its version
pip show pandas             # shows detailed info about one specific package
```

## `requirements.txt`: Reproducing an Environment

A `requirements.txt` file lists every package (and version) your project needs, so anyone — a teammate, a server, future you on a different computer — can recreate the exact same environment.

**Generating it from your current environment:**

```bash
pip freeze > requirements.txt
```

This produces a file like:
```
numpy==1.26.4
pandas==2.1.4
requests==2.31.0
```

**Installing from it (on a fresh machine/environment):**

```bash
pip install -r requirements.txt
```

**How it works:** `pip freeze` lists every installed package with its *exact* version, in the standard `package==version` format. `-r requirements.txt` tells `pip install` to read that file and install everything listed, rather than installing one package by name.

🎯 **On the job:** This is the very first thing you do when you clone a teammate's project or set up a new environment: `python -m venv venv`, activate it, then `pip install -r requirements.txt` — three commands that recreate their exact working setup on your machine.

✅ **Best Practice:** Every real Python project should have a `requirements.txt` committed to its repository (never the `venv/` folder itself) — this is the standard, expected way to document a project's dependencies.

---

## Hands-On Exercise

**Task:**
1. Create a new folder called `venv_practice` and navigate into it in your terminal.
2. Create a virtual environment named `venv` inside it.
3. Activate it, and confirm your terminal prompt shows `(venv)`.
4. Install `requests` and `pandas` inside the activated environment.
5. Generate a `requirements.txt` file with `pip freeze`.
6. Deactivate the environment, then reactivate it and confirm `pip list` still shows your installed packages.

<details>
<summary>✅ Click to see the solution</summary>

```bash
mkdir venv_practice
cd venv_practice

python -m venv venv

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install requests pandas

pip freeze > requirements.txt

deactivate

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip list
```

**Expected outcome:** After activating, your prompt shows `(venv)`. `pip list` shows `requests`, `pandas`, and their dependencies (e.g. `numpy`, `certifi`), and `requirements.txt` contains the same packages with pinned versions.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Installing packages without activating the venv first | Always confirm `(venv)` shows in your prompt before running `pip install` |
| Committing the `venv/` folder to git | Add it to `.gitignore`; commit `requirements.txt` instead |
| Forgetting to update `requirements.txt` after installing new packages | Re-run `pip freeze > requirements.txt` whenever you add/change dependencies |
| One global environment shared across all projects | Create a fresh virtual environment per project |
| Confusing "created" with "activated" | `python -m venv venv` only creates it — you must run the activate command every session |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand why virtual environments prevent dependency conflicts
- [ ] Can create, activate, and deactivate a virtual environment with `venv`
- [ ] Can install, upgrade, and uninstall packages with `pip`
- [ ] Can generate and install from a `requirements.txt` file
- [ ] Completed the `venv_practice` exercise

**Next:** Continue to [`02-git-and-github.md`](02-git-and-github.md)
