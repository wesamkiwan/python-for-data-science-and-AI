# Module 02b: Modules & Packages — Organizing and Reusing Code

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 45min | **Prerequisites:** [01-functions.md](01-functions.md)

## 🎯 Learning Objectives
- [ ] Explain what a module and a package are
- [ ] Import modules and specific names using different `import` styles
- [ ] Use several core Python standard library modules
- [ ] Understand, at a high level, what third-party packages and `pip` provide
- [ ] Organize your own code into a reusable module

---

## Module Goal

Learn how Python code is organized beyond a single file — how to reuse code you (or someone else) already wrote by **importing** it, and how the standard library and third-party packages (like the ones you'll use constantly from Module 06 onward: NumPy, Pandas, scikit-learn) fit into this picture.

## Why This Matters on the Job

You will never write a real data science project as one giant file. You'll split code across files (`data_loader.py`, `model.py`, `utils.py`) and import standard-library and third-party tools constantly — `import pandas as pd` is likely the single most-typed line of code in this entire field. Understanding `import` mechanics now means Module 05 (environments, `pip`) and every module after it will make sense immediately.

---

## What Is a Module?

A **module** is simply a `.py` file containing Python code (functions, variables, classes) that you can import and reuse elsewhere. You've already been using modules without necessarily naming them that way.

**Example: create your own module.**

`math_utils.py`:
```python
def square(n):
    """Return n squared."""
    return n ** 2

def cube(n):
    """Return n cubed."""
    return n ** 3

PI = 3.14159
```

`main.py` (in the same folder):
```python
import math_utils

print(math_utils.square(4))    # 16
print(math_utils.cube(3))       # 27
print(math_utils.PI)              # 3.14159
```

**How it works:** `import math_utils` tells Python to run `math_utils.py` once and make everything defined in it accessible through the `math_utils.` prefix.

## What Is a Package?

A **package** is a folder of related modules, grouped together (typically containing an `__init__.py` file, which can be empty — it just tells Python "treat this folder as importable"). NumPy, Pandas, and scikit-learn are all packages — each is a folder full of modules, distributed together and installed with one `pip install` command.

```
my_project/
├── main.py
└── utils/
    ├── __init__.py
    ├── math_utils.py
    └── string_utils.py
```

```python
from utils import math_utils
print(math_utils.square(5))   # 25
```

💡 **Tip:** You don't need to build your own packages yet — just recognize the pattern. Every `import pandas` or `import sklearn` you write later is importing a package built exactly this way.

## Import Styles

There are several ways to import, each with a slightly different tradeoff:

```python
# 1. Import the whole module, access with a prefix
import math
print(math.sqrt(16))     # 4.0

# 2. Import the whole module with a shorter alias (very common for big libraries)
import numpy as np        # you'll type this constantly from Module 06 onward
# print(np.array([1, 2, 3]))

# 3. Import specific names directly — no prefix needed
from math import sqrt, pi
print(sqrt(16))    # 4.0
print(pi)            # 3.141592653589793

# 4. Import everything from a module (generally avoided)
from math import *
print(sqrt(25))   # 5.0
```

⚠️ **Warning:** Avoid `from module import *` in real code. It dumps every name from that module into your file's namespace, making it unclear where a function came from and risking silent name collisions (e.g., if both `math` and your own code define `pi`, the last import silently wins). ✅ **Best Practice:** use `import module`, `import module as alias`, or `from module import specific_name`.

🎯 **On the job:** You'll see the same handful of aliases everywhere — memorize them now, they're near-universal conventions:

| Import | Alias |
|---|---|
| `import numpy as np` | `np` |
| `import pandas as pd` | `pd` |
| `import matplotlib.pyplot as plt` | `plt` |
| `import seaborn as sns` | `sns` |

## The Python Standard Library

Python ships with a huge collection of built-in modules — no installation needed. A few you'll use constantly:

```python
import math
print(math.sqrt(16))       # 4.0
print(math.ceil(4.1))       # 5
print(math.floor(4.9))       # 4

import random
print(random.randint(1, 10))    # random int between 1 and 10 (inclusive)
print(random.choice(["a", "b", "c"]))   # randomly picks one

import datetime
today = datetime.date.today()
print(today)                     # e.g. 2026-07-31

import os
print(os.getcwd())               # prints your current working directory
```

💡 **Tip:** Whenever you need to do something common (date math, random sampling, file paths), check the [standard library docs](https://docs.python.org/3/library/) first — there's a good chance Python already has a built-in module for it before you reach for a third-party package.

## Third-Party Packages (Preview)

The standard library covers general-purpose needs, but data science relies on **third-party packages** — code written by the community and installed via `pip` (Python's package installer), which you'll set up properly in Module 05:

```bash
pip install numpy pandas
```

```python
import numpy as np
import pandas as pd

arr = np.array([1, 2, 3])
df = pd.DataFrame({"name": ["Ada", "Grace"], "score": [92, 88]})
```

💡 **Tip:** Don't install these yet if you haven't reached Module 05/06 — this is just so `import numpy as np` doesn't look unfamiliar when you get there. The full setup (virtual environments, `pip`, `requirements.txt`) is covered properly in Module 05.

---

## Hands-On Exercise

**Task:**
1. Create a file `string_utils.py` containing two functions: `shout(text)` (returns the text uppercased with a `"!"` appended) and `count_words(text)` (returns the number of words, using `.split()`).
2. Create a second file `main.py` in the same folder that imports `string_utils` and calls both functions on a sentence of your choice.
3. Separately, in `main.py`, import the standard library `random` module and print a random word chosen from a list of 4 words you define.

<details>
<summary>✅ Click to see the solution</summary>

`string_utils.py`:
```python
def shout(text):
    """Return the text uppercased with an exclamation mark appended."""
    return text.upper() + "!"

def count_words(text):
    """Return the number of whitespace-separated words in text."""
    return len(text.split())
```

`main.py`:
```python
import string_utils
import random

sentence = "python makes data science approachable"

print(string_utils.shout(sentence))         # PYTHON MAKES DATA SCIENCE APPROACHABLE!
print(string_utils.count_words(sentence))    # 5

words = ["pandas", "numpy", "sklearn", "pytorch"]
print(random.choice(words))    # one of the four, chosen at random
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| `from module import *` | Import specific names or use `import module as alias` instead |
| `ModuleNotFoundError: No module named 'numpy'` | The package isn't installed in your active environment — covered fully in Module 05 |
| Naming your own file `random.py` or `math.py` | Never name a file the same as a standard library module — it shadows the real one and breaks imports |
| Not using the community-standard alias (`import pandas as p`) | Stick to conventional aliases (`pd`, `np`, `plt`) — code reviewers and Stack Overflow answers all assume them |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Understand the difference between a module and a package
- [ ] Comfortable with all four `import` styles and when to use each
- [ ] Used at least 3 standard library modules (`math`, `random`, `datetime`, `os`)
- [ ] Understand at a high level what `pip` and third-party packages are for
- [ ] Completed the `string_utils.py` / `main.py` exercise

**Next:** Continue to [`03-error-handling.md`](03-error-handling.md)
