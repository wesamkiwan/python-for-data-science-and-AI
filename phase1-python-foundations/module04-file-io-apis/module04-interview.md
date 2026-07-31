# 🎤 Module 04 Interview Prep: File I/O, JSON/CSV & APIs

## Conceptual Questions

### 🟢 Beginner

**Q: Why should you always use `with open(...)` instead of `open()` and manually calling `.close()`?**
> A: `with` is a context manager — it guarantees the file is closed automatically when the block ends, even if an exception occurs partway through. If you manually call `.close()` at the end of the code and an error happens before reaching that line, the file is left open, which can leak resources or leave writes incomplete. `with` removes that risk entirely.

**Q: What's the difference between `"w"` and `"a"` file modes?**
> A: `"w"` (write) erases any existing content in the file the moment it's opened, then writes fresh. `"a"` (append) keeps existing content and adds new writes to the end of the file. Using `"w"` when you meant `"a"` is a common way to accidentally destroy existing data.

**Q: What Python types does a JSON object map to, and what does a JSON array map to?**
> A: A JSON object (`{...}`) maps to a Python `dict`. A JSON array (`[...]`) maps to a Python `list`. JSON's `true`/`false`/`null` map to Python's `True`/`False`/`None`. This near-one-to-one mapping is why `json.load()`/`json.loads()` can convert JSON text directly into native Python data structures.

### 🟡 Intermediate

**Q: What's the difference between `json.dump()` and `json.dumps()` (and `load`/`loads`)?**
> A: The versions without an `s` (`dump`, `load`) work directly with an already-open **file object** — `json.dump(data, file)` writes JSON into that file, `json.load(file)` reads and parses JSON from it. The versions with an `s` (`dumps`, `loads`) work with plain Python **strings** instead — `json.dumps(data)` returns a JSON-formatted string, and `json.loads(text)` parses a JSON string into Python data. The `s` in each name stands for "string."

**Q: Why does `requests.get()` NOT raise an exception when a server returns a 404 or 500 status code?**
> A: From the HTTP client's perspective, the request itself succeeded — a response came back from the server, it just happens to represent an error condition. `requests` treats "getting any response" as success and leaves it to you to inspect `.status_code` or explicitly call `.raise_for_status()`, which converts a 4xx/5xx status into a `requests.HTTPError` exception you can catch.

**Q: Why does `csv.DictReader` return every value as a string, even a column that looks numeric?**
> A: CSV is a plain-text format with no concept of data types — every field is just literal text between commas. `csv.DictReader` (and `csv.reader`) parse the text structure (which text belongs to which column) but don't attempt to infer or convert types, so a column like `"age"` comes back as `"36"` (a string), not `36` (an int). You must explicitly cast with `int()`/`float()` if you need numeric operations. This is exactly the kind of type-inference work that `pd.read_csv()` automates later.

## Practical/Coding Questions

**Q: Write code that reads a JSON file `config.json` and safely returns a default value if the key `"timeout"` is missing.**
```python
import json

with open("config.json", "r") as file:
    config = json.load(file)

timeout = config.get("timeout", 30)   # default to 30 if the key isn't present
print(timeout)
```
> Explanation: since `json.load()` returns a plain Python `dict`, all the normal `dict` methods apply — `.get(key, default)` avoids a `KeyError` exactly as it would for any other dict (Module 01).

**Q: Write a function `fetch_user(user_id)` that GETs `https://jsonplaceholder.typicode.com/users/{user_id}`, returns the parsed JSON on success, and returns `None` on any failure (bad status or network error).**
```python
import requests

def fetch_user(user_id):
    try:
        response = requests.get(
            f"https://jsonplaceholder.typicode.com/users/{user_id}",
            timeout=5
        )
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return None

print(fetch_user(1))       # returns the user dict
print(fetch_user(9999))     # returns None (404)
```
> Explanation: `requests.RequestException` is the base class for all of `requests`' exceptions (`HTTPError`, `ConnectionError`, `Timeout`, etc.), so catching it here is a concise way to treat any failure the same way — return `None` rather than crash the caller.

## Scenario Questions

**Q: You're building a script that calls a third-party API every hour to fetch pricing data, and the API occasionally times out or returns a 500 error. How would you make this resilient?**
> A: I'd wrap the request in `try`/`except`, catching `requests.Timeout` and `requests.HTTPError` specifically (plus `ConnectionError` for network issues), always passing an explicit `timeout=`. On failure, I'd log the error with enough detail to diagnose it later, and depending on requirements, either skip that hour's run and try again next cycle, or implement a retry with a short backoff for transient errors like a `500` or timeout (though I'd avoid retrying on a `404`, since that's not going to change). The key principle is: don't let one bad API call crash the whole scheduled job.

**Q: You need to save API response data locally so you don't have to re-call the API every time you test your script. What would you do?**
> A: After a successful request, I'd write `response.json()` to a local file with `json.dump(data, file, indent=4)`. Then, while developing/testing, I could load from that cached file instead of hitting the live API repeatedly — useful for avoiding rate limits, working offline, and getting consistent test data. I'd make sure this is clearly a temporary dev convenience, not a substitute for real API calls in production.

## "Gotcha" Questions

**Q: What's wrong with this code, assuming the goal is to only read the file's existing contents?**
```python
with open("important_data.txt", "w") as file:
    contents = file.read()
```
> A: Opening in `"w"` mode immediately erases the file's existing content, so `file.read()` returns an empty string — and the original data is now gone. To read without risk of overwriting, the mode should be `"r"` (or omit the mode argument entirely, since `"r"` is the default).

**Q: Why might `response.json()` raise an error even though `response.status_code` was `200`?**
> A: A `200` status only confirms the *request* succeeded — it says nothing about whether the response *body* is valid JSON. If the server returned an empty body, HTML, or malformed text (which can happen with misconfigured endpoints or unexpected server behavior), `.json()` will raise a `json.JSONDecodeError` (via `requests.exceptions.JSONDecodeError`) trying to parse it. Status code and response format/validity are two separate things to check.

## Quick-Fire Rapid Review

- Q: What guarantees a file gets closed even if an error occurs? → **the `with` statement (context manager)**
- Q: Which file mode erases existing content? → **`"w"`**
- Q: JSON functions that work with strings (not files)? → **`json.dumps()` / `json.loads()`**
- Q: What type are all values read from a CSV file? → **strings**
- Q: Preferred CSV reader for accessing columns by name? → **`csv.DictReader`**
- Q: Does `requests.get()` raise an exception on a 404 response by itself? → **No — check `.status_code` or call `.raise_for_status()`**
- Q: What should you always pass to a real `requests.get()` call? → **`timeout=`**
- Q: Method that parses a `requests` response body as JSON? → **`.json()`**
