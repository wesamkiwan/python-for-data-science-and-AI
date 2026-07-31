# 📋 Module 05 Cheat Sheet: Tooling & Environments

Fast reference for virtual environments, pip, git/GitHub, and VS Code.

## Virtual Environments (`venv`)
```bash
python -m venv venv           # create a virtual environment named "venv"

# Activate
venv\Scripts\activate            # Windows
source venv/bin/activate           # macOS/Linux

deactivate                            # exit the virtual environment
```

## pip
```bash
pip install pandas                   # install latest version
pip install pandas==2.1.0              # install specific version
pip install --upgrade pandas             # upgrade
pip uninstall pandas                       # remove

pip list                                      # list installed packages
pip show pandas                                 # details on one package

pip freeze > requirements.txt                     # export exact installed versions
pip install -r requirements.txt                      # install from that file
```

## The "New Project" Setup Workflow
1. `mkdir project && cd project`
2. `python -m venv venv`
3. Activate it (see above) — confirm `(venv)` shows in your prompt
4. `pip install <packages you need>`
5. `pip freeze > requirements.txt`
6. `git init` + `.gitignore` (see below) as your very first commit

## Git — Core Workflow
```bash
git init                          # start tracking this folder
git status                          # what's changed?
git diff                              # line-by-line unstaged changes
git add file.py                         # stage one file
git add .                                 # stage everything
git commit -m "message"                     # save a checkpoint
git log --oneline                             # view history, compact
```

## Git — Remote (GitHub)
```bash
git remote add origin <url>       # connect to a GitHub repo (once)
git push -u origin main              # first push, sets upstream
git push                                # push subsequent commits
git pull                                  # fetch + merge remote changes
```

## Git — Branches
```bash
git branch                        # list branches
git branch -M main                   # rename current branch to "main"
git checkout -b new-feature             # create AND switch to a new branch
git checkout main                         # switch back
git merge new-feature                        # merge that branch into the current one
```

## `.gitignore` Essentials (Python projects)
```
venv/
__pycache__/
*.pyc
.env
.ipynb_checkpoints/
```

## VS Code Essentials

| Action | Shortcut |
|---|---|
| Command Palette | `Ctrl+Shift+P` |
| Select Python interpreter | Command Palette → "Python: Select Interpreter" |
| Integrated terminal | `` Ctrl+` `` |
| Quick file open | `Ctrl+P` |
| Run current file | ▷ button, top-right |
| Set breakpoint | click left margin next to line number |
| Start debugging | `F5` |
| Step over / into | `F10` / `F11` |
| Go to definition | `F12` or `Ctrl+Click` |
| Jupyter-style cell | `# %%` above a code block |

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `ModuleNotFoundError` even after `pip install` | venv wasn't activated when you installed, or VS Code is using the wrong interpreter | Confirm `(venv)` in prompt; check "Python: Select Interpreter" |
| `git push` rejected | Local history is behind the remote | `git pull` first, resolve any conflicts, then push |
| "branch not found" switching to `main` | Local default branch is actually `master` | Run `git branch` to check; `git branch -M main` to rename |
| Accidentally committed `venv/` or a secret | Missing/late `.gitignore` | Add `.gitignore` before ever committing; for already-committed secrets, rotate them immediately |
| `import pandas` shows red/error in VS Code despite being installed | Wrong interpreter selected | Re-run "Python: Select Interpreter", choose the project's venv |
