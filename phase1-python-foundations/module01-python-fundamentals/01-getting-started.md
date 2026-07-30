# Module 01a: Getting Started with Python

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** None

## 🎯 Learning Objectives
- [ ] Explain what Python is and why it's the #1 language for data science and AI
- [ ] Install Python and run code two different ways (script + interactive/REPL)
- [ ] Write, save, and run your first `.py` file
- [ ] Use comments and understand Python's indentation rule
- [ ] Declare and use variables correctly

---

## Module Goal

Get Python installed, understand how code actually runs, and write your first working program. This is the "hello world" foundation everything else in this course sits on top of.

## Why This Matters on the Job

Every data scientist, ML engineer, and AI engineer writes Python daily — in Jupyter notebooks for exploration, in `.py` scripts/modules for production pipelines, and in both when building AI applications. Before you can use pandas or PyTorch, you need to be fluent in bare Python: how to run it, how it reads your code, and how to avoid the syntax mistakes that trip up 90% of beginners (indentation errors are the #1 beginner bug).

---

## What Is Python?

**Python** is a general-purpose, high-level programming language known for being easy to read and write. "High-level" means it hides most of the complex details of how a computer works (memory management, machine code) so you can focus on solving problems.

💡 **Why Python for data science & AI specifically?**
- **Huge ecosystem**: NumPy, Pandas, scikit-learn, PyTorch, TensorFlow, HuggingFace — nearly every major data/AI library is Python-first.
- **Readable syntax**: code looks close to plain English, which speeds up learning and collaboration.
- **Interpreted language**: you run code directly without a separate "compile" step, which makes experimentation fast (critical for data exploration).
- **Industry standard**: it's the language used at Google, Netflix, OpenAI, and virtually every company doing data/AI work today.

## Installing Python

1. Go to [python.org/downloads](https://www.python.org/downloads/) and download the latest **Python 3.11+** (never use Python 2 — it's deprecated/unsupported).
2. **Windows users:** during install, check the box **"Add Python to PATH"**. This lets you run `python` from any terminal.
3. Verify the install by opening a terminal (PowerShell on Windows, Terminal on macOS) and running:

```bash
python --version
```

Expected output:
```
Python 3.11.7
```

⚠️ **Warning:** If you see `python: command not found` or a Python 2.x version, revisit your PATH setup or try `python3 --version` instead (common on macOS/Linux).

## Two Ways to Run Python Code

### 1. The Interactive Interpreter (REPL)

REPL stands for **Read-Eval-Print Loop** — you type one line, Python runs it immediately and shows the result. Great for quick experiments.

```bash
python
```

```python
>>> 2 + 2
4
>>> print("Hello, Data Science!")
Hello, Data Science!
>>> exit()
```

🎯 **On the job:** Jupyter Notebook (which you'll use constantly in Phase 2+) is essentially a supercharged, shareable REPL — you'll recognize this same "run a bit, see the result immediately" workflow.

### 2. Running a Script File

For anything beyond a one-liner, you write code in a `.py` file and run the whole file at once. This is how production code, pipelines, and reusable programs work.

**Step-by-step:**

1. Create a file named `hello.py` in a folder of your choice.
2. Add this code:

```python
# This is my first Python program
print("Hello, Data Science!")
print("2 + 2 =", 2 + 2)
```

3. Run it from the terminal:

```bash
python hello.py
```

**Expected output:**
```
Hello, Data Science!
2 + 2 = 4
```

**Line-by-line explanation:**
- `# This is my first Python program` — a **comment**. Anything after `#` on a line is ignored by Python; it's there purely for humans to read.
- `print(...)` — a built-in **function** that displays text/values on the screen. `print` is one of the most-used functions in all of Python.
- `"Hello, Data Science!"` — a **string** (text data), wrapped in quotes.
- `print("2 + 2 =", 2 + 2)` — `print` can take multiple items separated by commas; it prints them space-separated. `2 + 2` is evaluated (calculated) *before* being printed, giving `4`.

## Comments

Comments document *why* code exists, not *what* it does (good code should already be readable). Python has two comment styles:

```python
# Single-line comment

"""
Multi-line comment
(technically a string literal Python ignores if
it's not assigned to anything — commonly used for
documentation blocks)
"""
```

✅ **Best Practice:** Use `#` for real comments. Reserve `"""triple quotes"""` for **docstrings** (documentation strings placed at the top of functions/files) — you'll learn these properly in Module 02.

## Indentation: Python's Most Important Rule

Unlike many languages that use `{ }` curly braces to group code, Python uses **indentation** (whitespace at the start of a line) to define blocks of code. This isn't a style choice — it's required syntax.

```python
if 5 > 3:
    print("5 is greater than 3")   # indented = part of the if-block
print("This always runs")          # not indented = outside the if-block
```

⚠️ **Warning:** Mixing tabs and spaces, or inconsistent indentation, causes an `IndentationError`. **Always use 4 spaces per indentation level** (the universal Python convention — configure your editor to insert spaces when you press Tab).

## Variables

A **variable** is a named container that stores a value in memory so you can reuse it later.

```python
name = "Ada"
age = 36
is_learning_python = True

print(name)              # Ada
print(age)                # 36
print(is_learning_python) # True
```

**How it works:** `name = "Ada"` is an **assignment** — the `=` sign takes the value on the right (`"Ada"`) and binds it to the label on the left (`name`). This is *not* mathematical equality; it's "store this value under this name."

### Variable Naming Rules

| Rule | Example |
|---|---|
| Must start with a letter or underscore | `age`, `_temp` ✅ &nbsp;&nbsp; `2age` ❌ |
| Can contain letters, numbers, underscores | `user_2` ✅ |
| Case-sensitive | `Age` and `age` are different variables |
| Cannot be a reserved keyword | `class = 5` ❌ (`class` is reserved) |
| Convention: `snake_case` for variables | `first_name` ✅ (not `firstName` — that's JavaScript style) |

✅ **Best Practice:** Use descriptive names. `df` (for a dataframe) or `total_revenue` communicates intent far better than `x` or `t1`. You'll thank yourself (and so will your teammates) six months later.

💡 **Tip:** Python is **dynamically typed** — you don't declare a variable's type up front. `age = 36` then later `age = "thirty-six"` is legal (age just now refers to a string instead). This is flexible but means you must be disciplined about knowing what type a variable holds — covered next in Module 01b.

---

## Hands-On Exercise

**Task:** Create a file `about_me.py` that:
1. Stores your name, age, and favorite programming language in three variables.
2. Prints a sentence combining all three, e.g. `"My name is Wesam, I am 30 years old, and my favorite language is Python."`
3. Includes at least one comment explaining what the script does.

<details>
<summary>✅ Click to see the solution</summary>

```python
# This script introduces myself using variables and print()
name = "Wesam"
age = 30
favorite_language = "Python"

print("My name is " + name + ", I am " + str(age) + " years old, and my favorite language is " + favorite_language + ".")
```

**Expected output:**
```
My name is Wesam, I am 30 years old, and my favorite language is Python.
```

Note the `str(age)` — `age` is a number, and Python can't directly combine (`+`) a number with a string. You must convert it to a string first (called **type casting**, covered in the next lesson). You'll also learn a cleaner way to do this with **f-strings** next.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Forgetting `python --version` shows Python 2 on some systems | Always confirm 3.11+ before starting; use `python3` if needed |
| Mixing tabs and spaces | Set your editor to insert 4 spaces on Tab |
| `print "hello"` (no parentheses) | Python 3 requires parentheses: `print("hello")` — this is a common leftover from Python 2 |
| Using `x`, `y`, `temp` as variable names | Use descriptive `snake_case` names |
| Forgetting Python is case-sensitive | `Name` ≠ `name` — a very common source of `NameError` bugs |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Python 3.11+ installed and verified with `python --version`
- [ ] Ran code in the interactive REPL
- [ ] Created and ran a `.py` script file
- [ ] Understand why indentation matters in Python
- [ ] Created variables and printed them
- [ ] Completed the `about_me.py` exercise

**Next:** Continue to [`02-data-types-and-operators.md`](02-data-types-and-operators.md)
