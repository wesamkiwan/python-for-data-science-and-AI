# 🎤 Module 05 Interview Prep: Tooling & Environments

## Conceptual Questions

### 🟢 Beginner

**Q: Why do we use virtual environments instead of installing packages globally?**
> A: Different projects often need different, sometimes conflicting, versions of the same package. A virtual environment gives each project its own isolated Python installation and set of packages, so installing or upgrading something for one project can never silently break another. It also makes a project's exact dependencies explicit and reproducible via `requirements.txt`, rather than depending on whatever happens to be installed globally on a given machine.

**Q: What's the difference between `git add` and `git commit`?**
> A: `git add` stages changes — marking specific files/changes as "ready to be included in the next checkpoint" — without actually saving them to history yet. `git commit` takes everything currently staged and saves it as a permanent snapshot in the project's history, along with a message. Staging lets you build up exactly what you want in a commit, even if you have other unrelated changes sitting in the working directory that you're not ready to commit yet.

**Q: What does a `.gitignore` file do, and why is `venv/` almost always in it?**
> A: `.gitignore` tells git which files/folders to never track or commit, even if they exist in the project folder. `venv/` is excluded because it's large, platform-specific (it may not even work if copied to a different OS), and fully reproducible from `requirements.txt` — there's no reason to store it in version control when `pip install -r requirements.txt` recreates it identically on any machine.

### 🟡 Intermediate

**Q: Explain the difference between `git push` and `git pull`.**
> A: `git push` sends your local commits to the remote repository (e.g., GitHub), updating it with your latest history. `git pull` does the reverse — it fetches commits from the remote and merges them into your local branch. If you and a teammate are both working on the same branch, you generally need to `git pull` before you `push`, since git will reject a push if your local history doesn't already include the remote's latest commits.

**Q: What's a practical reason to use a feature branch instead of committing directly to `main`?**
> A: A feature branch isolates in-progress, potentially broken work from `main`, which should stay stable and deployable at all times. It also enables code review — you push the branch, open a Pull Request, and teammates review the diff before it's merged — and if the feature turns out to be a bad idea, you can simply discard the branch without ever having disturbed `main`'s history.

**Q: How would you reproduce a teammate's exact Python environment on a new machine?**
> A: Clone the repository, create a fresh virtual environment (`python -m venv venv`), activate it, and run `pip install -r requirements.txt` — assuming they committed an up-to-date `requirements.txt` (generated via `pip freeze`) alongside their code, this recreates the identical set of packages and versions they were using.

## Practical/Coding Questions

**Q: Walk through the exact sequence of commands to take a brand-new, empty project folder from nothing to a working, isolated environment with `requests` installed and its own git history.**
```bash
mkdir my_project && cd my_project
python -m venv venv
source venv/bin/activate        # or venv\Scripts\activate on Windows
pip install requests
pip freeze > requirements.txt

git init
git branch -M main
echo -e "venv/\n__pycache__/" > .gitignore
git add .
git commit -m "Initial commit: project setup with requests dependency"
```
> Explanation: this is the canonical "start a new Python project" sequence — isolate dependencies first, capture them in `requirements.txt`, then initialize version control with a `.gitignore` in place *before* the first commit so nothing unwanted (like `venv/`) ever gets tracked.

**Q: Your `requirements.txt` is out of date after you `pip install`ed two new packages mid-project. What's the fix?**
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update requirements.txt with newly added dependencies"
```
> Explanation: `pip freeze` always reflects the *current* state of the active environment, so simply re-running it and overwriting the file brings it back in sync; committing that change keeps the repository's documented dependencies accurate for anyone who sets the project up next.

## Scenario Questions

**Q: A teammate says "it works on my machine" but the exact same code crashes with `ModuleNotFoundError` on yours. What would you check first?**
> A: First, whether they committed and you correctly installed from an up-to-date `requirements.txt` — if they added a new package but forgot to regenerate/commit that file, your environment simply won't have it. Second, whether your own virtual environment is actually activated when you run the script (or whether VS Code has the correct interpreter selected) — installing into the wrong environment (or none at all) produces exactly this symptom even when the package is "installed" somewhere on the machine.

**Q: You accidentally committed and pushed a file containing an API key to a public GitHub repo. What do you do?**
> A: The most important immediate step is to treat the key as compromised and rotate/revoke it right away at the source (the service that issued it) — simply deleting the file in a new commit does *not* remove it from git's history, so anyone can still retrieve it from an earlier commit. After rotating the credential, I'd also remove the secret from history (e.g., with `git filter-repo` or GitHub's guidance for removing sensitive data) and add the file to `.gitignore` going forward so it can't happen again.

## "Gotcha" Questions

**Q: You run `pip install pandas` and it succeeds, but your script still can't `import pandas`. What's the most likely explanation?**
> A: The virtual environment wasn't activated when you ran `pip install`, so the package installed globally (or into a different environment) rather than into the one your script actually runs against — or conversely, it installed correctly into a venv that simply isn't the one currently active/selected when you run the script. Always confirm `(venv)` appears in your terminal prompt before installing, and confirm VS Code's selected interpreter matches.

**Q: You run `git checkout main` and get an error that no such branch exists, even though you're sure you've been committing normally. What's going on?**
> A: Your repository's default branch is very likely named `master`, not `main` — this depends on your local git version and configuration, and doesn't always match GitHub's `main` default. Running `git branch` shows the actual current branch name; `git branch -M main` renames it to match GitHub's convention if that's what you want.

## Quick-Fire Rapid Review

- Q: Command to create a virtual environment named `venv`? → **`python -m venv venv`**
- Q: Command to export exact installed package versions? → **`pip freeze > requirements.txt`**
- Q: Command to install from a requirements file? → **`pip install -r requirements.txt`**
- Q: What must you do before `pip install` actually goes into your project's isolated environment? → **activate the virtual environment**
- Q: Command to create AND switch to a new branch in one step? → **`git checkout -b branch-name`**
- Q: File that tells git what to never track? → **`.gitignore`**
- Q: Command to see exactly what changed, not yet staged? → **`git diff`**
- Q: VS Code shortcut to select the Python interpreter? → **Command Palette (`Ctrl+Shift+P`) → "Python: Select Interpreter"**
