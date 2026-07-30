# Module 01c: Control Flow & Collections

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [02-data-types-and-operators.md](02-data-types-and-operators.md)

## 🎯 Learning Objectives
- [ ] Write conditional logic with `if` / `elif` / `else`
- [ ] Write `for` and `while` loops, including `break` and `continue`
- [ ] Use Python's four core collection types: `list`, `tuple`, `dict`, `set`
- [ ] Choose the right collection type for a given problem
- [ ] Use list comprehensions for concise, readable code

---

## Module Goal

Learn how to make decisions in code (conditionals), repeat actions (loops), and store groups of related data (collections). These three skills combined let you write real, useful programs — and they map directly onto how you'll manipulate rows, columns, and records once you reach Pandas.

## Why This Matters on the Job

Every data pipeline is fundamentally: loop over records → check a condition → transform or filter → store the result. A `list` of customer records, a `dict` mapping user IDs to names, filtering rows where `revenue > 1000` — these patterns appear constantly, whether you're writing raw Python or (later) Pandas operations that do the same thing at scale.

---

## Conditional Logic: `if` / `elif` / `else`

```python
age = 20

if age < 13:
    print("Child")
elif age < 20:
    print("Teenager")
else:
    print("Adult")
```

**How it works:** Python checks conditions **top to bottom** and runs the first block whose condition is `True`, then skips the rest. `else` catches everything not matched above it. `elif` (short for "else if") lets you chain multiple conditions.

**Expected output:** `Adult` (age is 20, which is not `< 13` and not `< 20`, so it falls to `else`)

💡 **Tip:** You can nest conditionals, but more than 2-3 levels of nesting usually signals your logic should be refactored into a function (Module 02).

## Loops

### `for` Loops: Repeat for Each Item

```python
fruits = ["apple", "banana", "cherry"]

for fruit in fruits:
    print(fruit)
```
```
apple
banana
cherry
```

**How it works:** `for fruit in fruits` means "for each item in the `fruits` list, temporarily name it `fruit` and run the indented block."

Use `range()` to loop a specific number of times:

```python
for i in range(5):       # 0, 1, 2, 3, 4 (starts at 0, stops before 5)
    print(i)

for i in range(2, 10, 2):  # start=2, stop=10 (exclusive), step=2
    print(i)               # 2, 4, 6, 8
```

### `while` Loops: Repeat While a Condition Holds

```python
count = 0
while count < 3:
    print(f"Count is {count}")
    count += 1     # shorthand for count = count + 1
```
```
Count is 0
Count is 1
Count is 2
```

⚠️ **Warning:** If you forget to update the loop's condition variable (`count += 1` here), you get an **infinite loop** that never stops. Always double-check `while` loops have a clear exit path.

✅ **Best Practice:** Prefer `for` loops when you know how many items you're iterating over (very common in data work). Use `while` loops when you're repeating "until some condition changes" (e.g., waiting for a value or retrying an API call).

### `break` and `continue`

```python
for i in range(10):
    if i == 5:
        break          # exits the loop entirely
    print(i)
# Prints 0 1 2 3 4, then stops

for i in range(5):
    if i == 2:
        continue       # skips just this iteration
    print(i)
# Prints 0 1 3 4 (skips 2)
```

---

## Collections: Storing Groups of Data

Python has four core built-in collection types. Choosing the right one is a real design decision you'll make constantly.

| Type | Ordered? | Mutable (changeable)? | Duplicates allowed? | Syntax |
|---|:---:|:---:|:---:|---|
| `list` | ✅ | ✅ | ✅ | `[1, 2, 3]` |
| `tuple` | ✅ | ❌ | ✅ | `(1, 2, 3)` |
| `dict` | ✅ (insertion order) | ✅ | Keys: ❌ / Values: ✅ | `{"a": 1, "b": 2}` |
| `set` | ❌ | ✅ | ❌ | `{1, 2, 3}` |

### Lists: Ordered, Changeable Collections

The most commonly used collection — an ordered sequence of items you can add to, remove from, and modify.

```python
scores = [85, 92, 78, 90]

print(scores[0])       # 85   (indexing starts at 0!)
print(scores[-1])       # 90   (negative index = from the end)
print(scores[1:3])      # [92, 78]  (slicing: index 1 up to, not including, 3)

scores.append(88)       # add to the end
print(scores)            # [85, 92, 78, 90, 88]

scores[0] = 100          # modify by index
print(scores)             # [100, 92, 78, 90, 88]

scores.remove(78)         # remove by value
print(len(scores))         # 4

print(sorted(scores))       # [88, 90, 92, 100] — new sorted list, doesn't modify original
print(sum(scores) / len(scores))  # average
```

⚠️ **Warning:** Python indexing starts at **0**, not 1. `scores[0]` is the *first* item. This trips up nearly every beginner at least once.

### Tuples: Ordered, Unchangeable Collections

Like a list, but **immutable** — once created, it cannot be changed. Use tuples for fixed data that shouldn't accidentally be modified (e.g., coordinates, RGB color values).

```python
point = (4, 5)
print(point[0])    # 4

# point[0] = 10   # This would raise: TypeError: 'tuple' object does not support item assignment
```

💡 **Tip:** Tuples are also slightly faster and signal intent — "this data is fixed" — which makes code easier to reason about. You'll see them used for function return values that bundle multiple results (Module 02).

### Dictionaries: Key-Value Pairs

A `dict` maps unique **keys** to **values** — like a real dictionary maps words to definitions. This is one of the most important data structures in all of Python (and closely mirrors a single row/record of data, or a JSON object you'll meet in Module 04).

```python
person = {
    "name": "Ada Lovelace",
    "age": 36,
    "occupation": "Mathematician"
}

print(person["name"])          # Ada Lovelace
print(person.get("age"))        # 36
print(person.get("email", "N/A"))  # N/A — .get() returns a default instead of crashing

person["age"] = 37              # update a value
person["email"] = "ada@example.com"  # add a new key
print(person)

for key, value in person.items():
    print(f"{key}: {value}")
```

⚠️ **Warning:** `person["email"]` raises a `KeyError` if the key doesn't exist. Use `.get("key", default_value)` when the key might be missing — this is the single most common `dict` bug in real code.

### Sets: Unique, Unordered Collections

A `set` automatically removes duplicates and is optimized for fast membership checks (`in`).

```python
unique_ids = {101, 102, 103, 101, 102}
print(unique_ids)         # {101, 102, 103} — duplicates removed automatically

print(103 in unique_ids)   # True — very fast lookup, even for huge sets

a = {1, 2, 3}
b = {2, 3, 4}
print(a & b)     # {2, 3}      intersection
print(a | b)     # {1,2,3,4}   union
print(a - b)     # {1}         difference
```

🎯 **On the job:** Sets are the fastest way to de-duplicate a list of IDs or check "has this user already been processed?" against thousands of records.

## Choosing the Right Collection

| Need to... | Use |
|---|---|
| Keep items in order and allow duplicates/changes | `list` |
| Keep fixed data that should never change | `tuple` |
| Look up values by a meaningful name/key | `dict` |
| Store unique items, check membership fast | `set` |

## List Comprehensions (Bonus: Writing Pythonic Code)

A **list comprehension** builds a new list in a single, readable line — instead of a multi-line loop with `.append()`.

```python
numbers = [1, 2, 3, 4, 5]

# Traditional loop
squares = []
for n in numbers:
    squares.append(n ** 2)

# Equivalent list comprehension
squares = [n ** 2 for n in numbers]
print(squares)   # [1, 4, 9, 16, 25]

# With a filtering condition
even_squares = [n ** 2 for n in numbers if n % 2 == 0]
print(even_squares)   # [4, 16]
```

✅ **Best Practice:** List comprehensions are considered more "Pythonic" (idiomatic) than manual loops for simple transformations, and you'll see them everywhere in real codebases. Don't force complex logic into one, though — if it's hard to read on one line, use a regular loop instead.

---

## Hands-On Exercise

**Task:** Write `grade_report.py` that:
1. Stores a `dict` of student names mapped to their score (e.g., `{"Ada": 92, "Grace": 85, "Alan": 76}`).
2. Loops over the dictionary and prints each student's name and a letter grade (A: 90+, B: 80-89, C: below 80) using `if/elif/else`.
3. Uses a list comprehension to build a list of just the names of students who scored an A.

<details>
<summary>✅ Click to see the solution</summary>

```python
scores = {"Ada": 92, "Grace": 85, "Alan": 76}

for name, score in scores.items():
    if score >= 90:
        grade = "A"
    elif score >= 80:
        grade = "B"
    else:
        grade = "C"
    print(f"{name}: {score} ({grade})")

a_students = [name for name, score in scores.items() if score >= 90]
print(f"A students: {a_students}")
```

**Expected output:**
```
Ada: 92 (A)
Grace: 85 (B)
Alan: 76 (C)
A students: ['Ada']
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Off-by-one errors with indexing/`range()` | Remember: 0-indexed, `range(stop)` excludes `stop` |
| Infinite `while` loops | Always confirm the loop condition will eventually become `False` |
| `KeyError` on missing dict key | Use `.get("key", default)` |
| Using a `list` when order doesn't matter and duplicates aren't wanted | Use a `set` instead — faster and clearer intent |
| Overly complex list comprehensions | If it's unreadable on one line, use a regular loop |

---

## ✅ Module 01 Completion Checklist
- [ ] Comfortable with `if` / `elif` / `else`
- [ ] Can write `for` and `while` loops, including `break`/`continue`
- [ ] Know the difference between `list`, `tuple`, `dict`, and `set` and when to use each
- [ ] Can write a basic list comprehension
- [ ] Completed the `grade_report.py` exercise
- [ ] Reviewed [`module01-cheatsheet.md`](module01-cheatsheet.md)
- [ ] Reviewed [`module01-interview.md`](module01-interview.md)
- [ ] Browsed [`module01-references.md`](module01-references.md)

**Next Step:** Module 02 — Functions, Modules & Error Handling (`phase1-python-foundations/module02-functions-modules-errors/`)
