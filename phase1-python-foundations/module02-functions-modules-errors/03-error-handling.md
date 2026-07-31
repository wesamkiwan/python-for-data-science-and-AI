# Module 02c: Error Handling — Writing Code That Doesn't Crash

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 45min | **Prerequisites:** [02-modules-and-packages.md](02-modules-and-packages.md)

## 🎯 Learning Objectives
- [ ] Explain what an exception is and why Python raises them
- [ ] Handle errors with `try` / `except` / `else` / `finally`
- [ ] Catch specific exception types instead of catching everything blindly
- [ ] Raise your own exceptions with `raise`
- [ ] Know when to let an error crash the program vs. when to handle it

---

## Module Goal

Learn to anticipate and gracefully handle things going wrong — bad input, missing files, unexpected data — instead of letting your program crash. This is the difference between a script that works "on the happy path" and production code that survives contact with messy real-world data.

## Why This Matters on the Job

Real data is never perfectly clean. A CSV will have a missing value where a number should be, an API call will occasionally time out, a file path will occasionally not exist. Production pipelines that process thousands of rows can't afford to crash entirely because *one* row is bad — you need to catch the problem, log it, and keep going. This is one of the most-tested practical skills in take-home interview exercises.

---

## What Is an Exception?

An **exception** is Python's way of signaling that something went wrong *while the program was running* (as opposed to a syntax error, which is caught before the program even starts). You've already met several in Module 01:

```python
print(10 / 0)          # ZeroDivisionError: division by zero
print(int("abc"))       # ValueError: invalid literal for int() with base 10: 'abc'
my_dict = {}
print(my_dict["key"])    # KeyError: 'key'
my_list = [1, 2]
print(my_list[5])          # IndexError: list index out of range
```

Without handling, an exception **crashes the program** at that line — nothing after it runs.

## `try` / `except`: Catching Errors

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("You can't divide by zero!")

print("Program continues running")
```
```
You can't divide by zero!
Program continues running
```

**How it works:** Python runs the `try` block. If an exception occurs, it stops that block immediately and jumps to the matching `except` block instead of crashing. Code after the `try`/`except` still runs normally.

### Catching Specific Exceptions

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Error: cannot divide by zero.")
        return None

print(safe_divide(10, 2))   # 5.0
print(safe_divide(10, 0))    # Error: cannot divide by zero. \n None
```

⚠️ **Warning:** Avoid a bare `except:` (catching *everything*) — it silently swallows bugs you didn't anticipate too, including typos like `NameError`, making bugs much harder to find. ✅ **Best Practice:** always catch the *specific* exception type you expect.

```python
# ❌ Avoid — hides real bugs
try:
    risky_operation()
except:
    pass

# ✅ Better — only catches what you expect, lets everything else surface
try:
    risky_operation()
except ValueError:
    print("Invalid value provided.")
```

### Catching Multiple Exception Types

```python
def process_value(raw_value):
    try:
        number = int(raw_value)
        return 100 / number
    except ValueError:
        print(f"'{raw_value}' isn't a valid number.")
    except ZeroDivisionError:
        print("Can't divide by zero.")

process_value("abc")   # 'abc' isn't a valid number.
process_value("0")      # Can't divide by zero.
process_value("5")       # returns 20.0
```

You can also group exception types in one `except` if you want to handle them the same way:

```python
except (ValueError, TypeError):
    print("Bad input.")
```

## `else` and `finally`

```python
try:
    number = int("42")
except ValueError:
    print("Conversion failed.")
else:
    print(f"Conversion succeeded: {number}")   # runs only if NO exception occurred
finally:
    print("This always runs, error or not.")    # cleanup code — runs no matter what
```
```
Conversion succeeded: 42
This always runs, error or not.
```

💡 **Tip:** `finally` is the right place for cleanup that must happen regardless of success or failure — e.g., closing a file or a database connection. `else` is for code that should only run when nothing went wrong (keeping it out of `try` makes clear it isn't the part being protected).

## Accessing the Exception Details

Sometimes you want to inspect or log the actual error message:

```python
try:
    result = int("abc")
except ValueError as e:
    print(f"Caught an error: {e}")
    # Caught an error: invalid literal for int() with base 10: 'abc'
```

**How it works:** `as e` binds the exception object to the name `e`, letting you access its message (`str(e)`) — useful for logging real error details instead of a generic message.

## Raising Your Own Exceptions

Use `raise` to signal an error condition yourself — useful when you're writing a function and want to enforce that callers pass valid input.

```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative.")
    return age

set_age(30)     # works fine, returns 30
set_age(-5)      # raises: ValueError: Age cannot be negative.
```

The caller can then decide whether to catch it:

```python
try:
    set_age(-5)
except ValueError as e:
    print(f"Invalid input: {e}")
```

✅ **Best Practice:** Raise the most specific built-in exception type that fits (`ValueError` for a bad value, `TypeError` for a wrong type, `KeyError` for a missing key) rather than a generic `Exception` — this lets callers catch precisely what they expect.

## Real-World Pattern: Processing a Batch Without Crashing

```python
raw_scores = ["85", "92", "N/A", "78", "oops", "90"]
valid_scores = []

for raw in raw_scores:
    try:
        valid_scores.append(int(raw))
    except ValueError:
        print(f"Skipping invalid score: {raw!r}")

print(valid_scores)   # [85, 92, 78, 90]
```
```
Skipping invalid score: 'N/A'
Skipping invalid score: 'oops'
[85, 92, 78, 90]
```

🎯 **On the job:** This exact pattern — loop over records, `try` to process each one, `except` and log/skip the bad ones, keep going — is how real data pipelines stay robust against messy real-world input. In Phase 2, you'll learn Pandas' built-in equivalent (`pd.to_numeric(..., errors="coerce")`), which does this at scale without a manual loop.

---

## Hands-On Exercise

**Task:** Write `safe_calculator.py` that:
1. Defines a function `safe_divide(a, b)` that returns `a / b`, but catches `ZeroDivisionError` and returns `None` with a printed message instead of crashing.
2. Defines a function `parse_scores(raw_list)` that loops through a list of strings, converts each to an `int`, skips (with a printed message) any that fail, and returns the list of successfully converted integers.
3. Tests both functions with at least one input that triggers the error path.

<details>
<summary>✅ Click to see the solution</summary>

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Cannot divide by zero.")
        return None

def parse_scores(raw_list):
    valid = []
    for raw in raw_list:
        try:
            valid.append(int(raw))
        except ValueError:
            print(f"Skipping invalid score: {raw!r}")
    return valid

print(safe_divide(10, 2))    # 5.0
print(safe_divide(10, 0))     # Cannot divide by zero. \n None

scores = parse_scores(["88", "N/A", "76", "95", "bad"])
print(scores)   # [88, 76, 95]
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Bare `except:` catching everything | Always catch specific exception types |
| Using exceptions for normal control flow everywhere | Use `try`/`except` for genuinely exceptional/unpredictable cases (bad input, I/O); use `if`/`else` for expected branching |
| Swallowing errors silently (`except: pass`) | At minimum, log or print what went wrong |
| Raising a generic `Exception("bad thing")` | Raise the most specific built-in type (`ValueError`, `TypeError`, etc.) |
| Forgetting cleanup code runs even when an error occurs | Put must-run cleanup in `finally` |

---

## ✅ Module 02 Completion Checklist
- [ ] Understand what an exception is and why unhandled ones crash a program
- [ ] Can write `try` / `except` / `else` / `finally` blocks
- [ ] Can catch specific exception types (and know why bare `except:` is bad)
- [ ] Can raise a custom exception with `raise`
- [ ] Completed the `safe_calculator.py` exercise
- [ ] Reviewed [`module02-cheatsheet.md`](module02-cheatsheet.md)
- [ ] Reviewed [`module02-interview.md`](module02-interview.md)
- [ ] Browsed [`module02-references.md`](module02-references.md)

**Next Step:** Module 03 — Object-Oriented Programming (`phase1-python-foundations/module03-oop/`)
