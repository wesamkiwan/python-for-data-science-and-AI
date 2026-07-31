# Module 02a: Functions — Reusable, Testable Code

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [Module 01 — Python Fundamentals](../module01-python-fundamentals/03-control-flow-and-collections.md)

## 🎯 Learning Objectives
- [ ] Define and call functions with `def`
- [ ] Use parameters, arguments, and `return` values correctly
- [ ] Use default arguments and keyword arguments
- [ ] Use `*args` and `**kwargs` to accept flexible numbers of arguments
- [ ] Explain variable scope (local vs. global)
- [ ] Write a proper docstring for a function

---

## Module Goal

Learn to package logic into reusable, named blocks — **functions**. This is the single biggest jump in code quality from Module 01: instead of copy-pasting the same lines repeatedly, you write it once and call it wherever you need it.

## Why This Matters on the Job

Every real codebase is built from functions. A data pipeline isn't one giant script — it's `load_data()`, `clean_data()`, `train_model()`, `evaluate_model()`, each doing one clear job. Interviewers test this constantly ("write a function that..."), and on the job you'll read far more function signatures than you write from scratch — understanding parameters, defaults, and return values fluently is non-negotiable.

---

## Defining and Calling a Function

```python
def greet(name):
    return f"Hello, {name}!"

message = greet("Ada")
print(message)   # Hello, Ada!
```

**How it works:**
- `def greet(name):` — **defines** a function named `greet` that takes one **parameter**, `name`. This line does *not* run the code inside — it just teaches Python the recipe.
- `name` inside the parentheses is a **parameter** (the placeholder). `"Ada"` passed in when calling is the **argument** (the actual value).
- `return` sends a value back to wherever the function was called. A function without `return` implicitly returns `None`.
- `greet("Ada")` — **calling** the function, which actually runs its code with `name` bound to `"Ada"`.

⚠️ **Warning:** `print()` inside a function displays something, but `return` is what hands a value back so you can store it in a variable or use it elsewhere. Confusing the two is a very common beginner bug — a function that only `print()`s its result returns `None` if you try to capture it.

```python
def greet_bad(name):
    print(f"Hello, {name}!")   # displays but doesn't return anything

result = greet_bad("Ada")   # prints "Hello, Ada!"
print(result)                # None  <- gotcha!
```

## Parameters, Arguments & Return Values

A function can take multiple parameters and return a computed value:

```python
def calculate_total(price, quantity):
    total = price * quantity
    return total

order_total = calculate_total(9.99, 3)
print(order_total)   # 29.97
```

You can return multiple values at once — Python packages them into a **tuple** (from Module 01):

```python
def min_max(numbers):
    return min(numbers), max(numbers)

lowest, highest = min_max([4, 8, 15, 16, 23, 42])
print(lowest, highest)   # 4 42
```

💡 **Tip:** This "return a tuple, unpack into multiple variables" pattern is extremely common in real code — you'll see it again with functions like `train_test_split()` in scikit-learn (Module 12).

## Default Arguments

Give a parameter a default value so callers can omit it:

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

print(greet("Ada"))                  # Hello, Ada!
print(greet("Ada", "Welcome"))        # Welcome, Ada!
```

⚠️ **Warning:** Parameters with defaults must come *after* parameters without defaults. `def f(a=1, b):` is a `SyntaxError`.

## Keyword Arguments

You can call a function by naming its parameters instead of relying on position — this makes calls with several arguments far more readable:

```python
def create_user(username, age, is_admin=False):
    return {"username": username, "age": age, "is_admin": is_admin}

# Positional (order matters)
create_user("wesam", 30)

# Keyword (order doesn't matter, and it's self-documenting)
create_user(age=30, username="wesam", is_admin=True)
```

✅ **Best Practice:** Once a function has 3+ parameters, prefer calling it with keyword arguments — `create_user(username="wesam", age=30, is_admin=True)` is far easier for a reviewer to check at a glance than three bare positional values.

## `*args` and `**kwargs`: Flexible Arguments

Sometimes you don't know in advance how many arguments a function needs to accept.

```python
def total(*args):
    return sum(args)

print(total(1, 2, 3))        # 6
print(total(1, 2, 3, 4, 5))   # 15
```

**How it works:** `*args` collects any number of extra **positional** arguments into a tuple named `args` (the name is convention, not a keyword — you could call it `*numbers`).

```python
def describe_pet(**kwargs):
    for key, value in kwargs.items():
        print(f"{key}: {value}")

describe_pet(name="Rex", species="Dog", age=3)
# name: Rex
# species: Dog
# age: 3
```

**How it works:** `**kwargs` collects any number of extra **keyword** arguments into a `dict` named `kwargs`.

🎯 **On the job:** You'll see `*args, **kwargs` constantly in library code (e.g., wrapper/decorator functions, or scikit-learn estimators that forward extra settings) — it means "accept anything else the caller passes and handle it generically."

## Variable Scope: Local vs. Global

A variable defined **inside** a function only exists inside that function (**local scope**) — it disappears once the function finishes, and it can't be seen from outside.

```python
def calculate():
    result = 100   # local to calculate()
    return result

calculate()
print(result)   # NameError: name 'result' is not defined
```

A variable defined **outside** any function (**global scope**) can be *read* inside a function, but if you assign to a same-named variable inside the function, Python creates a new local variable instead of changing the global one — unless you explicitly say otherwise:

```python
counter = 0

def increment_broken():
    counter = counter + 1   # UnboundLocalError! Python sees the assignment
                              # and treats counter as local *throughout* the function

def increment_fixed():
    global counter
    counter = counter + 1

increment_fixed()
print(counter)   # 1
```

⚠️ **Warning:** Relying on `global` to mutate state from inside functions is generally considered poor practice — it makes code harder to reason about (a function's behavior now depends on and changes outside state invisibly). ✅ **Best Practice:** prefer passing values in as arguments and returning new values out, rather than reaching for `global`.

## Docstrings

A **docstring** is a string literal placed as the *first line* inside a function, documenting what it does. Unlike a `#` comment, it's stored by Python and accessible via `help()`.

```python
def calculate_bmi(weight_kg, height_m):
    """
    Calculate Body Mass Index (BMI).

    Args:
        weight_kg (float): Weight in kilograms.
        height_m (float): Height in meters.

    Returns:
        float: The calculated BMI.
    """
    return weight_kg / (height_m ** 2)

print(calculate_bmi(70, 1.75))   # 22.857142857142858
help(calculate_bmi)               # prints the docstring
```

✅ **Best Practice:** Write a docstring for any function whose purpose isn't 100% obvious from its name and parameters — especially anything reused across a project or shared with teammates. This exact `Args:` / `Returns:` style (Google style) is one of the most common conventions in production Python and is what tools like VS Code and Jupyter show as a tooltip.

---

## Hands-On Exercise

**Task:** Write `functions_practice.py` that:
1. Defines a function `apply_discount(price, discount_percent=10)` that returns the price after applying the discount (default 10%).
2. Defines a function `summarize_scores(*scores)` that returns a tuple of `(average, minimum, maximum)` for any number of scores passed in.
3. Calls both functions and prints the results with descriptive f-strings.
4. Includes a docstring on at least one function.

<details>
<summary>✅ Click to see the solution</summary>

```python
def apply_discount(price, discount_percent=10):
    """Return the price after applying a percentage discount."""
    return price * (1 - discount_percent / 100)

def summarize_scores(*scores):
    average = sum(scores) / len(scores)
    return average, min(scores), max(scores)

discounted = apply_discount(200)
print(f"Discounted price: {discounted}")   # Discounted price: 180.0

custom_discount = apply_discount(200, 25)
print(f"25% off price: {custom_discount}")   # 25% off price: 150.0

avg, low, high = summarize_scores(88, 92, 79, 95)
print(f"Average: {avg}, Min: {low}, Max: {high}")   # Average: 88.5, Min: 79, Max: 95
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Forgetting `return` and expecting `print()` to hand back a value | Use `return` for any value the caller needs to use |
| Mutable default arguments (e.g. `def f(items=[]):`) | Never use a mutable object (`list`/`dict`) as a default — it's shared across *all* calls. Use `None` and create the list inside the function instead |
| Using `global` to fix scope errors | Pass values as arguments and return results instead |
| Positional argument soup (`create_user("wesam", 30, True, False)`) | Switch to keyword arguments once you have 3+ parameters |
| No docstring on shared/reusable functions | Add one — future you (and teammates) will need it |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Can define and call a function with parameters and a return value
- [ ] Understand the difference between a parameter and an argument
- [ ] Can use default arguments and keyword arguments
- [ ] Can use `*args` and `**kwargs`
- [ ] Understand local vs. global scope and why `global` is best avoided
- [ ] Can write a docstring
- [ ] Completed the `functions_practice.py` exercise

**Next:** Continue to [`02-modules-and-packages.md`](02-modules-and-packages.md)
