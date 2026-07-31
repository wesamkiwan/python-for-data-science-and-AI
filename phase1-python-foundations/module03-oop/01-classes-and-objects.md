# Module 03a: Classes & Objects — Modeling Real-World Things in Code

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [Module 02 — Functions, Modules & Error Handling](../module02-functions-modules-errors/03-error-handling.md)

## 🎯 Learning Objectives
- [ ] Explain what a class and an object are, and how they relate
- [ ] Define a class with `__init__` and instance attributes
- [ ] Write instance methods that operate on an object's data
- [ ] Distinguish class attributes from instance attributes
- [ ] Use class methods and static methods appropriately

---

## Module Goal

Learn **Object-Oriented Programming (OOP)** — a way of organizing code around "objects" that bundle data (attributes) and behavior (methods) together. This is how almost every real Python library you'll use is built: a Pandas `DataFrame`, a scikit-learn model, a PyTorch neural network — all are **objects**, instances of **classes**.

## Why This Matters on the Job

You already *use* OOP constantly without writing it — `df.head()`, `model.fit(X, y)`, `model.predict(X_test)` are all method calls on objects. Understanding classes means you understand *why* `model.fit()` works the way it does, why some libraries require you to create an object before calling methods on it (`model = LinearRegression()` then `model.fit(...)`), and lets you build your own reusable, well-organized components instead of scattering related data and functions across a file.

---

## Classes vs. Objects: The Blueprint Analogy

A **class** is a blueprint — it defines what data and behavior something will have, but it isn't a real "thing" itself. An **object** (or **instance**) is an actual thing built from that blueprint.

💡 **Analogy:** Think of a class as an architectural blueprint for a house, and each object as an actual house built from it. The blueprint defines "every house has a number of bedrooms and a front door you can open" — each individual house has its *own* number of bedrooms, and opening one house's door doesn't open another's.

```python
class Dog:
    pass   # empty class body — a placeholder, does nothing yet

my_dog = Dog()      # my_dog is an object — an instance of the Dog class
your_dog = Dog()      # a completely separate object

print(type(my_dog))    # <class '__main__.Dog'>
print(my_dog is your_dog)   # False — two distinct objects
```

✅ **Best Practice:** Class names use `PascalCase` (`Dog`, `LinearRegression`, `CustomerAccount`) — this is the universal Python convention that distinguishes a class from a regular variable or function (`snake_case`).

## Defining a Class with `__init__`

`__init__` is a special method (note the double underscores — called a **dunder**, short for "double underscore") that runs automatically whenever you create a new object. It sets up the object's initial data.

```python
class Dog:
    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age

my_dog = Dog("Rex", "Labrador", 3)

print(my_dog.name)     # Rex
print(my_dog.breed)      # Labrador
print(my_dog.age)         # 3
```

**How it works:**
- `def __init__(self, name, breed, age):` — defines the constructor. It runs automatically when you call `Dog("Rex", "Labrador", 3)`.
- `self` refers to *the specific object being created*. It's always the first parameter of any instance method, though Python passes it automatically — you never type it yourself when calling.
- `self.name = name` — stores the `name` argument as an **instance attribute**, attached to this specific object, accessible later as `my_dog.name`.

⚠️ **Warning:** Forgetting `self` as the first parameter of a method (or forgetting the `self.` prefix when storing an attribute) is the single most common beginner OOP mistake. Without `self.name = name`, the `name` argument is just a local variable that disappears once `__init__` finishes — the object never actually stores it.

## Instance Methods: Behavior Tied to an Object

A method is a function defined inside a class that operates on a specific object's data via `self`.

```python
class Dog:
    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age

    def bark(self):
        return f"{self.name} says Woof!"

    def have_birthday(self):
        self.age += 1
        return f"{self.name} is now {self.age} years old."

my_dog = Dog("Rex", "Labrador", 3)
print(my_dog.bark())            # Rex says Woof!
print(my_dog.have_birthday())     # Rex is now 4 years old.
print(my_dog.age)                  # 4 — the object's state actually changed
```

**How it works:** Calling `my_dog.bark()` is shorthand for `Dog.bark(my_dog)` — Python automatically passes `my_dog` as `self`. Inside the method, `self.name` and `self.age` refer to *that specific dog's* data, not any other `Dog` object's.

🎯 **On the job:** This is exactly the pattern behind `model.fit(X, y)` in scikit-learn — `fit` is an instance method that stores what it learns (`self.coefficients_`, etc.) directly on the `model` object, so a later call to `model.predict(X_test)` can use that stored state.

## Class Attributes vs. Instance Attributes

An **instance attribute** (like `self.name` above) belongs to one specific object. A **class attribute** is defined directly in the class body (not inside `__init__`) and is shared by *every* instance of that class, unless a specific instance overrides it.

```python
class Dog:
    species = "Canis familiaris"   # class attribute — shared by ALL dogs

    def __init__(self, name, age):
        self.name = name    # instance attribute — unique per dog
        self.age = age        # instance attribute — unique per dog

dog1 = Dog("Rex", 3)
dog2 = Dog("Bella", 5)

print(dog1.species)   # Canis familiaris
print(dog2.species)    # Canis familiaris — same value, shared from the class

print(dog1.name, dog2.name)   # Rex Bella — different, each instance's own
```

⚠️ **Warning:** Just like mutable default arguments (Module 02), a *mutable* class attribute (like a `list`) is dangerous — since it's shared across every instance, mutating it through one object affects all of them.

```python
class Team:
    members = []   # ❌ shared mutable class attribute — bug waiting to happen

    def add_member(self, name):
        self.members.append(name)

team_a = Team()
team_b = Team()
team_a.add_member("Ada")
print(team_b.members)   # ['Ada']  <- shared across BOTH teams! Not what you wanted.
```

✅ **Best Practice:** if a "list of things per object" is what you want, initialize it inside `__init__` as `self.members = []` — that creates a fresh, independent list for every instance.

## Class Methods and Static Methods (Brief Intro)

Occasionally a method needs to operate on the *class itself* rather than one instance, or doesn't need `self`/instance data at all.

```python
class Dog:
    species_count = 0

    def __init__(self, name):
        self.name = name
        Dog.species_count += 1

    @classmethod
    def get_population(cls):
        """cls refers to the class itself, not an instance."""
        return cls.species_count

    @staticmethod
    def is_valid_age(age):
        """Doesn't need self OR cls — just a utility function grouped with the class."""
        return 0 <= age <= 25

Dog("Rex")
Dog("Bella")
print(Dog.get_population())         # 2
print(Dog.is_valid_age(30))            # False
```

💡 **Tip:** You don't need to master these two decorators yet — just recognize the pattern (`@classmethod` uses `cls` for class-level data; `@staticmethod` is a plain function that's just organized inside the class namespace). You'll see both occasionally in library code.

---

## Hands-On Exercise

**Task:** Write `bank_account.py` that:
1. Defines a class `BankAccount` with `__init__(self, owner, balance=0)`.
2. Adds a method `deposit(self, amount)` that increases `balance` and returns the new balance.
3. Adds a method `withdraw(self, amount)` that decreases `balance` if there are sufficient funds, otherwise returns a message saying so (no exceptions yet — that's fine at this stage).
4. Creates two separate `BankAccount` objects and proves their balances are tracked independently.

<details>
<summary>✅ Click to see the solution</summary>

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            return f"Insufficient funds. Current balance: {self.balance}"
        self.balance -= amount
        return self.balance

ada_account = BankAccount("Ada", 100)
grace_account = BankAccount("Grace", 50)

print(ada_account.deposit(50))      # 150
print(grace_account.withdraw(100))    # Insufficient funds. Current balance: 50
print(ada_account.balance)              # 150 — unaffected by grace_account's operations
print(grace_account.balance)              # 50
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Forgetting `self` as a method's first parameter | Every instance method needs `self` first — Python passes it automatically on call |
| Forgetting `self.` when storing/reading an attribute | Always use `self.attribute_name` inside methods, not a bare local variable |
| Using a mutable class attribute (`list`/`dict`) for per-object data | Initialize it inside `__init__` as `self.attr = []` instead |
| Confusing a class (blueprint) with an object (instance) | A class defines structure; an object is one concrete thing built from it |
| snake_case class names | Use `PascalCase` for class names — universal convention |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand the class/object (blueprint/instance) relationship
- [ ] Can define a class with `__init__` and instance attributes
- [ ] Can write instance methods that read/modify `self`'s data
- [ ] Know the difference between class attributes and instance attributes, and the mutable-class-attribute trap
- [ ] Recognize `@classmethod` and `@staticmethod` at a basic level
- [ ] Completed the `bank_account.py` exercise

**Next:** Continue to [`02-inheritance-and-polymorphism.md`](02-inheritance-and-polymorphism.md)
