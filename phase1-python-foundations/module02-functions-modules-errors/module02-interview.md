# 🎤 Module 02 Interview Prep: Functions, Modules & Error Handling

## Conceptual Questions

### 🟢 Beginner

**Q: What's the difference between a parameter and an argument?**
> A: A parameter is the named placeholder in a function's definition (`def greet(name):` — `name` is a parameter). An argument is the actual value passed in when you call the function (`greet("Ada")` — `"Ada"` is the argument). People often use the terms loosely/interchangeably in conversation, but knowing the precise distinction helps when reading error messages that mention one or the other.

**Q: What does a function return if it has no explicit `return` statement?**
> A: `None`. If a function only calls `print()` and never explicitly `return`s a value, capturing its result in a variable will store `None`, not whatever was printed. This is a common beginner mistake when confusing "displaying" a value with "returning" it.

**Q: What's the difference between a module and a package?**
> A: A module is a single `.py` file. A package is a folder containing multiple related modules (typically with an `__init__.py` marking it as importable). NumPy and Pandas are packages — each is a folder of many modules distributed and installed together.

### 🟡 Intermediate

**Q: Why is `from module import *` generally discouraged?**
> A: It imports every public name from that module directly into your namespace without a prefix, which makes it unclear where any given name came from when reading the code later, and risks silently overwriting names you already have (e.g., your own `pi` variable getting clobbered by `math.pi`). Explicit imports (`import module`, `import module as alias`, or `from module import specific_name`) keep code traceable.

**Q: Why shouldn't you use a mutable default argument like `def f(items=[]):`?**
> A: Default argument values are evaluated *once*, when the function is defined — not on every call. If the default is a mutable object like a list, every call that doesn't pass its own `items` shares and mutates the *same* list object, which persists and grows across calls in a way that's very surprising. The standard fix is `def f(items=None): items = items if items is not None else []` — creating a fresh list inside the function body every call.

**Q: Explain what happens with `global` and why relying on it is usually a bad idea.**
> A: Assigning to a variable inside a function creates a local variable by default, even if a global variable with the same name exists — Python decides this at compile time for the whole function body. The `global` keyword tells Python "this name refers to the module-level variable, not a new local one," letting the function modify it. It's generally discouraged because it makes a function's behavior depend on and silently change external state, which is harder to test, reason about, and parallelize than a function that just takes arguments and returns a result.

## Practical/Coding Questions

**Q: Write a function that takes any number of numeric arguments and returns their average, handling the case of zero arguments gracefully.**
```python
def average(*numbers):
    if not numbers:
        return 0
    return sum(numbers) / len(numbers)

print(average(2, 4, 6))   # 4.0
print(average())            # 0
```
> Explanation: `*numbers` collects all positional arguments into a tuple. Checking `if not numbers` (an empty tuple is falsy) avoids a `ZeroDivisionError` from `len(numbers)` being 0.

**Q: Write a function `safe_int(value, default=0)` that converts `value` to an `int`, returning `default` if the conversion fails.**
```python
def safe_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default

print(safe_int("42"))     # 42
print(safe_int("abc"))      # 0
print(safe_int(None))        # 0
```
> Explanation: catching both `ValueError` (bad string content) and `TypeError` (e.g. passing `None`, which `int()` can't accept at all) covers the two realistic failure modes for this conversion.

## Scenario Questions

**Q: You're processing a list of 10,000 API responses in a loop, and one response is missing an expected key, raising a `KeyError` that crashes the whole job at record #4,281. How would you redesign this to be production-safe?**
> A: Wrap the per-record processing logic in a `try`/`except KeyError` (or more broadly, catch the specific exceptions I expect from malformed records) inside the loop, not around the whole loop — that way one bad record is logged/skipped and the loop continues to the next one instead of losing all progress. I'd also log which record failed and why, so the bad data can be investigated afterward rather than silently dropped.

**Q: When would you choose to let an exception crash the program versus catching it?**
> A: If the error represents a truly unrecoverable, unexpected state — e.g., a configuration file that must exist for the program to make sense at all — letting it crash loudly (with a clear traceback) is often better than silently limping along in a broken state. I'd catch exceptions when the failure is expected/routine (bad row in a large dataset, an occasional network timeout I can retry) and the program can meaningfully continue without that one piece of data.

## "Gotcha" Questions

**Q: What's wrong with this code?**
```python
def add_item(item, items=[]):
    items.append(item)
    return items

print(add_item("a"))   # ['a']
print(add_item("b"))    # ['a', 'b']  <- probably not what you expected!
```
> A: The default `items=[]` is created *once* at function definition time and reused across every call that doesn't supply its own list, so items silently accumulate across unrelated calls. Fix: `def add_item(item, items=None): items = items if items is not None else []`.

**Q: What does this print, and why?**
```python
def outer():
    x = 10
    def inner():
        print(x)   # reads the enclosing function's x — this works fine
    inner()

outer()   # 10
```
> A: `10`. Nested functions can *read* variables from an enclosing function's scope (this is called a closure) without needing `global` — `global` is only required when you need to *modify* a name defined at module level from inside a function.

## Quick-Fire Rapid Review

- Q: What does a function with no `return` give back? → **`None`**
- Q: `*args` collects what into what? → **extra positional arguments into a tuple**
- Q: `**kwargs` collects what into what? → **extra keyword arguments into a dict**
- Q: Keyword to modify a global variable inside a function? → **`global`**
- Q: Safest way to import from a library? → **`import module` / `import module as alias` / `from module import name`, not `import *`**
- Q: Runs no matter what, error or not? → **`finally`**
- Q: Runs only if the `try` block succeeded? → **`else`**
- Q: Never use this as a default argument value → **a mutable object like `[]` or `{}`**
