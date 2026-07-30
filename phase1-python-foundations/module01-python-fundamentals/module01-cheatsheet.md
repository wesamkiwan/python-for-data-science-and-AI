# 📋 Module 01 Cheat Sheet: Python Fundamentals

Fast reference for Python basics — syntax, types, operators, control flow, and collections.

## Running Python
```bash
python --version          # check installed version
python                    # start interactive REPL
python script.py          # run a script file
```

## Variables & Types
```python
name = "Ada"        # str
age = 36            # int
gpa = 3.9            # float
active = True         # bool
data = None            # NoneType

type(name)             # <class 'str'>
```

## Type Casting
```python
int("42")        # 42
float("3.14")     # 3.14
str(42)            # "42"
bool(1)             # True
int(float("3.5"))    # 3 (must go through float for decimal strings)
```

## f-strings (preferred string formatting)
```python
f"Hello, {name}!"
f"Price: ${price:.2f}"      # 2 decimal places
f"{value:,}"                 # thousands separator
f"{value:>10}"                # right-align in 10 chars
```

## Operators

| Category | Operators |
|---|---|
| Arithmetic | `+ - * / // % **` |
| Comparison | `== != > < >= <=` |
| Logical | `and  or  not` |
| Assignment shorthand | `+= -= *= /=` |

## Control Flow
```python
if condition:
    ...
elif other_condition:
    ...
else:
    ...

for item in iterable:
    ...

while condition:
    ...
    break       # exit loop
    continue    # skip to next iteration

for i in range(5):        # 0,1,2,3,4
for i in range(2, 10, 2):  # 2,4,6,8
```

## Collections Decision Table

| Need | Use | Example |
|---|---|---|
| Ordered, changeable, duplicates OK | `list` | `[1, 2, 3]` |
| Ordered, fixed/unchangeable | `tuple` | `(1, 2, 3)` |
| Key → value lookup | `dict` | `{"a": 1}` |
| Unique items, fast membership check | `set` | `{1, 2, 3}` |

## Lists
```python
lst = [1, 2, 3]
lst[0]              # first item (0-indexed)
lst[-1]              # last item
lst[1:3]              # slice: index 1 up to (not incl.) 3
lst.append(4)          # add to end
lst.remove(2)            # remove by value
len(lst)                  # length
sorted(lst)                # new sorted list
sum(lst) / len(lst)         # average
[x**2 for x in lst]           # list comprehension
[x for x in lst if x > 1]      # comprehension with filter
```

## Dictionaries
```python
d = {"name": "Ada", "age": 36}
d["name"]                    # "Ada" — raises KeyError if missing
d.get("email", "N/A")          # safe lookup with default
d["email"] = "a@b.com"           # add/update key
for k, v in d.items():              # loop over key-value pairs
    print(k, v)
```

## Sets
```python
s = {1, 2, 3}
s.add(4)
3 in s                # fast membership check -> True
a & b                  # intersection
a | b                   # union
a - b                    # difference
```

## Quick Troubleshooting

| Error | Likely Cause | Fix |
|---|---|---|
| `IndentationError` | Mixed tabs/spaces or wrong indent level | Use 4 spaces consistently |
| `NameError` | Variable used before assignment / typo | Check spelling & define before use |
| `TypeError: can only concatenate str` | Mixing `str` + `int` with `+` | Use f-strings or cast with `str()` |
| `ValueError: invalid literal for int()` | Casting a non-numeric string | Validate/clean data before casting |
| `KeyError` | Dict key doesn't exist | Use `.get(key, default)` |
| `IndexError: list index out of range` | Index beyond list length | Check `len()` before indexing |

## The "New Script" Workflow — do this every time you start a Python file
1. Add a one-line comment describing what the script does.
2. Declare your variables with clear `snake_case` names.
3. Write the logic (conditionals/loops).
4. `print()` intermediate results while developing — remove/replace with proper output before finishing.
5. Run with `python filename.py` and check the output matches what you expect.
