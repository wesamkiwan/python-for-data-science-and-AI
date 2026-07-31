# Module 04c: Working with APIs

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [02-json-and-csv.md](02-json-and-csv.md)

## 🎯 Learning Objectives
- [ ] Explain what an API is and what a GET request does
- [ ] Install and use the `requests` library to call a public API
- [ ] Parse a JSON API response into Python data
- [ ] Check status codes and handle failed requests gracefully
- [ ] Pass query parameters to an API request

---

## Module Goal

Learn to pull real, live data from the internet into your Python programs by calling web APIs — combining everything from this module (files, JSON) with a new tool, the `requests` library, Python's de facto standard for making HTTP requests.

## Why This Matters on the Job

A huge amount of real-world data work starts with "go get this data from an API" — pricing data, weather data, a company's internal microservice, a third-party data provider. Later in this course, calling an LLM API (Module 19) is *also* fundamentally an HTTP request that returns JSON — the exact pattern you're about to learn. Mastering `requests` now means every future module that touches an external service will feel familiar rather than intimidating.

---

## What Is an API?

An **API** (Application Programming Interface) is how one piece of software asks another for data or to perform an action — in this module's context, specifically a **web API**: you send an HTTP request to a URL, and the server sends back a response, usually as JSON.

💡 **Analogy:** Think of an API like a restaurant menu and waiter. You (the client) don't walk into the kitchen (the server's internal code) yourself — you ask the waiter (the API) for something specific from the menu (an endpoint/URL), and they bring back exactly that (the response), without you needing to know how the kitchen works internally.

## Installing `requests`

```bash
pip install requests
```

💡 **Tip:** Unlike `json` and `csv` (standard library, no install needed), `requests` is a third-party package — you first met this distinction in Module 02.

## Making a GET Request

A **GET** request asks a server for data (as opposed to a **POST** request, which typically sends data to create or change something — out of scope for this module, but you'll recognize the term).

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users/1")

print(response.status_code)   # 200 -- 200 means "OK, success"
print(response.text)             # the raw response body as a string
```

**How it works:** `requests.get(url)` sends an HTTP GET request to that URL and waits for a response, returned as a `Response` object with useful attributes like `.status_code` and `.text`.

## Parsing the JSON Response

Most modern APIs return JSON. Instead of manually calling `json.loads(response.text)`, `requests` gives you a shortcut:

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users/1")
data = response.json()          # parses the JSON body directly into a Python dict

print(data["name"])          # Leanne Graham
print(data["email"])           # Sincere@april.biz
print(data["address"]["city"])   # Gwenborough -- nested dict, just like Module 02's JSON lesson
```

**How it works:** `.json()` is equivalent to `json.loads(response.text)` — it's a convenience method `requests` provides since parsing JSON responses is by far the most common thing you'll do with one.

## Status Codes: Did the Request Succeed?

Every HTTP response includes a **status code** telling you what happened:

| Code range | Meaning | Example |
|---|---|---|
| 200-299 | Success | `200 OK` |
| 300-399 | Redirection | `301 Moved Permanently` |
| 400-499 | Client error (you made a bad request) | `404 Not Found`, `401 Unauthorized` |
| 500-599 | Server error (something broke on their end) | `500 Internal Server Error` |

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users/9999")   # doesn't exist
print(response.status_code)   # 404
```

⚠️ **Warning:** `requests.get()` does **not** raise an exception just because the server returned an error status like `404` or `500` — the request itself "succeeded" (a response came back), even though the *content* represents a failure. You must check `.status_code` yourself, or use `.raise_for_status()`.

```python
import requests

response = requests.get("https://jsonplaceholder.typicode.com/users/9999")

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Request failed with status code: {response.status_code}")
```

### `raise_for_status()`: Turning Bad Status Codes into Exceptions

```python
import requests

try:
    response = requests.get("https://jsonplaceholder.typicode.com/users/9999")
    response.raise_for_status()   # raises requests.HTTPError if status is 4xx or 5xx
    data = response.json()
    print(data)
except requests.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except requests.ConnectionError:
    print("Failed to connect — check your internet connection or the URL.")
```

✅ **Best Practice:** Combining `.raise_for_status()` with `try`/`except` (from Module 02) is the standard, production-grade pattern — it turns "silently getting bad data" into a clear, catchable exception, and separately handles the case where the network itself failed (`ConnectionError`) versus the server responding with an error (`HTTPError`).

## Passing Query Parameters

Many APIs accept extra options via **query parameters** (the `?key=value` part of a URL). `requests` lets you pass these as a dictionary instead of building the URL string by hand:

```python
import requests

response = requests.get(
    "https://jsonplaceholder.typicode.com/posts",
    params={"userId": 1}
)
print(response.url)            # https://jsonplaceholder.typicode.com/posts?userId=1
posts = response.json()
print(len(posts))                 # number of posts belonging to userId 1
```

**How it works:** `params={"userId": 1}` gets automatically appended to the URL as `?userId=1` — `requests` handles the correct formatting/escaping for you, which matters more once values contain spaces or special characters.

## Timeouts: Don't Wait Forever

```python
import requests

try:
    response = requests.get("https://jsonplaceholder.typicode.com/users/1", timeout=5)
    response.raise_for_status()
    print(response.json())
except requests.Timeout:
    print("The request took too long and timed out.")
```

✅ **Best Practice:** Always pass a `timeout` (in seconds) on real requests. Without one, a hung server can leave your program waiting indefinitely — a surprisingly common cause of "frozen" scripts in production.

🎯 **On the job:** This full pattern — `timeout`, `raise_for_status()`, catching `HTTPError`/`ConnectionError`/`Timeout` — is exactly what you'll reuse when calling an LLM API in Module 19, or any external service in a production pipeline.

---

## Hands-On Exercise

**Task:** Write `api_explorer.py` that:
1. Sends a GET request to `https://jsonplaceholder.typicode.com/posts/1` with a 5-second timeout.
2. Uses `raise_for_status()` inside a `try`/`except` to handle failures.
3. Prints the post's `title` and `body` from the parsed JSON.
4. Sends a second request to `https://jsonplaceholder.typicode.com/comments` with `params={"postId": 1}`, and prints how many comments were returned.
5. Saves the comments to a file `comments.json` using what you learned in the previous lesson.

<details>
<summary>✅ Click to see the solution</summary>

```python
import requests
import json

try:
    response = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=5)
    response.raise_for_status()
    post = response.json()
    print(f"Title: {post['title']}")
    print(f"Body: {post['body']}")
except requests.HTTPError as e:
    print(f"HTTP error occurred: {e}")
except requests.Timeout:
    print("The request timed out.")

try:
    comments_response = requests.get(
        "https://jsonplaceholder.typicode.com/comments",
        params={"postId": 1},
        timeout=5
    )
    comments_response.raise_for_status()
    comments = comments_response.json()
    print(f"Number of comments: {len(comments)}")

    with open("comments.json", "w") as file:
        json.dump(comments, file, indent=4)
except requests.HTTPError as e:
    print(f"HTTP error occurred: {e}")
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Assuming a request that "returns" is automatically a success | Always check `.status_code` or use `.raise_for_status()` |
| No `timeout` set | Always pass `timeout=` to avoid indefinite hangs |
| Manually building query strings (`url + "?userId=" + str(id)`) | Use the `params=` dictionary — `requests` handles formatting/escaping |
| Calling `.json()` on a response that isn't actually JSON | Check the response is what you expect, or catch `json.JSONDecodeError` |
| Catching only `Exception` broadly around a request | Catch specific `requests` exceptions (`HTTPError`, `ConnectionError`, `Timeout`) so you can respond appropriately to each |

---

## ✅ Module 04 Completion Checklist
- [ ] Understand what an API and a GET request are, in plain terms
- [ ] Can call a public API with `requests.get()` and parse the JSON response
- [ ] Always check status codes or use `.raise_for_status()`
- [ ] Can pass query parameters with `params=`
- [ ] Always set a `timeout` on real requests
- [ ] Completed the `api_explorer.py` exercise
- [ ] Reviewed [`module04-cheatsheet.md`](module04-cheatsheet.md)
- [ ] Reviewed [`module04-interview.md`](module04-interview.md)
- [ ] Browsed [`module04-references.md`](module04-references.md)

**Next Step:** Module 05 — Python Tooling & Environments (`phase1-python-foundations/module05-tooling-environments/`)
