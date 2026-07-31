# 📋 Module 02 Cheat Sheet: Functions, Modules & Error Handling

Fast reference for defining functions, importing code, and handling errors.

## Defining & Calling Functions
```python
def greet(name, greeting="Hello"):   # "greeting" has a default value
    """One-line docstring describing what this does."""
    return f"{greeting}, {name}!"

greet("Ada")                    # positional -> Hello, Ada!
greet(name="Ada", greeting="Hi")  # keyword -> Hi, Ada!
```

## Multiple Return Values
```python
def min_max(nums):
    return min(nums), max(nums)   # returns a tuple

low, high = min_max([3, 1, 4, 1, 5])   # unpack directly
```

## `*args` / `**kwargs`
```python
def total(*args):           # args -> tuple of positional extras
    return sum(args)

def describe(**kwargs):      # kwargs -> dict of keyword extras
    for k, v in kwargs.items():
        print(k, v)

total(1, 2, 3)                # 6
describe(name="Rex", age=3)    # name: Rex \n age: 3
```

## Scope
```python
count = 0

def bump():
    global count       # required to MODIFY a global from inside a function
    count += 1
```
| Scope | Where defined | Visible where |
|---|---|---|
| Local | Inside a function | Only inside that function |
| Global | Top level of a file | Readable everywhere; needs `global` keyword to modify from inside a function |

## Docstring (Google style)
```python
def calculate_bmi(weight_kg, height_m):
    """
    Calculate BMI.

    Args:
        weight_kg (float): Weight in kilograms.
        height_m (float): Height in meters.

    Returns:
        float: The calculated BMI.
    """
    return weight_kg / (height_m ** 2)
```

## Imports
```python
import math                   # prefix access: math.sqrt(16)
import numpy as np              # aliased: np.array(...)
from math import sqrt, pi        # direct names: sqrt(16)
from math import *                 # ❌ avoid — pollutes namespace
```

| Package | Standard alias |
|---|---|
| `numpy` | `np` |
| `pandas` | `pd` |
| `matplotlib.pyplot` | `plt` |
| `seaborn` | `sns` |

## Common Standard Library Modules
```python
import math       # math.sqrt, math.ceil, math.floor
import random      # random.randint(a, b), random.choice(list)
import datetime     # datetime.date.today()
import os             # os.getcwd(), os.path.join(...)
```

## Error Handling
```python
try:
    risky_thing()
except ValueError as e:        # catch specific type, capture message
    print(f"Bad value: {e}")
except (TypeError, KeyError):   # catch multiple types at once
    print("Type or key problem.")
else:
    print("Ran with no error.")   # only if try succeeded
finally:
    print("Always runs.")          # cleanup, error or not
```

## Raising Your Own Errors
```python
def set_age(age):
    if age < 0:
        raise ValueError("Age cannot be negative.")
    return age
```

## Batch-Processing-Without-Crashing Pattern
```python
valid = []
for raw in raw_values:
    try:
        valid.append(int(raw))
    except ValueError:
        print(f"Skipping invalid value: {raw!r}")
```

## Quick Troubleshooting

| Error | Likely Cause | Fix |
|---|---|---|
| `UnboundLocalError` | Assigning to a global-named variable inside a function without `global` | Add `global var_name`, or better: pass in / return instead |
| `ModuleNotFoundError` | Package not installed in active environment | `pip install <package>` (see Module 05) |
| `TypeError: f() missing 1 required positional argument` | Called a function without all required arguments | Check the function's signature/defaults |
| Bare `except:` hides a real bug | Catching everything, including typos | Catch the specific exception type you expect |
| `ZeroDivisionError` uncaught | Dividing by a value that can be 0 | Wrap in `try`/`except ZeroDivisionError` |

## The "New Function" Workflow — do this every time you write one
1. Name it with a clear verb (`calculate_total`, not `data2`).
2. Decide its parameters — use defaults for optional ones, keyword-only style for 3+.
3. Write a one-line (or Args/Returns) docstring.
4. `return` the result — don't just `print()` it.
5. Consider: can any input cause an exception? If yes, wrap the risky part in `try`/`except`.
