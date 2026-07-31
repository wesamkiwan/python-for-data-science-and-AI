# Module 03b: Inheritance & Polymorphism — Reusing and Extending Classes

🟢 **Difficulty:** Beginner | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [01-classes-and-objects.md](01-classes-and-objects.md)

## 🎯 Learning Objectives
- [ ] Explain what inheritance is and why it prevents duplicated code
- [ ] Create a subclass that inherits from a parent class
- [ ] Override a parent method in a subclass
- [ ] Use `super()` to call the parent class's version of a method
- [ ] Explain polymorphism with a practical example

---

## Module Goal

Learn how to build a new class based on an existing one — **inheriting** its attributes and methods, and **overriding** just the parts that need to differ. This lets you model "is a kind of" relationships (a `Dog` *is a kind of* `Animal`) without duplicating shared code.

## Why This Matters on the Job

Inheritance is everywhere in the libraries you'll use. Every scikit-learn model (`LinearRegression`, `RandomForestClassifier`, `LogisticRegression`) inherits from a common base class that defines the shared `.fit()`/`.predict()` interface — that's *why* they all work the same way even though what happens inside `.fit()` is completely different for each. Every PyTorch neural network you write in Module 16 will be a class that inherits from `torch.nn.Module`. Recognizing this pattern now means those modules won't feel like new magic later.

---

## Why Inheritance? The Problem It Solves

Imagine modeling different animals without inheritance — you'd duplicate `name` and `sound`-handling logic in every single class:

```python
class Dog:
    def __init__(self, name):
        self.name = name
    def make_sound(self):
        return f"{self.name} says Woof!"

class Cat:
    def __init__(self, name):     # duplicated!
        self.name = name
    def make_sound(self):
        return f"{self.name} says Meow!"
```

If every animal needs a shared feature later (e.g., `self.is_alive = True`), you'd have to update it in every single class. Inheritance solves this: define the shared behavior *once* in a parent class, and let subclasses inherit it automatically.

## Basic Inheritance

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        return f"{self.name} makes a sound."

class Dog(Animal):     # Dog inherits from Animal
    pass                 # no changes yet — Dog gets everything Animal has

class Cat(Animal):
    pass

rex = Dog("Rex")
whiskers = Cat("Whiskers")

print(rex.make_sound())         # Rex makes a sound.
print(whiskers.make_sound())      # Whiskers makes a sound.
```

**How it works:** `class Dog(Animal):` means "`Dog` is a subclass of `Animal`" (`Animal` is the **parent class** / **base class**; `Dog` is the **child class** / **subclass**). `Dog` automatically gets `Animal`'s `__init__` and `make_sound` — we didn't have to rewrite them.

## Overriding Methods

A subclass can **override** a parent method by defining a method with the same name — its own version replaces the parent's for that subclass.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def make_sound(self):
        return f"{self.name} makes a sound."

class Dog(Animal):
    def make_sound(self):            # overrides Animal's version
        return f"{self.name} says Woof!"

class Cat(Animal):
    def make_sound(self):            # overrides Animal's version, differently
        return f"{self.name} says Meow!"

rex = Dog("Rex")
whiskers = Cat("Whiskers")

print(rex.make_sound())         # Rex says Woof!
print(whiskers.make_sound())      # Whiskers says Meow!
```

## Extending `__init__` with `super()`

Often a subclass needs *extra* attributes on top of everything the parent already sets up. `super()` lets you call the parent's method (commonly `__init__`) from inside the child, so you don't have to duplicate its logic.

```python
class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def make_sound(self):
        return f"{self.name} says {self.sound}!"

class Dog(Animal):
    def __init__(self, name, breed):
        super().__init__(name, sound="Woof")   # runs Animal's __init__ first
        self.breed = breed                        # then adds Dog-specific data

rex = Dog("Rex", "Labrador")
print(rex.make_sound())     # Rex says Woof!
print(rex.breed)              # Labrador
```

**How it works:** `super().__init__(name, sound="Woof")` calls `Animal.__init__(self, name, sound="Woof")`, setting `self.name` and `self.sound` exactly as `Animal` would. Then `Dog.__init__` continues, adding `self.breed` — data only `Dog` objects have.

✅ **Best Practice:** Whenever a subclass's `__init__` needs everything the parent sets up *plus* more, call `super().__init__(...)` first rather than copy-pasting the parent's attribute assignments — if the parent class changes later, every subclass using `super()` picks up the change automatically.

## Polymorphism: Same Method Name, Different Behavior

**Polymorphism** ("many forms") means you can call the *same* method name on different object types and each responds in its own way, without the calling code needing to know which specific type it's dealing with.

```python
animals = [Dog("Rex", "Labrador"), Dog("Fido", "Poodle")]

class Cat(Animal):
    def __init__(self, name):
        super().__init__(name, sound="Meow")

animals.append(Cat("Whiskers"))

for animal in animals:
    print(animal.make_sound())   # each animal responds in its own way
```
```
Rex says Woof!
Fido says Woof!
Whiskers says Meow!
```

**How it works:** The loop calls `animal.make_sound()` identically for every item, but each object's *own* `make_sound` (inherited or overridden) runs — the loop code doesn't need an `if isinstance(animal, Dog): ...` check for every type.

🎯 **On the job:** This is exactly why you can write `model.fit(X, y)` once and swap `model = LinearRegression()` for `model = RandomForestClassifier()` without changing your training loop — every scikit-learn estimator implements `.fit()` polymorphically, each doing something completely different internally.

## Checking Types: `isinstance()`

```python
print(isinstance(rex, Dog))       # True
print(isinstance(rex, Animal))     # True — Dog IS an Animal (inheritance)
print(isinstance(rex, Cat))          # False
```

💡 **Tip:** `isinstance()` respects inheritance — a `Dog` object is also considered an instance of `Animal`, since `Dog` inherits from it. This is useful when writing code that should accept "any kind of Animal."

---

## Hands-On Exercise

**Task:** Write `shapes.py` that:
1. Defines a base class `Shape` with `__init__(self, name)` and a method `area(self)` that returns `0` (a placeholder — the base `Shape` doesn't know its area).
2. Defines `Rectangle(Shape)` that takes `width` and `height`, calls `super().__init__("Rectangle")`, and overrides `area()` to return `width * height`.
3. Defines `Circle(Shape)` that takes `radius`, calls `super().__init__("Circle")`, and overrides `area()` to return `3.14159 * radius ** 2`.
4. Loops over a list containing one of each shape and prints each one's name and area.

<details>
<summary>✅ Click to see the solution</summary>

```python
class Shape:
    def __init__(self, name):
        self.name = name

    def area(self):
        return 0

class Rectangle(Shape):
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

shapes = [Rectangle(4, 5), Circle(3)]

for shape in shapes:
    print(f"{shape.name}: area = {shape.area()}")
```

**Expected output:**
```
Rectangle: area = 20
Circle: area = 28.27431
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Copy-pasting the parent's `__init__` logic into every subclass | Call `super().__init__(...)` and add only what's new |
| Forgetting to call `super().__init__()` at all, losing parent setup | Always call it first thing in a subclass's `__init__` unless you deliberately want to replace parent behavior entirely |
| Writing `if isinstance(x, Dog): ... elif isinstance(x, Cat): ...` chains | Let polymorphism handle it — give each subclass its own overridden method instead |
| Deep inheritance chains (5+ levels) | Prefer shallow, focused hierarchies — 1-2 levels covers almost every real case |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Understand why inheritance avoids duplicated code
- [ ] Can create a subclass and override a parent method
- [ ] Can use `super()` to extend (not replace) a parent's `__init__`
- [ ] Can explain polymorphism with a concrete example
- [ ] Comfortable with `isinstance()` and how it respects inheritance
- [ ] Completed the `shapes.py` exercise

**Next:** Continue to [`03-dunder-methods-and-encapsulation.md`](03-dunder-methods-and-encapsulation.md)
