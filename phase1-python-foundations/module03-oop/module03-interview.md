# 🎤 Module 03 Interview Prep: Object-Oriented Programming

## Conceptual Questions

### 🟢 Beginner

**Q: What's the difference between a class and an object?**
> A: A class is a blueprint — it defines what attributes and methods something will have. An object (or instance) is a concrete thing built from that blueprint, with its own actual data. `class Dog:` defines the shape; `rex = Dog("Rex", 3)` creates one real dog. You can create many independent objects from the same class.

**Q: What is `self`, and why does every instance method need it?**
> A: `self` refers to the specific object a method is being called on. It's how a method accesses and modifies *that particular* object's data (`self.name`, `self.balance`, etc.) rather than some other instance's. Python passes it automatically when you call `obj.method()` — you never pass it explicitly yourself, but you must declare it as the first parameter when defining the method.

**Q: What's the difference between a class attribute and an instance attribute?**
> A: A class attribute is defined directly in the class body and shared by every instance (unless a specific instance overrides it). An instance attribute is set inside `__init__` (or another method) via `self.x = ...` and belongs to just that one object. Class attributes are useful for genuinely shared, constant data; instance attributes are for per-object data — and importantly, a *mutable* class attribute (like a list) is dangerous because mutating it through one instance affects all instances.

### 🟡 Intermediate

**Q: What does `super()` do, and why use it instead of just duplicating the parent's `__init__` code?**
> A: `super()` gives you access to the parent class's methods from within a subclass, most commonly to call `super().__init__(...)` so the subclass reuses the parent's setup logic instead of copy-pasting it. This means if the parent class's `__init__` logic changes later, every subclass using `super()` automatically picks up the change — duplicated code would silently drift out of sync.

**Q: Explain polymorphism with an example.**
> A: Polymorphism means the same method call behaves differently depending on the actual object's type, without the calling code needing to check which type it is. For example, if `Dog` and `Cat` both inherit from `Animal` and each overrides `make_sound()`, a loop that calls `animal.make_sound()` on a mixed list of dogs and cats gets the correct sound for each, with no `if isinstance(...)` branching needed. scikit-learn relies on this heavily — `model.fit(X, y)` works identically whether `model` is a `LinearRegression` or a `RandomForestClassifier`.

**Q: What's the difference between `__str__` and `__repr__`?**
> A: `__str__` controls the human-readable representation shown by `print()`/`str()` — meant to be friendly and readable. `__repr__` controls the representation used by the REPL, `repr()`, and inside containers like lists — meant to be unambiguous, ideally code that could recreate the object. If only `__repr__` is defined, Python falls back to it for `print()` too, so it's the safer one to always implement.

## Practical/Coding Questions

**Q: Write a class `Rectangle` with `width` and `height`, a method `area()`, and a method `perimeter()`.**
```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

r = Rectangle(4, 5)
print(r.area())        # 20
print(r.perimeter())     # 18
```
> Explanation: straightforward instance attributes set in `__init__`, with two instance methods computing values from `self.width`/`self.height`.

**Q: Given a base class `Shape` with a placeholder `area()` returning `0`, write a subclass `Square` that overrides `area()` correctly.**
```python
class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2

sq = Square(4)
print(sq.area())   # 16
```
> Explanation: `Square` inherits from `Shape` but overrides `area()` with its own logic — demonstrating inheritance plus method overriding in one example.

## Scenario Questions

**Q: You're designing classes to represent different employee types (Manager, Engineer, Intern) that all need a name, salary, and a `calculate_bonus()` method — but the bonus formula differs per type. How would you structure this with OOP?**
> A: I'd create a base `Employee` class holding the shared attributes (`name`, `salary`) in `__init__`, and define `calculate_bonus()` there as a placeholder (or leave it unimplemented, expecting subclasses to override it). Then each subclass — `Manager`, `Engineer`, `Intern` — inherits from `Employee`, calls `super().__init__(name, salary)` to reuse the shared setup, and overrides `calculate_bonus()` with its own formula. Code that processes a list of employees can then call `employee.calculate_bonus()` polymorphically without caring which subclass it actually is.

**Q: Why might you use `@property` instead of just letting callers set `self.balance` directly?**
> A: A plain attribute has no way to validate what gets assigned to it — `account.balance = -500` would silently succeed even though a negative balance shouldn't be allowed. `@property` with a paired setter lets me run validation logic (raise a `ValueError` for bad values) while callers still use the same simple `account.balance = 200` syntax, with no change to the class's public interface.

## "Gotcha" Questions

**Q: What's the bug here, and what does it print?**
```python
class Team:
    members = []
    def add_member(self, name):
        self.members.append(name)

team_a = Team()
team_b = Team()
team_a.add_member("Ada")
print(team_b.members)
```
> A: It prints `['Ada']` — surprising, since `team_a` and `team_b` are supposed to be independent. The bug is that `members = []` is a *class* attribute, shared by every instance of `Team`, not a per-instance list. Fix: set `self.members = []` inside `__init__` so each `Team` object gets its own independent list.

**Q: Why does `p1 == p2` return `False` here even though both points have identical coordinates?**
```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

p1 = Point(1, 2)
p2 = Point(1, 2)
print(p1 == p2)   # False
```
> A: Without a custom `__eq__`, `==` falls back to Python's default behavior, which checks object *identity* (same as `is`) — are these literally the same object in memory? `p1` and `p2` are two separate objects, so it's `False` regardless of their data being equal. Defining `__eq__(self, other): return self.x == other.x and self.y == other.y` fixes this to compare values instead.

## Quick-Fire Rapid Review

- Q: What creates a new object from a class? → **calling the class like a function, e.g. `Dog("Rex", 3)`**
- Q: What's always the first parameter of an instance method? → **`self`**
- Q: What does `super().__init__(...)` do? → **calls the parent class's `__init__`**
- Q: Default meaning of `==` without a custom `__eq__`? → **object identity (same as `is`)**
- Q: Which dunder is the safer fallback to always define, `__str__` or `__repr__`? → **`__repr__`**
- Q: Convention for "internal use" attribute? → **single leading underscore, `_name`**
- Q: What decorator lets a method be accessed like a plain attribute? → **`@property`**
- Q: What does `isinstance(rex, Animal)` check if `Dog` inherits from `Animal`? → **`True` — respects inheritance**
