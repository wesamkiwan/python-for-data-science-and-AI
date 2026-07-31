# Module 05b: Git & GitHub — Version Control Fundamentals

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [01-virtual-environments-and-pip.md](01-virtual-environments-and-pip.md)

## 🎯 Learning Objectives
- [ ] Explain what version control is and why every project needs it
- [ ] Initialize a git repository and make commits
- [ ] Connect a local repository to GitHub and push/pull changes
- [ ] Use branches for isolated, parallel work
- [ ] Write an effective `.gitignore` file

---

## Module Goal

Learn **git**, the version control system used by virtually every software team on the planet, and **GitHub**, the most popular platform for hosting git repositories, collaborating, and showcasing your work. This is non-negotiable professional infrastructure — you'll use it every single day on the job.

## Why This Matters on the Job

Git gives you a complete, searchable history of every change ever made to a project, the ability to undo mistakes, and a way for multiple people to work on the same codebase without overwriting each other's work. GitHub is also where you'll build your **portfolio** — the capstone projects later in this course are meant to live in public GitHub repositories you can show an interviewer. This course's own repository (the one you're reading this file from!) is itself a live example of everything in this lesson.

---

## What Is Version Control?

**Version control** tracks changes to files over time, letting you see what changed, when, and by whom — and roll back to any previous state if something breaks. Git is a **distributed** version control system: every clone of a repository has the *entire* history, not just a pointer to a central server.

💡 **Analogy:** Think of git like an infinitely detailed "track changes" + "save version" system for an entire folder of files, where you decide exactly when to save a meaningful checkpoint (a **commit**) and can always jump back to any checkpoint later.

## Installing & Configuring Git

Download from [git-scm.com](https://git-scm.com/) if not already installed, then verify:

```bash
git --version
```

Configure your identity once per machine (this attaches your name/email to every commit you make):

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

## The Core Git Workflow

```bash
git init                     # turn the current folder into a git repository (once, per project)
git status                     # see what's changed since the last commit
git add file.py                  # stage a specific file (mark it to be included in the next commit)
git add .                           # stage ALL changed files in the current folder
git commit -m "Add data loader"       # save a checkpoint with a descriptive message
git log                                  # view the commit history
```

⚠️ **Warning:** `git init` names the default branch based on your local git configuration — depending on your git version and settings, this may be `master` or `main`. GitHub itself defaults new repositories to `main`. Run `git branch` any time to check your current branch's actual name, and if you want to match GitHub's convention, rename it with `git branch -M main` before your first push. This mismatch (expecting `main` locally when you actually have `master`, or vice versa) is a common source of "branch not found" confusion for beginners.

**How it works:**
- `git init` creates a hidden `.git/` folder that stores the entire history — do this once at the root of your project.
- **Staging** (`git add`) is a middle step between "changed on disk" and "saved in history" — it lets you choose exactly which changes go into the next commit, rather than committing everything blindly.
- `git commit -m "..."` saves a permanent snapshot of everything currently staged, along with a message explaining *why* the change was made.

✅ **Best Practice:** Write commit messages that explain the *why*, not just the *what* — `"Fix off-by-one error in batch loader causing last row to be dropped"` is far more useful six months later than `"fix bug"`.

## Checking What Changed: `git diff`

```bash
git diff              # shows exact line-by-line changes not yet staged
git diff --staged       # shows changes that ARE staged, about to be committed
```

💡 **Tip:** Run `git diff` before every `git add` as a habit — reviewing exactly what you're about to stage catches accidental changes (like a stray `print()` you forgot to remove) before they're committed.

## Connecting to GitHub

**GitHub** hosts your git repository remotely — a **remote** — so you can back it up, share it, and collaborate. To connect an existing local repository to a new GitHub repo:

```bash
git remote add origin https://github.com/yourusername/your-repo.git
git push -u origin main       # pushes your commits AND sets "origin/main" as the default upstream
```

After that first push, day-to-day syncing is just:

```bash
git push        # send your local commits to GitHub
git pull          # fetch and merge changes from GitHub into your local copy
```

**How it works:** `origin` is just a conventional nickname for "the remote repository this project is connected to" — you could name it anything, but `origin` is what everyone uses by default. `-u` (short for `--set-upstream`) only needs to run once per branch; after that, plain `git push`/`git pull` know where to send/fetch from.

⚠️ **Warning:** Always `git pull` before you start new work (especially if working with others, or across multiple machines) — pushing when your local history is behind the remote's causes a rejected push that requires merging first.

## Branches: Isolated, Parallel Work

A **branch** is an independent line of development — changes made on one branch don't affect others until you explicitly merge them. `main` (sometimes `master` on older repos) is the default, primary branch.

```bash
git branch                          # list branches (current one marked with *)
git branch feature-login               # create a new branch (doesn't switch to it yet)
git checkout feature-login                # switch to that branch
git checkout -b feature-signup               # create AND switch in one step

# ... make changes, git add, git commit on feature-signup ...

git checkout main                                # switch back to main
git merge feature-signup                            # bring feature-signup's commits into main
```

🎯 **On the job:** The standard team workflow is: create a branch for each feature/fix, commit your work there, push the branch, open a **Pull Request** on GitHub (a request to merge your branch into `main`, which teammates review), then merge once approved. `main` stays stable and deployable at all times; in-progress work lives on branches.

## `.gitignore`: Excluding Files from Version Control

Certain files should **never** be committed — virtual environments, credentials, cache files, OS-specific junk files. A `.gitignore` file (placed at the repo root) tells git to ignore matching files/folders entirely.

```
# .gitignore
venv/
__pycache__/
*.pyc
.env
.DS_Store
*.log
```

**How it works:** Each line is a pattern. `venv/` ignores that entire folder. `*.pyc` ignores every file ending in `.pyc` (Python's compiled bytecode cache), anywhere in the project. `.env` ignores a file commonly used to store secrets/API keys.

⚠️ **Warning:** Never commit credentials, API keys, or passwords — even briefly. Once something is committed, it exists in git's history forever (even if you delete it in a later commit), and if pushed to a public GitHub repo, it can be scraped by bots within minutes. Always add secret-holding files (`.env`, `credentials.json`) to `.gitignore` *before* your first commit that could include them.

✅ **Best Practice:** Add a `.gitignore` as your very first commit in any new project, before you've had a chance to accidentally commit something you shouldn't. [gitignore.io](https://www.toptal.com/developers/gitignore) and GitHub's own [templates](https://github.com/github/gitignore) generate good starting points for any language/tool.

---

## Hands-On Exercise

**Task:**
1. Create a folder `git_practice`, navigate into it, and run `git init`.
2. Create a `.gitignore` file that ignores `venv/` and `__pycache__/`.
3. Create a file `main.py` with a simple `print("Hello, git!")`.
4. Stage and commit both files with a clear commit message.
5. Create a new branch called `add-feature`, switch to it, and add a second line to `main.py`.
6. Commit that change on the branch, switch back to `main`, and merge `add-feature` into it.
7. Run `git log` to confirm both commits appear in `main`'s history.

<details>
<summary>✅ Click to see the solution</summary>

```bash
mkdir git_practice
cd git_practice
git init
git branch -M main   # ensure the default branch is named "main", matching GitHub's convention

echo "venv/" > .gitignore
echo "__pycache__/" >> .gitignore

echo "print('Hello, git!')" > main.py

git add .
git commit -m "Initial commit: add .gitignore and hello-world script"

git checkout -b add-feature
echo "print('This is a new feature.')" >> main.py

git add main.py
git commit -m "Add second print statement to main.py"

git checkout main
git merge add-feature

git log --oneline
```

**Expected outcome:** `git log --oneline` on `main` shows both commits, and `main.py` now contains both `print()` lines.

💡 **Tip:** If `git branch -M main` errors because you have no commits yet, skip it and run it right after your first commit instead — either order works, as long as you run it before switching to your feature branch.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Committing `venv/`, `.env`, or other secrets/junk | Set up `.gitignore` before your first commit |
| Vague commit messages (`"fix"`, `"stuff"`, `"update"`) | Write messages explaining *why* the change was made |
| Working directly on `main` for every change | Use a feature branch, then merge (or open a Pull Request) once done |
| Pushing without pulling first when collaborating | `git pull` before starting new work to avoid rejected pushes |
| Forgetting `git status` before committing | Run it constantly — it's the single most useful command for staying oriented |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Understand what version control is and why it matters
- [ ] Can `init`, `add`, `commit`, and check `status`/`log`/`diff`
- [ ] Can connect a local repo to GitHub and `push`/`pull`
- [ ] Can create, switch, and merge branches
- [ ] Can write an effective `.gitignore`
- [ ] Completed the `git_practice` exercise

**Next:** Continue to [`03-code-editors-and-vscode.md`](03-code-editors-and-vscode.md)
