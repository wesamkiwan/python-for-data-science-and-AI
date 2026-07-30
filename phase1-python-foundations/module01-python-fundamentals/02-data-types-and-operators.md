# Module 01b: Data Types & Operators

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [01-getting-started.md](01-getting-started.md)

## 🎯 Learning Objectives
- [ ] Identify and use Python's core data types (int, float, str, bool, None)
- [ ] Convert between types (type casting)
- [ ] Use arithmetic, comparison, and logical operators
- [ ] Format strings using f-strings
- [ ] Check a variable's type with `type()`

---

## Module Goal

Master the basic building blocks of data in Python. Every dataset you'll ever load — a CSV of sales numbers, a column of customer names, a `True/False` flag — is ultimately made of these fundamental types.

## Why This Matters on the Job

Type errors (e.g., trying to do math on text) are one of the most common bugs in real data pipelines — especially when reading messy CSV/Excel files where a "number" column accidentally contains text. Understanding types deeply means you'll spot and fix these bugs in seconds instead of hours.

---

## Core Data Types

| Type | Name | Example | Used For |
|---|---|---|---|
| `int` | Integer | `42`, `-7` | Whole numbers: counts, IDs, ages |
| `float` | Floating point | `3.14`, `-0.5` | Decimal numbers: prices, measurements |
| `str` | String | `"hello"` | Text |
| `bool` | Boolean | `True`, `False` | Yes/no, on/off, conditions |
| `NoneType` | None | `None` | "No value" / missing data |

Check any variable's type with the built-in `type()` function:

```python
x = 42
print(type(x))       # <class 'int'>

y = 3.14
print(type(y))       # <class 'float'>

name = "Ada"
print(type(name))    # <class 'str'>

is_active = True
print(type(is_active))  # <class 'bool'>

result = None
print(type(result))   # <class 'NoneType'>
```

### Numbers: `int` and `float`

```python
whole_number = 10          # int
decimal_number = 10.5      # float

# Mixing int and float in an operation always produces a float
total = whole_number + decimal_number
print(total)          # 20.5
print(type(total))    # <class 'float'>
```

💡 **Tip:** `None` is Python's way of representing "nothing" or "no value yet" — very similar to `NULL` in SQL or databases, and you'll see it constantly when working with missing data in Pandas (`NaN` is the numeric cousin of `None` you'll meet in Module 06-07).

### Strings: Text Data

Strings can use single `'...'` or double `"..."` quotes — they're equivalent, just be consistent.

```python
first = 'Ada'
last = "Lovelace"

# String concatenation with +
full_name = first + " " + last
print(full_name)   # Ada Lovelace

# String repetition with *
print("ab" * 3)    # ababab

# Length of a string
print(len(full_name))   # 12

# Common string methods
print(full_name.upper())      # ADA LOVELACE
print(full_name.lower())      # ada lovelace
print(full_name.replace("Ada", "Grace"))  # Grace Lovelace
print("  padded  ".strip())   # "padded" (removes leading/trailing whitespace)
print(full_name.split(" "))   # ['Ada', 'Lovelace']
```

🎯 **On the job:** `.strip()`, `.split()`, and `.replace()` are exactly what you'll use constantly when cleaning messy text data (e.g., stripping whitespace from CSV values, splitting a "First Last" column into two columns).

### f-strings: The Modern Way to Format Strings

An **f-string** (formatted string literal) lets you embed variables directly inside a string using `{ }`. This is the modern, industry-standard way to build strings — prefer it over `+` concatenation.

```python
name = "Wesam"
age = 30

message = f"My name is {name} and I am {age} years old."
print(message)
# My name is Wesam and I am 30 years old.

# You can even do math/expressions inside the braces
print(f"Next year I will be {age + 1}.")
# Next year I will be 31.

# Number formatting: round a float to 2 decimal places
price = 19.98765
print(f"Price: ${price:.2f}")
# Price: $19.99
```

✅ **Best Practice:** Always use f-strings (`f"..."`) over `+` concatenation. They're more readable, faster, and handle type conversion automatically (no more `str(age)` needed).

### Booleans and `None`

```python
is_raining = True
is_sunny = False

print(is_raining)        # True
print(type(is_raining))  # <class 'bool'>

data = None
print(data is None)      # True — always use `is None`, not `== None`
```

⚠️ **Warning:** Use `is None` / `is not None` to check for `None`, never `== None`. This is a real Python convention enforced by linters (`is` checks identity, which is the correct/reliable way to check for `None`).

## Type Casting (Converting Between Types)

Sometimes you need to explicitly convert a value from one type to another:

```python
age_str = "30"
age_int = int(age_str)        # str -> int
print(age_int + 1)             # 31

price_int = 20
price_float = float(price_int) # int -> float
print(price_float)             # 20.0

count = 5
count_str = str(count)         # int -> str
print("Count: " + count_str)   # Count: 5

flag = bool(1)                  # int -> bool (0 is False, anything else is True)
print(flag)                     # True
```

⚠️ **Warning:** `int("30.5")` raises a `ValueError` — you can't directly cast a decimal-looking string to `int`. You must go through `float` first: `int(float("30.5"))` → `30`.

🎯 **On the job:** Type casting failures are one of the most common real-world data bugs — e.g., a CSV "age" column that looks numeric but has a stray text value like `"unknown"` in one row will crash `int()` conversion on the whole column. You'll learn robust ways to handle this in Module 08 (Data Cleaning).

## Operators

### Arithmetic Operators

```python
a, b = 10, 3

print(a + b)   # 13   addition
print(a - b)   # 7    subtraction
print(a * b)   # 30   multiplication
print(a / b)   # 3.333...  division (always returns a float)
print(a // b)  # 3    floor division (rounds down to nearest int)
print(a % b)   # 1    modulo (remainder)
print(a ** b)  # 1000 exponentiation (a to the power of b)
```

💡 **Tip:** `%` (modulo) is extremely useful for checking even/odd (`n % 2 == 0`) or cycling through values — common in data indexing and loops.

### Comparison Operators

Comparison operators always produce a `bool` (`True`/`False`):

```python
print(5 > 3)    # True
print(5 < 3)    # False
print(5 == 5)   # True  (equality check — TWO equals signs)
print(5 != 3)   # True  (not equal)
print(5 >= 5)   # True
print(5 <= 4)   # False
```

⚠️ **Warning:** `=` assigns a value; `==` compares two values. Confusing these (`if x = 5:` instead of `if x == 5:`) is a classic beginner mistake and Python will raise a `SyntaxError` to protect you.

### Logical Operators

Combine multiple `bool` conditions:

```python
age = 25
has_id = True

print(age >= 18 and has_id)   # True  — both must be True
print(age >= 18 or has_id)    # True  — at least one must be True
print(not has_id)              # False — flips True/False
```

| Operator | Meaning | Example |
|---|---|---|
| `and` | Both conditions must be `True` | `age >= 18 and has_id` |
| `or` | At least one condition must be `True` | `is_admin or is_owner` |
| `not` | Flips a boolean | `not is_active` |

---

## Hands-On Exercise

**Task:** Write `shopping_cart.py` that:
1. Stores a product name (`str`), price (`float`), and quantity (`int`).
2. Calculates the total cost (`price * quantity`).
3. Uses an f-string to print: `"3x Notebook @ $4.50 = $13.50"` (format the total to 2 decimal places).
4. Prints whether the total is over $10 using a comparison operator.

<details>
<summary>✅ Click to see the solution</summary>

```python
product_name = "Notebook"
price = 4.50
quantity = 3

total = price * quantity

print(f"{quantity}x {product_name} @ ${price} = ${total:.2f}")
print(f"Is the total over $10? {total > 10}")
```

**Expected output:**
```
3x Notebook @ $4.5 = $13.50
Is the total over $10? True
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| `"5" + 5` → `TypeError` | Cast explicitly: `int("5") + 5`, or better, use an f-string |
| `int("3.5")` → `ValueError` | Go through `float()` first: `int(float("3.5"))` |
| Using `== None` | Use `is None` |
| Confusing `=` and `==` | `=` assigns, `==` compares |
| String concatenation with `+` everywhere | Prefer f-strings for readability |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Can identify int, float, str, bool, and None
- [ ] Comfortable casting between types
- [ ] Can write f-strings with formatting (e.g., `:.2f`)
- [ ] Understand arithmetic, comparison, and logical operators
- [ ] Completed the `shopping_cart.py` exercise

**Next:** Continue to [`03-control-flow-and-collections.md`](03-control-flow-and-collections.md)
