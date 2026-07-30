# 🎤 Module 01 Interview Prep: Python Fundamentals

## Conceptual Questions

### 🟢 Beginner

**Q: What's the difference between a list and a tuple?**
> A: Both are ordered collections that can hold duplicates. The key difference is mutability — a list can be changed after creation (add/remove/modify items), while a tuple is immutable — once created, it can't be changed. I'd use a tuple for fixed data like coordinates, and a list for anything I expect to grow or modify, like a running collection of results.

**Q: What does "dynamically typed" mean in Python?**
> A: It means you don't have to declare a variable's type up front, and a variable can be reassigned to a value of a different type later. Python figures out the type at runtime based on the value assigned. This is different from statically typed languages like Java or C++, where you must declare `int x` before use.

**Q: What's the difference between `==` and `is`?**
> A: `==` checks if two values are equal. `is` checks if two variables refer to the exact same object in memory (identity). For comparing values (like numbers or strings), use `==`. The one common exception is checking for `None` — convention is to always use `is None` rather than `== None`.

### 🟡 Intermediate

**Q: Why does `int("3.5")` raise an error, but `int(3.5)` doesn't?**
> A: `int()` on a string requires the string to look like a valid integer literal — `"3.5"` isn't, because it contains a decimal point, so Python raises a `ValueError`. `int(3.5)` works because it's converting an actual float value, which Python truncates toward zero, giving `3`. To convert a decimal-looking string to an int, you go through float first: `int(float("3.5"))`.

**Q: When would you choose a set over a list?**
> A: When I need to store unique items and don't care about order, or when I need to do fast membership checks (`in`) — sets use a hash table internally, so checking membership is roughly O(1) versus O(n) for a list. A common use case is de-duplicating a large collection of IDs, or checking "have I already seen this value?" inside a loop over thousands of records.

## Practical/Coding Questions

**Q: Write a function-free snippet that takes a list of numbers and returns only the even ones, using a list comprehension.**
```python
numbers = [1, 2, 3, 4, 5, 6]
evens = [n for n in numbers if n % 2 == 0]
print(evens)  # [2, 4, 6]
```
> Explanation: `n % 2 == 0` checks if the remainder of `n / 2` is zero, which is true only for even numbers.

**Q: Given `d = {"a": 1, "b": 2}`, write code that safely prints the value for key `"c"` without crashing, defaulting to `0`.**
```python
d = {"a": 1, "b": 2}
print(d.get("c", 0))  # 0
```
> Explanation: `dict.get(key, default)` returns `default` instead of raising `KeyError` when the key is absent — this is safer than `d["c"]` for keys that may not exist.

## Scenario Questions

**Q: You're reading a "score" column from a CSV, and it's supposed to contain integers, but one row has the text "N/A". What happens if you call `int()` on every value in a loop, and how would you handle it?**
> A: `int("N/A")` raises a `ValueError` and crashes the loop on that row. In real code, I'd wrap the conversion in a `try/except` (covered in Module 02) to catch bad values, log or skip them, and continue processing the rest of the data rather than letting one bad row take down the whole pipeline. In practice, once we reach Pandas (Module 07-08), we'd typically use `pd.to_numeric(..., errors="coerce")` to handle this at scale.

## "Gotcha" Questions

**Q: What does this print, and why?**
```python
print(5 / 2)
print(5 // 2)
```
> A: `5 / 2` prints `2.5` — the `/` operator always returns a `float` in Python 3, even when both operands are integers. `5 // 2` prints `2` — the `//` operator is floor division, which rounds down to the nearest whole number. This trips people up coming from languages where `/` on two ints returns an int.

**Q: Is Python's `range(5)` inclusive or exclusive of 5?**
> A: Exclusive. `range(5)` produces `0, 1, 2, 3, 4` — it stops *before* reaching the stop value. This "stop is exclusive" convention also applies to list slicing, e.g. `lst[1:3]` gives indices 1 and 2, not 3.

## Quick-Fire Rapid Review

- Q: 0-indexed or 1-indexed? → **0-indexed**
- Q: Mutable collection types? → **list, dict, set**
- Q: Immutable collection type? → **tuple**
- Q: `and`/`or`/`not` are what kind of operators? → **Logical**
- Q: What does `.get()` prevent on a dict? → **KeyError**
- Q: What type does `/` always return? → **float**
- Q: Preferred way to build strings with variables? → **f-strings**
- Q: How do you check for `None` correctly? → **`is None`, not `== None`**
