# Module 05c: Code Editors & VS Code Setup

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 45min | **Prerequisites:** [02-git-and-github.md](02-git-and-github.md)

## 🎯 Learning Objectives
- [ ] Install VS Code and the official Python extension
- [ ] Select the correct Python interpreter (virtual environment) for a project
- [ ] Run and debug a Python script from within VS Code
- [ ] Use core productivity features: IntelliSense, integrated terminal, and Jupyter cells

---

## Module Goal

Get properly set up in **Visual Studio Code (VS Code)**, the industry-standard, free code editor for Python and data science work, and learn the handful of features that will save you enormous time for the rest of this course (and your career).

## Why This Matters on the Job

Every module from here forward assumes you have a comfortable, functioning editor setup — the wrong setup (like accidentally running code with the global Python instead of your project's virtual environment) causes a huge fraction of "why isn't this working" confusion for beginners. Getting this right now, once, pays off every single day after.

---

## Installing VS Code

1. Download from [code.visualstudio.com](https://code.visualstudio.com/) (free, cross-platform).
2. Install the **Python extension** (by Microsoft) — open VS Code, click the Extensions icon in the left sidebar (or `Ctrl+Shift+X`), search "Python", and install the official one published by Microsoft.

💡 **Tip:** The Python extension bundles several sub-features automatically: syntax highlighting, IntelliSense (smart autocomplete), linting (style/error checking), debugging, and Jupyter notebook support — installing it once covers everything you need for this entire course.

## Selecting the Right Python Interpreter

This is the single most important, most commonly misconfigured setting for beginners. VS Code needs to know **which** Python installation (global, or a specific project's virtual environment) to use for running/debugging code and providing autocomplete.

**Steps:**
1. Open the Command Palette: `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS).
2. Type "Python: Select Interpreter" and press Enter.
3. Choose the interpreter matching your project's virtual environment (it will show a path like `.\venv\Scripts\python.exe`, listed as `('venv': venv)`).

⚠️ **Warning:** If VS Code is using the wrong interpreter (e.g., the global Python instead of your project's `venv`), it will show `import pandas` as an error even though you correctly `pip install`ed it inside your activated venv — because VS Code is looking at a *different* Python installation's packages. This is the #1 cause of "but I definitely installed it!" confusion. Always double-check the interpreter shown in the bottom-right status bar matches your project's virtual environment.

## Running a Script

Three common ways, in increasing order of usefulness:

1. **Run button:** Click the ▷ ("Run Python File") button in the top-right of an open `.py` file.
2. **Integrated terminal:** Press `` Ctrl+` `` to open a terminal *inside* VS Code, then run `python script.py` yourself — this is what you'll do most often, since it also lets you pass command-line arguments and see full output.
3. **Interactive window / Jupyter cells:** Add a special comment `# %%` before a block of code to turn it into a runnable "cell" (like a Jupyter notebook), then click "Run Cell" above it — extremely useful for data exploration, which you'll rely on constantly from Module 06 onward.

```python
# %%
import pandas as pd
df = pd.DataFrame({"a": [1, 2, 3]})
df   # in a Jupyter cell, this displays as a formatted table, not just printed text
```

🎯 **On the job:** Data scientists live in this "run one cell, inspect the result, adjust, run again" loop constantly — it's dramatically faster for exploration than re-running an entire script from the top every time.

## Debugging: Stepping Through Code Line by Line

Instead of scattering `print()` statements everywhere to figure out what's wrong, a **debugger** lets you pause execution and inspect exactly what every variable holds at that moment.

**Steps:**
1. Click in the left margin next to a line number to set a **breakpoint** (a red dot appears).
2. Press `F5` (or the "Run and Debug" icon in the sidebar) to start debugging.
3. Execution pauses at your breakpoint. Use the debug toolbar to:
   - **Step Over** (`F10`) — run the current line, move to the next
   - **Step Into** (`F11`) — step inside a function call to see what happens within it
   - **Continue** (`F5`) — run until the next breakpoint (or the end)
4. While paused, hover over any variable to see its current value, or check the "Variables" panel in the sidebar.

✅ **Best Practice:** Reach for the debugger — not more `print()` statements — the moment you're confused about *why* a value isn't what you expect partway through a function. It's dramatically faster once you're comfortable with it, and it's a skill interviewers specifically look for in more senior candidates.

## Other Productivity Features Worth Knowing

| Feature | Shortcut | What it does |
|---|---|---|
| Command Palette | `Ctrl+Shift+P` | Search and run any VS Code command by name |
| Integrated terminal | `` Ctrl+` `` | Open a terminal without leaving the editor |
| Quick file open | `Ctrl+P` | Jump to any file in the project by typing part of its name |
| Format document | `Shift+Alt+F` | Auto-format your code (with a formatter extension like Black installed) |
| Multi-cursor editing | `Alt+Click` | Edit multiple lines at once |
| Go to definition | `F12` (or `Ctrl+Click`) | Jump straight to where a function/class is defined |

💡 **Tip:** `Go to Definition` (`F12`) is invaluable once you start using libraries like Pandas and scikit-learn — `Ctrl+Click` on `pd.read_csv` jumps straight into its actual source code and docstring, which is often faster than searching documentation online.

---

## Hands-On Exercise

**Task:**
1. Confirm VS Code and the Python extension are installed.
2. Open your `venv_practice` folder (from the previous lesson) in VS Code.
3. Use "Python: Select Interpreter" to confirm/select that project's `venv`.
4. Create a file `debug_practice.py` with the following buggy code:
   ```python
   def calculate_average(numbers):
       total = 0
       for n in numbers:
           total = n   # bug: should be total += n
       return total / len(numbers)

   scores = [80, 90, 100]
   print(calculate_average(scores))
   ```
5. Set a breakpoint on the `total = n` line, run the debugger, and step through the loop, watching `total`'s value each iteration to spot the bug.
6. Fix the bug (`total += n`) and confirm the corrected output is `90.0`.

<details>
<summary>✅ Click to see the solution</summary>

The bug: `total = n` overwrites `total` every iteration instead of accumulating it, so after the loop, `total` only holds the *last* number (`100`), giving `100 / 3 = 33.33` instead of the correct average.

```python
def calculate_average(numbers):
    total = 0
    for n in numbers:
        total += n   # fixed: accumulate instead of overwrite
    return total / len(numbers)

scores = [80, 90, 100]
print(calculate_average(scores))   # 90.0
```

Stepping through with the debugger and watching `total` in the Variables panel makes this exact kind of bug immediately obvious — you'd see `total` reset to each new number instead of growing, well before doing the manual math.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Wrong Python interpreter selected (global instead of project's venv) | Always check "Python: Select Interpreter" matches your project |
| Only using `print()` to debug increasingly complex issues | Reach for breakpoints + the debugger once `print()` debugging gets tedious |
| Never opening the integrated terminal | Use `` Ctrl+` `` — it's faster than switching to a separate terminal app |
| Missing the Python extension entirely | Install it first — nearly every other Python-specific feature depends on it |

---

## ✅ Module 05 Completion Checklist
- [ ] VS Code and the Python extension are installed
- [ ] Can select the correct interpreter/virtual environment for a project
- [ ] Can run a script via the Run button, integrated terminal, and a Jupyter-style cell
- [ ] Can set a breakpoint and step through code with the debugger
- [ ] Completed the `debug_practice.py` exercise
- [ ] Reviewed [`module05-cheatsheet.md`](module05-cheatsheet.md)
- [ ] Reviewed [`module05-interview.md`](module05-interview.md)
- [ ] Browsed [`module05-references.md`](module05-references.md)

**Next Step:** Module 06 — NumPy Fundamentals (`phase2-data-science-core/module06-numpy-fundamentals/`) — the start of Phase 2: Data Science Core!

---

## 🎉 Phase 1 Complete!

You've finished **Phase 1: Python Foundations** — you can now write real Python programs with functions, classes, error handling, file/API I/O, and you have a proper professional dev environment set up (virtual environments, git/GitHub, VS Code). Everything from Module 06 onward builds directly on these skills. Nice work.
