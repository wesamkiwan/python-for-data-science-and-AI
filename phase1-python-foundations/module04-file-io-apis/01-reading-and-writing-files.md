# Module 04a: Reading & Writing Files

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 45min | **Prerequisites:** [Module 03 — Object-Oriented Programming](../module03-oop/03-dunder-methods-and-encapsulation.md)

## 🎯 Learning Objectives
- [ ] Open, read, and write plain text files
- [ ] Explain why the `with` statement (context manager) is the correct way to work with files
- [ ] Use the different file modes (`r`, `w`, `a`, `x`)
- [ ] Read a file line by line vs. all at once

---

## Module Goal

Learn how Python programs read data from and write data to files on disk — the foundation for every data pipeline, since real data almost always starts life as a file (a log file, a CSV export, a config file) rather than typed directly into your code.

## Why This Matters on the Job

Before you ever load a dataset with `pd.read_csv()` in Module 07, it helps enormously to understand what's actually happening underneath: Python is opening a file, reading its raw text, and parsing it. When something goes wrong with a data load — wrong encoding, a locked file, a missing path — that lower-level understanding is what lets you diagnose the problem instead of being stuck staring at a library error.

---

## Opening a File: The `with` Statement

The correct, modern way to work with a file in Python uses a **context manager** — the `with` statement:

```python
with open("notes.txt", "w") as file:
    file.write("Hello, file!\n")
    file.write("This is line two.\n")
```

**How it works:**
- `open("notes.txt", "w")` opens (or creates) a file named `notes.txt` in **write mode** (`"w"`).
- `as file` binds the open file object to the name `file` for use inside the block.
- `file.write(...)` writes text to it. `\n` is the newline character — without it, everything runs together on one line.
- When the indented block ends, `with` **automatically closes the file** — even if an error occurred inside the block.

⚠️ **Warning:** The old-school alternative — `file = open(...)` then manually calling `file.close()` later — is error-prone: if an exception happens between opening and closing, the file never gets closed, which can corrupt data or leak system resources. ✅ **Best Practice:** always use `with open(...) as file:` — never call `open()` without it.

## File Modes

| Mode | Meaning | If file doesn't exist | If file exists |
|---|---|---|---|
| `"r"` | Read (default) | Raises `FileNotFoundError` | Reads from the start |
| `"w"` | Write | Creates it | **Overwrites/erases** existing content |
| `"a"` | Append | Creates it | Adds to the end, keeps existing content |
| `"x"` | Exclusive create | Creates it | Raises `FileExistsError` |

⚠️ **Warning:** `"w"` mode silently erases the entire existing file the moment you open it — even before you write anything. This is one of the most damaging beginner mistakes (accidentally wiping a file you meant to only read). Double-check your mode before running write code against a real file.

## Reading a File

```python
with open("notes.txt", "r") as file:
    contents = file.read()      # reads the ENTIRE file as one string

print(contents)
```
```
Hello, file!
This is line two.
```

### Reading Line by Line

For large files, reading line by line is more memory-efficient than loading everything at once:

```python
with open("notes.txt", "r") as file:
    for line in file:              # iterating over a file yields one line at a time
        print(line.strip())          # .strip() removes the trailing \n
```
```
Hello, file!
This is line two.
```

Other common reading methods:

```python
with open("notes.txt", "r") as file:
    lines = file.readlines()   # returns a LIST of lines, each still ending in \n

print(lines)   # ['Hello, file!\n', 'This is line two.\n']
```

💡 **Tip:** For small-to-medium files, `.read()` or `.readlines()` are convenient. For genuinely large files (gigabytes of logs, for example), looping line-by-line with `for line in file:` avoids loading the whole thing into memory at once.

## Appending to a File

```python
with open("notes.txt", "a") as file:
    file.write("This line was appended.\n")

with open("notes.txt", "r") as file:
    print(file.read())
```
```
Hello, file!
This is line two.
This line was appended.
```

## Checking If a File Exists

Trying to read a file that doesn't exist raises `FileNotFoundError`. Use the standard library's `os.path` (or the more modern `pathlib`) to check first, or catch the exception:

```python
import os

if os.path.exists("notes.txt"):
    with open("notes.txt", "r") as file:
        print(file.read())
else:
    print("File not found.")
```

Or, using the error-handling skills from Module 02:

```python
try:
    with open("missing_file.txt", "r") as file:
        print(file.read())
except FileNotFoundError:
    print("That file doesn't exist yet.")
```

🎯 **On the job:** This exact pattern — check if a file exists, or catch `FileNotFoundError` — is standard practice before loading any dataset, config, or log file in a real pipeline, since assuming a file is always there is a common cause of production crashes.

---

## Hands-On Exercise

**Task:** Write `journal.py` that:
1. Writes three lines of your choice to a new file `journal.txt` (write mode).
2. Appends one additional line to the same file (append mode).
3. Reads the file back line by line, printing each line with its line number (e.g., `1: Hello`).
4. Wraps the read step in a `try`/`except FileNotFoundError` in case the file is missing.

<details>
<summary>✅ Click to see the solution</summary>

```python
with open("journal.txt", "w") as file:
    file.write("Today I learned about file I/O.\n")
    file.write("Context managers close files automatically.\n")
    file.write("Write mode erases existing content.\n")

with open("journal.txt", "a") as file:
    file.write("This line was appended afterward.\n")

try:
    with open("journal.txt", "r") as file:
        for line_number, line in enumerate(file, start=1):
            print(f"{line_number}: {line.strip()}")
except FileNotFoundError:
    print("journal.txt doesn't exist yet.")
```

**Expected output:**
```
1: Today I learned about file I/O.
2: Context managers close files automatically.
3: Write mode erases existing content.
4: This line was appended afterward.
```

Note: `enumerate(file, start=1)` pairs each line with a counter starting at 1 — a clean way to number lines without manually tracking an index.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Opening a file without `with` and forgetting to close it | Always use `with open(...) as file:` |
| Using `"w"` mode when you meant to only read or append | Double-check the mode — `"w"` erases existing content immediately |
| Forgetting `\n` when writing lines | Add `\n` explicitly, or use `print(..., file=file)` |
| Loading a huge file entirely into memory with `.read()` | Iterate line by line (`for line in file:`) for large files |
| Assuming a file always exists | Check with `os.path.exists()` or catch `FileNotFoundError` |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Can open, read, and write text files using `with`
- [ ] Understand the difference between `"r"`, `"w"`, `"a"`, and `"x"` modes
- [ ] Can read a file line by line vs. all at once
- [ ] Can handle a missing file gracefully
- [ ] Completed the `journal.py` exercise

**Next:** Continue to [`02-json-and-csv.md`](02-json-and-csv.md)
