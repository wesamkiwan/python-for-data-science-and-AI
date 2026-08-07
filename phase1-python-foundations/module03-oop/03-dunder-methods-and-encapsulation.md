# Module 03c: Dunder Methods & Encapsulation

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 45min | **Prerequisites:** [02-inheritance-and-polymorphism.md](02-inheritance-and-polymorphism.md)

## 🎯 Learning Objectives
- [ ] Implement `__str__` and `__repr__` to control how objects print
- [ ] Implement `__eq__` to control how objects compare with `==`
- [ ] Explain Python's encapsulation conventions (`_protected`, `__private`)
- [ ] Write classic `get_x()`/`set_x()` getter and setter methods
- [ ] Use the `@property` decorator for controlled attribute access, and know when to reach for it instead of a plain method

---

## Module Goal

Learn the "special methods" (dunders) that let your objects integrate naturally with Python's built-in behavior — printing, comparing, and more — plus the conventions Python uses to signal "internal use only" data, since Python doesn't enforce true private attributes the way some other languages do.

## Why This Matters on the Job

Ever printed a Pandas DataFrame and gotten a clean table instead of `<DataFrame object at 0x7f...>`? That's `__str__`/`__repr__` at work. Ever compared two objects with `==` and had it check *their values* instead of just "are these the exact same object in memory"? That's `__eq__`. These dunder methods are why library objects feel polished — and writing them for your own classes is what separates "code that technically works" from code that's pleasant and debuggable to use.

---

## `__repr__` and `__str__`: Controlling How Objects Print

By default, printing an object gives an unhelpful memory address:

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

rex = Dog("Rex", "Labrador")
print(rex)   # <__main__.Dog object at 0x000001A2B3C4D5E0>  -- not useful!
```

Define `__str__` to control what `print()` and `str()` show — meant for a **readable, human-facing** description:

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def __str__(self):
        return f"{self.name} the {self.breed}"

rex = Dog("Rex", "Labrador")
print(rex)          # Rex the Labrador
print(str(rex))       # Rex the Labrador
```

Define `__repr__` to control what shows in the **interactive REPL**, inside a `list`/`dict`, or when debugging — meant to be **unambiguous**, ideally code that could recreate the object:

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def __repr__(self):
        return f"Dog(name={self.name!r}, breed={self.breed!r})"

rex = Dog("Rex", "Labrador")
print(rex)                # Dog(name='Rex', breed='Labrador') -- falls back to __repr__ if no __str__
print([rex])                # [Dog(name='Rex', breed='Labrador')] -- lists always use repr() on their items
```

💡 **Tip:** `!r` inside an f-string calls `repr()` on that value — for a string, that wraps it in quotes, making it clear it's a string and not raw code. This is exactly why `repr()`-style output is considered "unambiguous."

✅ **Best Practice:** Define both when you can. If you only define one, prefer `__repr__` — Python falls back to it for `print()`/`str()` if `__str__` is missing, but not the other way around.

## `__eq__`: Controlling How Objects Compare

By default, `==` on two objects checks **identity** (are they the exact same object in memory) — the same as `is`:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1 == p2)   # False -- different objects, even with identical data!
```

Define `__eq__` to compare based on **values** instead:

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1 == p2)   # True -- now compares the actual coordinate values
```

**How it works:** `p1 == p2` calls `p1.__eq__(p2)`, with `other` bound to `p2`. We define what "equal" means for our own class instead of relying on Python's default identity check.

⚠️ **Warning:** This simplified `__eq__` will raise an `AttributeError` if compared against something without `.x`/`.y` (e.g. `p1 == "hello"`). Production code typically adds a type check first (`isinstance(other, Point)`), but that's a refinement to layer on once the core idea clicks.

## Encapsulation: Python's Naming Conventions

**Encapsulation** means controlling access to an object's internal data — hiding implementation details and exposing only what's meant to be used from outside. Unlike languages with a strict `private` keyword, Python relies on **naming conventions** — nothing is truly unreachable, but the names signal intent clearly.

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner            # public — freely accessible
        self._balance = balance         # single underscore: "protected" (convention: internal use)
        self.__pin = "1234"                # double underscore: "private" (name-mangled)

account = BankAccount("Ada", 100)
print(account.owner)          # Ada -- fine, it's public
print(account._balance)         # 100 -- works, but a single underscore signals "please don't touch this directly"
# print(account.__pin)            # AttributeError! double-underscore names are "mangled"
print(account._BankAccount__pin)  # 1234 -- still technically reachable, just awkward on purpose
```

| Convention | Meaning | Enforcement |
|---|---|---|
| `name` | Public — part of the intended interface | None needed |
| `_name` | "Protected" — internal use, don't touch from outside the class | Convention only (nothing stops you) |
| `__name` | "Private" — Python renames it internally (`_ClassName__name`) to avoid accidental clashes with subclasses | Mostly enforced via name mangling, still technically reachable |

✅ **Best Practice:** Use a single leading underscore (`_balance`) for attributes meant to be internal — this is by far the most common convention in real Python code. Reserve double underscores for the rare case where you specifically want to avoid subclass naming collisions.

## Getters and Setters: The Classic Pattern

Once you have an internal attribute like `_balance`, the traditional OOP way to control access to it — the same technique used in Java, C++, C#, and taught this way in classic CS texts like *Introduction to Computation and Programming Using Python* (MIT's intro course book, which builds its whole `Person` class example around `get_name()`, `set_birthday()`, and `get_age()` methods) — is a pair of plain methods:

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance

    def get_balance(self):
        """Classic getter -- just hands back the internal value."""
        return self._balance

    def set_balance(self, new_balance):
        """Classic setter -- validates before updating."""
        if new_balance < 0:
            raise ValueError("Balance cannot be negative.")
        self._balance = new_balance

account = BankAccount("Ada", 100)
print(account.get_balance())     # 100

account.set_balance(200)              # runs validation, then updates _balance
print(account.get_balance())        # 200

account.set_balance(-50)                # raises: ValueError: Balance cannot be negative.
```

**How it works:** exactly like any other method — `get_balance()` reads `self._balance`, `set_balance()` validates and writes it. Nothing Python-specific here; this is standard, fully valid, widely-used object-oriented code in any language, Python included.

✅ **Best Practice:** There's nothing wrong with this style — plenty of real Python code (and most non-Python OOP code you'll read) uses it. Python just also offers a second option, `@property`, that gives you the same validation with attribute-style syntax at the call site (`account.balance` instead of `account.get_balance()`). Reach for it when you're writing new code and want that syntax; keep using plain getter/setter methods when that's the existing pattern in a codebase, or when you're more comfortable with the explicit method call.

## `@property`: Controlled Access to Attributes

A **property** lets you expose a method that behaves like a plain attribute — useful for adding validation or computed values without changing how callers use your class.

💡 **Tip — coming from Java/C#/C++?** `@property` is Python's *optional upgrade* on top of the classic getter/setter pattern you just saw. It solves one specific annoyance: if a class starts out with a plain public attribute (`self.balance`) and later needs validation, switching to `get_balance()`/`set_balance()` breaks every caller that wrote `account.balance`. `@property` lets you make that switch without changing any calling code — `account.balance` keeps working, it just quietly runs your method underneath.

| Style | Call site | When to use |
|---|---|---|
| `get_x()` / `set_x()` | `account.get_balance()` | Matches other OOP languages; fine for any class, especially if that's the convention already in use |
| `@property` + `@x.setter` | `account.balance` | Idiomatic default for *new* Python code; lets you add validation later without breaking existing `obj.attr` call sites |

```python
class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        """Read-only access to the current balance."""
        return self._balance

    @balance.setter
    def balance(self, new_balance):
        if new_balance < 0:
            raise ValueError("Balance cannot be negative.")
        self._balance = new_balance

account = BankAccount("Ada", 100)
print(account.balance)     # 100 -- looks like a plain attribute, but runs the @property method

account.balance = 200        # runs the setter, validates, then updates _balance
print(account.balance)         # 200

account.balance = -50           # raises: ValueError: Balance cannot be negative.
```

**How it works:** `@property` turns the `balance` method into something accessed *without* parentheses (`account.balance`, not `account.balance()`). The paired `@balance.setter` lets `account.balance = 200` run validation logic instead of blindly overwriting the attribute.

🎯 **On the job:** This pattern — store the real data with a leading underscore, expose controlled read/write access via `@property` — is exactly how many library classes let you write `model.n_estimators = 100` while validating the value behind the scenes.

---

## Hands-On Exercise

**Task:** Write `temperature.py` that:
1. Defines a class `Temperature` with `__init__(self, celsius)` storing `self._celsius`.
2. Adds a `@property` called `celsius` that returns `self._celsius`, with a setter that raises `ValueError` if the value is below `-273.15` (absolute zero).
3. Adds a `@property` called `fahrenheit` (read-only, no setter needed) that computes and returns `celsius * 9/5 + 32`.
4. Adds `__str__` returning something like `"25.0°C (77.0°F)"`.
5. Tests creating a `Temperature`, printing it, and triggering the validation error.

<details>
<summary>✅ Click to see the solution</summary>

```python
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Temperature cannot be below absolute zero.")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32

    def __str__(self):
        return f"{self.celsius}°C ({self.fahrenheit}°F)"

temp = Temperature(25)
print(temp)                 # 25°C (77.0°F)

temp.celsius = 30
print(temp)                  # 30°C (86.0°F)

temp.celsius = -300            # raises: ValueError: Temperature cannot be below absolute zero.
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Expecting `_name` to be truly private | It's convention only — use it to signal intent, not to enforce security |
| Only defining `__str__`, never `__repr__` | Define `__repr__` at minimum — it's the fallback for printing, debugging, and container display |
| Relying on default `==` (identity) when you meant value equality | Define `__eq__` whenever "equal" should mean "same data," not "same object" |
| Directly mutating an attribute that should be validated | Use a setter method (`set_x()`) or `@property` + setter to centralize validation logic |
| Assuming `@property` is "correct Python" and `get_x()`/`set_x()` is "wrong" | Both are valid; classic getter/setter methods are still common and completely fine, `@property` is just the more idiomatic *default* for brand-new code |
| Overusing double-underscore "private" attributes | Reserve for genuine name-collision concerns; single underscore covers 95% of real cases |

---

## ✅ Module 03 Completion Checklist
- [ ] Can implement `__str__` and `__repr__` and explain the difference
- [ ] Can implement `__eq__` for value-based comparison
- [ ] Understand `_protected` vs `__private` naming conventions and that neither is truly enforced
- [ ] Can write classic `get_x()`/`set_x()` getter and setter methods
- [ ] Can use `@property` and a matching setter for validated attribute access, and explain when each style is the better fit
- [ ] Completed the `temperature.py` exercise
- [ ] Reviewed [`module03-cheatsheet.md`](module03-cheatsheet.md)
- [ ] Reviewed [`module03-interview.md`](module03-interview.md)
- [ ] Browsed [`module03-references.md`](module03-references.md)

**Next Step:** Module 04 — File I/O, JSON/CSV & Working with APIs (`phase1-python-foundations/module04-file-io-apis/`)
