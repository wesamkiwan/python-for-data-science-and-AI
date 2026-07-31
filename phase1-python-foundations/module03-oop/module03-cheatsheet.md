# 📋 Module 03 Cheat Sheet: Object-Oriented Programming

Fast reference for classes, objects, inheritance, and dunder methods.

## Defining a Class
```python
class Dog:                              # PascalCase class name
    species = "Canis familiaris"          # class attribute — shared by all instances

    def __init__(self, name, age):          # constructor — runs on Dog(...)
        self.name = name                       # instance attribute — unique per object
        self.age = age

    def bark(self):                              # instance method — needs self
        return f"{self.name} says Woof!"

rex = Dog("Rex", 3)      # rex is an object / instance of Dog
```

## Class vs. Static Methods
```python
class Dog:
    count = 0
    def __init__(self, name):
        self.name = name
        Dog.count += 1

    @classmethod
    def get_count(cls):        # cls = the class itself
        return cls.count

    @staticmethod
    def is_valid_age(age):       # no self or cls — plain utility grouped in the class
        return 0 <= age <= 25
```

## Inheritance
```python
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound
    def make_sound(self):
        return f"{self.name} says {self.sound}!"

class Dog(Animal):                                # Dog inherits from Animal
    def __init__(self, name, breed):
        super().__init__(name, sound="Woof")         # call parent's __init__
        self.breed = breed

    def make_sound(self):                                 # override parent method
        return f"{self.name} barks: Woof!"
```

## Polymorphism & Type Checks
```python
for animal in [Dog("Rex", "Lab"), Cat("Tom")]:
    print(animal.make_sound())     # same call, different behavior per subclass

isinstance(rex, Dog)         # True
isinstance(rex, Animal)       # True — respects inheritance
```

## Dunder Methods
```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __str__(self):                        # print(obj) / str(obj) — human-readable
        return f"({self.x}, {self.y})"

    def __repr__(self):                        # repr(obj), REPL, inside lists — unambiguous
        return f"Point(x={self.x!r}, y={self.y!r})"

    def __eq__(self, other):                    # obj == other — value comparison
        return self.x == other.x and self.y == other.y
```

| Dunder | Triggered by | Purpose |
|---|---|---|
| `__init__` | `ClassName(...)` | Set up instance attributes |
| `__str__` | `print(obj)`, `str(obj)` | Human-readable description |
| `__repr__` | REPL echo, `repr(obj)`, inside `list`/`dict` | Unambiguous, debug-friendly description (fallback for `__str__`) |
| `__eq__` | `obj == other` | Value-based equality (default is identity) |

## Encapsulation Conventions

| Syntax | Meaning | Enforced? |
|---|---|---|
| `self.name` | Public | N/A |
| `self._name` | "Protected" — internal use only | Convention only |
| `self.__name` | "Private" — name-mangled to `_ClassName__name` | Mostly, still reachable |

## `@property`: Validated Attribute Access
```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance

    @property
    def balance(self):                 # accessed like a plain attribute: account.balance
        return self._balance

    @balance.setter
    def balance(self, value):            # account.balance = 200 runs this
        if value < 0:
            raise ValueError("Balance cannot be negative.")
        self._balance = value
```

## Quick Troubleshooting

| Error | Likely Cause | Fix |
|---|---|---|
| `TypeError: __init__() missing 1 required positional argument: 'self'` | Called the method on the class, not an instance, or forgot `self` in the method signature | Call via an instance (`obj.method()`), always declare `self` first |
| `AttributeError: 'X' object has no attribute 'y'` | Never set `self.y` in `__init__`, or a typo | Check spelling; confirm the attribute is set somewhere before use |
| Mutating one instance changes all instances | Used a mutable class attribute (`list`/`dict`) instead of an instance attribute | Move it into `__init__` as `self.attr = []` |
| `obj1 == obj2` is `False` despite identical data | No `__eq__` defined — default is identity comparison | Implement `__eq__` for value-based comparison |
| Printing shows `<__main__.X object at 0x...>` | No `__str__`/`__repr__` defined | Implement at least `__repr__` |

## The "New Class" Workflow — do this every time you model something
1. Name the class in `PascalCase`, describing what it represents (`Customer`, not `Data`).
2. Define `__init__` with the attributes every instance needs — use `self.` for each.
3. Add instance methods for behavior; add `__str__`/`__repr__` early for easy debugging.
4. If this "is a kind of" an existing class, inherit from it and call `super().__init__(...)`.
5. Use `_leading_underscore` for internals; add `@property` if an attribute needs validation.
