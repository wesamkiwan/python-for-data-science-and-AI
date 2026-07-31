# Module 16c: Building Neural Networks with TensorFlow/Keras

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [02-building-networks-with-pytorch.md](02-building-networks-with-pytorch.md)

## 🎯 Learning Objectives
- [ ] Build the same network from Module 16b using TensorFlow/Keras
- [ ] Use `Sequential`, `.compile()`, and `.fit()`
- [ ] Compare PyTorch's and Keras' approaches to the same problem
- [ ] Decide which framework to reach for in different situations

---

## Module Goal

Build the identical Wine-classification network from the last lesson using **TensorFlow's Keras API** — the other dominant deep learning framework, known for its more concise, higher-level style. By the end, you'll be able to read and write both frameworks confidently, and understand the tradeoffs between them.

## Why This Matters on the Job

TensorFlow (via Keras) remains extremely widely used in industry, especially for production deployment (TensorFlow Serving, TensorFlow Lite for mobile/edge devices) and in teams with an established TensorFlow codebase. Job postings frequently list "PyTorch or TensorFlow" — being comfortable with both, and understanding that the underlying concepts (Module 16a) are identical regardless of framework, makes you flexible rather than locked into one ecosystem.

---

## Installing TensorFlow

```bash
pip install tensorflow
```

## Keras: TensorFlow's High-Level API

**Keras** is TensorFlow's official high-level API for building neural networks — dramatically more concise than PyTorch's explicit style, at the cost of somewhat less visibility into the exact training mechanics.

```python
import tensorflow as tf
from tensorflow import keras
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = keras.Sequential([
    keras.layers.Input(shape=(4,)),
    keras.layers.Dense(16, activation="relu"),
    keras.layers.Dense(3, activation="softmax")
])

model.summary()
```
```
Model: "sequential"
+--------------------------------------------------------------------------+
| Layer (type)                    | Output Shape           |       Param # |
|---------------------------------+------------------------+---------------|
| dense (Dense)                   | (None, 16)             |            80 |
|---------------------------------+------------------------+---------------|
| dense_1 (Dense)                 | (None, 3)              |            51 |
+--------------------------------------------------------------------------+
 Total params: 131 (524.00 B)
 Trainable params: 131 (524.00 B)
 Non-trainable params: 0 (0.00 B)
```

**How it works:** `keras.Sequential([...])` builds a network by simply listing its layers in order — this is precisely the same architecture as Module 16b's `SimpleNet` (4 inputs → 16 hidden neurons with ReLU → 3 outputs), just expressed far more concisely, since Keras handles the `nn.Module`/`forward()` boilerplate internally. `.summary()` is a convenient built-in that prints the exact architecture and parameter count — useful for sanity-checking a network's shape, and notably something PyTorch doesn't provide built-in (though the `torchinfo` package adds similar functionality).

## `.compile()`: Configuring How the Model Learns

```python
model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)
```

**How it works:** `.compile()` is where Keras condenses several of Module 16b's explicit PyTorch pieces into one call: `optimizer="adam"` is the same Adam optimizer from the last lesson; `loss="sparse_categorical_crossentropy"` is functionally the same as PyTorch's `nn.CrossEntropyLoss()` (the `"sparse"` prefix just means the labels are plain integers, like `0`/`1`/`2`, rather than one-hot encoded vectors); `metrics=["accuracy"]` tells Keras to track and report accuracy automatically during training, something you had to compute manually at the end in PyTorch.

## `.fit()`: Training the Model

```python
history = model.fit(X_train, y_train, epochs=100, verbose=0)

for epoch_index in [19, 39, 59, 79, 99]:
    print(f"Epoch {epoch_index+1}, Loss: {history.history['loss'][epoch_index]:.4f}")
```
```
Epoch 20, Loss: 0.6767
Epoch 40, Loss: 0.4774
Epoch 60, Loss: 0.3604
Epoch 80, Loss: 0.2905
Epoch 100, Loss: 0.2441
```

**How it works:** `.fit()` runs the *entire* Module 16b training loop internally — the zero_grad/forward/loss/backward/step cycle happens automatically, for every epoch, in one call. This is the single biggest practical difference from PyTorch: Keras trades away explicit step-by-step visibility for dramatically less boilerplate. `history.history["loss"]` retrieves the loss recorded at every epoch, in case you want to inspect or plot the training curve (using Module 09's Matplotlib skills) afterward.

🎯 **On the job:** This `Sequential` → `.compile()` → `.fit()` pattern will feel immediately familiar if you already know scikit-learn's `.fit()`/`.predict()` (Module 12) — Keras deliberately mirrors that same simple, high-level ergonomics, just for neural networks specifically.

## Evaluating the Model

```python
test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {test_accuracy:.4f}")

predictions = model.predict(X_test, verbose=0)   # returns probabilities per class (from softmax)
predicted_classes = predictions.argmax(axis=1)      # pick the highest-probability class per sample
```

**How it works:** `.evaluate()` computes the loss and every metric specified in `.compile()` (here, just accuracy) on new data in one call — directly comparable to scikit-learn's `.score()` (Module 12). `.predict()` returns the raw softmax probabilities for each class; `.argmax(axis=1)` (a NumPy method, Module 06) picks the index of the highest probability — exactly the same idea as PyTorch's `torch.max(..., 1)` from the last lesson.

## PyTorch vs. Keras: A Direct Comparison

| Step | PyTorch (Module 16b) | Keras (this lesson) |
|---|---|---|
| Define architecture | `class Net(nn.Module): ...` with explicit `forward()` | `keras.Sequential([layer1, layer2, ...])` |
| Configure training | Separate `criterion` and `optimizer` objects | One `.compile(optimizer=..., loss=..., metrics=...)` call |
| Train | Explicit loop: `zero_grad` → forward → loss → `backward` → `step`, per epoch | One `.fit(X, y, epochs=...)` call |
| Evaluate | Manual `torch.no_grad()` block + manual accuracy calculation | One `.evaluate(X, y)` call |
| Visibility into each step | Full — every line is explicit | Less — training loop is hidden inside `.fit()` |
| Conciseness | More code, more control | Less code, less low-level control |

✅ **Best Practice:** Neither framework is objectively "better" — PyTorch's explicitness is valued in research and when you need fine-grained custom training logic (common in Module 18's transformer models); Keras' conciseness is valued for rapid prototyping and standard architectures where the default training loop is exactly what you need. Many data scientists comfortably use both, choosing based on the team/project's existing codebase and the specific flexibility a task requires.

---

## Hands-On Exercise

**Task:** Write `keras_practice.py` that rebuilds Module 16b's exercise (the Wine classification network) in Keras:
1. Loads `load_wine()`, splits 80/20 with `random_state=42`, and scales features.
2. Builds a `Sequential` model: 13 inputs → Dense(32, relu) → Dense(3, softmax).
3. Compiles with `adam`, `sparse_categorical_crossentropy`, and `accuracy` metric.
4. Trains for 150 epochs (`verbose=0`), printing the loss at epochs 30, 60, 90, 120, 150.
5. Evaluates and prints test accuracy.
6. Writes a short comment comparing the amount of code needed here vs. the PyTorch version from Module 16b.

<details>
<summary>✅ Click to see the solution</summary>

```python
from tensorflow import keras
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42
)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = keras.Sequential([
    keras.layers.Input(shape=(13,)),
    keras.layers.Dense(32, activation="relu"),
    keras.layers.Dense(3, activation="softmax")
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

history = model.fit(X_train, y_train, epochs=150, verbose=0)
for epoch_index in [29, 59, 89, 119, 149]:
    print(f"Epoch {epoch_index+1}, Loss: {history.history['loss'][epoch_index]:.4f}")

test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {test_accuracy:.4f}")

# Compared to Module 16b's PyTorch version, this required no explicit training
# loop, no manual zero_grad/backward/step calls, and no manual accuracy
# calculation -- .compile() + .fit() + .evaluate() replaced all of that,
# at the cost of not seeing each individual training step explicitly.
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Using `categorical_crossentropy` with plain integer labels | Use `sparse_categorical_crossentropy` for integer labels; `categorical_crossentropy` expects one-hot encoded labels |
| Forgetting `metrics=["accuracy"]` in `.compile()` | Without it, `.evaluate()` only returns loss, not accuracy |
| Assuming Keras hides *everything* — it doesn't | You can still access per-epoch history, custom callbacks, and more when needed |
| Thinking you must choose PyTorch OR Keras forever | Many teams/projects use both; the underlying concepts (Module 16a) transfer completely between them |

---

## ✅ Module Completion Checklist (Part C)
- [ ] Can build a network with `keras.Sequential`
- [ ] Can configure training with `.compile()` and train with `.fit()`
- [ ] Can evaluate with `.evaluate()` and predict with `.predict()`
- [ ] Can compare PyTorch's and Keras' approaches and articulate the tradeoffs
- [ ] Completed the `keras_practice.py` exercise

**Next:** Continue to [`04-training-deep-networks-well.md`](04-training-deep-networks-well.md)
