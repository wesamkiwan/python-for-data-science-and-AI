# 📋 Module 04 Cheat Sheet: File I/O, JSON/CSV & APIs

Fast reference for reading/writing files, JSON, CSV, and calling web APIs.

## File Modes

| Mode | Meaning | Existing content |
|---|---|---|
| `"r"` | Read (default) | Reads from start; errors if missing |
| `"w"` | Write | **Erases** existing content |
| `"a"` | Append | Keeps existing, adds to end |
| `"x"` | Exclusive create | Errors if file already exists |

## Reading & Writing Text Files
```python
with open("file.txt", "w") as f:
    f.write("line one\n")

with open("file.txt", "r") as f:
    contents = f.read()          # whole file as one string
    # OR
    lines = f.readlines()          # list of lines, each ending in \n
    # OR
    for line in f:                    # memory-efficient, one line at a time
        print(line.strip())

import os
if os.path.exists("file.txt"):
    ...
try:
    with open("missing.txt") as f:
        ...
except FileNotFoundError:
    print("not found")
```

## JSON
```python
import json

json.dump(data, file_obj, indent=4)    # Python -> JSON, writes to an open FILE
json.dumps(data, indent=4)                # Python -> JSON, returns a STRING

data = json.load(file_obj)          # JSON file -> Python dict/list
data = json.loads(json_string)        # JSON string -> Python dict/list
```
| JSON | Python |
|---|---|
| `{...}` | `dict` |
| `[...]` | `list` |
| `true`/`false` | `True`/`False` |
| `null` | `None` |

`s` suffix = string version (`dumps`/`loads`). No `s` = file version (`dump`/`load`).

## CSV
```python
import csv

# Reading
with open("data.csv", newline="") as f:
    reader = csv.reader(f)              # each row -> list of strings
    header = next(reader)
    for row in reader:
        ...

with open("data.csv", newline="") as f:
    reader = csv.DictReader(f)          # each row -> dict keyed by header (preferred)
    for row in reader:
        print(row["column_name"])

# Writing
with open("out.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "age"])
    writer.writeheader()
    writer.writerows(list_of_dicts)
```
⚠️ Always include `newline=""` in `open()` for CSV files. All CSV values read back are **strings** — cast with `int()`/`float()` if needed.

## Calling a Web API with `requests`
```python
import requests

response = requests.get(url, params={"key": "value"}, timeout=5)

response.status_code       # 200, 404, 500, etc.
response.text                    # raw response body as a string
response.json()                    # parsed JSON body -> Python dict/list
response.url                         # final URL including query params

response.raise_for_status()   # raises requests.HTTPError if status is 4xx/5xx
```

## Robust API Call Pattern
```python
import requests

try:
    response = requests.get(url, timeout=5)
    response.raise_for_status()
    data = response.json()
except requests.HTTPError as e:
    print(f"HTTP error: {e}")
except requests.ConnectionError:
    print("Could not connect.")
except requests.Timeout:
    print("Request timed out.")
```

## HTTP Status Code Ranges

| Range | Meaning |
|---|---|
| 200-299 | Success |
| 300-399 | Redirection |
| 400-499 | Client error (bad request, e.g. `404 Not Found`) |
| 500-599 | Server error |

## Quick Troubleshooting

| Error | Likely Cause | Fix |
|---|---|---|
| `FileNotFoundError` | File doesn't exist / wrong path | Check `os.path.exists()` or catch the exception |
| File content unexpectedly erased | Opened with `"w"` instead of `"a"` or `"r"` | Double-check the mode before writing |
| `json.JSONDecodeError` | Invalid JSON (single quotes, trailing comma) | Validate the JSON text; JSON requires double quotes |
| CSV values behaving like text in math | All CSV values are strings by default | Cast explicitly: `int(row["age"])` |
| Extra blank rows in written CSV (Windows) | Missing `newline=""` in `open()` | Always pass `newline=""` for CSV files |
| `requests.get()` "succeeds" but data looks wrong | Server returned a 4xx/5xx — `requests` doesn't raise automatically | Check `.status_code` or call `.raise_for_status()` |
| Script hangs forever on a request | No `timeout` set | Always pass `timeout=` |

## The "Call an API" Workflow — do this every time
1. Build the request: `requests.get(url, params={...}, timeout=5)`.
2. Wrap it in `try`/`except` catching `HTTPError`, `ConnectionError`, `Timeout`.
3. Call `.raise_for_status()` right after the request.
4. Parse with `.json()` and pull out only the fields you need.
5. If saving for later, `json.dump()` the result to a file.
