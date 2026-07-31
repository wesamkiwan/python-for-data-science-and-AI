# Module 04b: Working with JSON & CSV

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [01-reading-and-writing-files.md](01-reading-and-writing-files.md)

## 🎯 Learning Objectives
- [ ] Explain what JSON is and why it's the standard format for data exchange
- [ ] Read and write JSON files/strings with the `json` module
- [ ] Read and write CSV files with the `csv` module
- [ ] Explain why Pandas will replace most manual CSV/JSON handling from Module 07 onward

---

## Module Goal

Learn to work with the two data formats you will encounter constantly in real work: **JSON** (the near-universal format for APIs and config files) and **CSV** (the near-universal format for tabular/spreadsheet data). Both build directly on the file-handling skills from the last lesson.

## Why This Matters on the Job

Nearly every API you call returns JSON. Nearly every spreadsheet export or database dump you receive is a CSV. You will read and write both formats constantly — for config files, for caching API responses, for quick data exports — even after you start using Pandas for the heavy lifting (Pandas' `pd.read_json()` and `pd.read_csv()` are built on the exact same underlying ideas you're learning here, just with far more convenience for large, tabular data).

---

## JSON: JavaScript Object Notation

**JSON** is a lightweight, text-based format for representing structured data — despite the name, it's language-agnostic and used everywhere, not just in JavaScript. If you've used a Python `dict`, JSON will look immediately familiar:

```json
{
    "name": "Ada Lovelace",
    "age": 36,
    "is_active": true,
    "skills": ["Python", "Mathematics"],
    "address": {
        "city": "London",
        "country": "UK"
    }
}
```

This maps almost one-to-one onto Python's `dict`, `list`, `str`, `int`/`float`, `bool`, and `None` (JSON's `null`).

| JSON type | Python equivalent |
|---|---|
| object `{...}` | `dict` |
| array `[...]` | `list` |
| string | `str` |
| number | `int` or `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

### Writing JSON: `json.dump()` and `json.dumps()`

```python
import json

person = {
    "name": "Ada Lovelace",
    "age": 36,
    "is_active": True,
    "skills": ["Python", "Mathematics"]
}

# Write directly to a file
with open("person.json", "w") as file:
    json.dump(person, file, indent=4)

# Or convert to a JSON-formatted STRING (no file involved)
json_string = json.dumps(person, indent=4)
print(json_string)
```

**How it works:** `json.dump(data, file)` writes `data` (a Python `dict`/`list`) as JSON text directly into an already-open file. `json.dumps(data)` (note the trailing `s` — "dump string") instead returns the JSON text as a Python `str`, useful when you need the text itself rather than a file (e.g., to send in an API request body). `indent=4` pretty-prints it with readable indentation — omit it for compact, minified output.

### Reading JSON: `json.load()` and `json.loads()`

```python
import json

with open("person.json", "r") as file:
    data = json.load(file)     # parses JSON from a file into a Python dict

print(data["name"])       # Ada Lovelace
print(data["skills"])       # ['Python', 'Mathematics']
print(type(data))             # <class 'dict'>

# Parsing a JSON STRING instead of a file
json_text = '{"city": "London", "population": 8982000}'
parsed = json.loads(json_text)   # note the trailing "s" again
print(parsed["city"])              # London
```

💡 **Tip:** Remember the pattern: **no `s`** (`dump`/`load`) works with **file objects**; **with `s`** (`dumps`/`loads`) works with **strings**. This mirrors exactly how you'll call `json.loads()` on the text of an API response in the next lesson.

⚠️ **Warning:** `json.load()`/`json.loads()` raises `json.JSONDecodeError` (a subclass of `ValueError`) if the text isn't valid JSON — e.g., a trailing comma, or single quotes instead of double quotes (JSON *requires* double quotes for strings, unlike Python, which accepts either).

## CSV: Comma-Separated Values

**CSV** stores tabular data as plain text — each line is a row, and values within a row are separated by commas (or occasionally another delimiter, like a tab or semicolon).

```csv
name,age,city
Ada,36,London
Grace,85,New York
Alan,41,Manchester
```

### Reading CSV with the `csv` Module

```python
import csv

with open("people.csv", "r", newline="") as file:
    reader = csv.reader(file)
    header = next(reader)          # grabs the first row (column names) separately
    print(header)                     # ['name', 'age', 'city']

    for row in reader:
        print(row)                     # each row is a plain LIST of strings
```
```
['name', 'age', 'city']
['Ada', '36', 'London']
['Grace', '85', 'New York']
['Alan', '41', 'Manchester']
```

⚠️ **Warning:** Every value read by `csv.reader` is a **string**, even `"36"` — CSV has no concept of data types. If you need `age` as a number, you must convert it yourself with `int()`, which is exactly the kind of tedious, error-prone step Pandas automates for you later.

### Reading CSV as Dictionaries: `csv.DictReader`

Far more convenient — reads each row as a `dict` keyed by the header row automatically:

```python
import csv

with open("people.csv", "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row)                        # {'name': 'Ada', 'age': '36', 'city': 'London'}
        print(row["name"], row["city"])     # Ada London
```

✅ **Best Practice:** Prefer `csv.DictReader` over plain `csv.reader` in almost every case — accessing `row["age"]` by name is far more readable and less error-prone than `row[1]` by position, especially if column order ever changes.

### Writing CSV with `csv.writer` and `csv.DictWriter`

```python
import csv

people = [
    {"name": "Ada", "age": 36, "city": "London"},
    {"name": "Grace", "age": 85, "city": "New York"},
]

with open("output.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "age", "city"])
    writer.writeheader()          # writes the column header row
    writer.writerows(people)        # writes all the data rows
```

💡 **Tip:** `newline=""` in `open()` is required boilerplate on every platform when reading/writing CSV files — without it, Windows can insert extra blank lines between rows. Just remember to always include it for CSV work.

## Why Pandas Will Take Over From Here

Manually writing `csv.DictReader` loops and converting every string to the right type works, but it's tedious and error-prone at scale — missing values, mixed types, and large files all require extra hand-written logic. Starting in Module 07, you'll replace nearly all of this with one line:

```python
import pandas as pd
df = pd.read_csv("people.csv")    # auto-detects types, handles missing values, and more
```

🎯 **On the job:** You're learning the manual version now so that when Pandas does all of this automatically, you understand *what* it's actually doing underneath — which makes debugging a `pd.read_csv()` type-inference issue or a JSON parsing error far less mysterious later.

---

## Hands-On Exercise

**Task:** Write `contacts.py` that:
1. Creates a Python list of at least 3 dictionaries, each representing a contact with `name`, `email`, and `phone` keys.
2. Writes that list to `contacts.json` using `json.dump()` with `indent=4`.
3. Writes the same list to `contacts.csv` using `csv.DictWriter`.
4. Reads `contacts.json` back and prints just the names.
5. Reads `contacts.csv` back using `csv.DictReader` and prints just the emails.

<details>
<summary>✅ Click to see the solution</summary>

```python
import json
import csv

contacts = [
    {"name": "Ada Lovelace", "email": "ada@example.com", "phone": "555-0100"},
    {"name": "Grace Hopper", "email": "grace@example.com", "phone": "555-0101"},
    {"name": "Alan Turing", "email": "alan@example.com", "phone": "555-0102"},
]

with open("contacts.json", "w") as file:
    json.dump(contacts, file, indent=4)

with open("contacts.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=["name", "email", "phone"])
    writer.writeheader()
    writer.writerows(contacts)

with open("contacts.json", "r") as file:
    loaded_contacts = json.load(file)
    for contact in loaded_contacts:
        print(contact["name"])

with open("contacts.csv", "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["email"])
```

**Expected output:**
```
Ada Lovelace
Grace Hopper
Alan Turing
ada@example.com
grace@example.com
alan@example.com
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Confusing `dump`/`load` (files) with `dumps`/`loads` (strings) | Remember: trailing `s` = string version |
| Forgetting all CSV values are strings | Cast with `int()`/`float()` explicitly when you need numbers |
| Omitting `newline=""` when opening a CSV file | Always include it — prevents extra blank rows on Windows |
| Using single quotes in hand-written JSON text | JSON requires double quotes for strings — invalid otherwise |
| Accessing CSV rows by position (`row[1]`) | Prefer `csv.DictReader` and access by column name |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Understand JSON's structure and its mapping to Python types
- [ ] Can read/write JSON with `json.load`/`dump` and `json.loads`/`dumps`
- [ ] Can read/write CSV with `csv.reader`/`writer` and `csv.DictReader`/`DictWriter`
- [ ] Understand why Pandas will replace most manual CSV/JSON code later
- [ ] Completed the `contacts.py` exercise

**Next:** Continue to [`03-working-with-apis.md`](03-working-with-apis.md)
