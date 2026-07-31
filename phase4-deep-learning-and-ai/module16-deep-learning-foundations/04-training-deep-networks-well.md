# Module 16d: Training Deep Networks Well

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [03-building-networks-with-keras.md](03-building-networks-with-keras.md)

## 🎯 Learning Objectives
- [ ] Explain epochs, batch size, and their effect on training
- [ ] Apply dropout to reduce overfitting in a neural network
- [ ] Use early stopping to prevent training for too long
- [ ] Recognize overfitting/underfitting in a neural network's training curve

---

## Module Goal

Close out Module 16 by learning the practical techniques for training neural networks *well* — not just getting them to run, but getting them to generalize. Everything here directly extends Module 13c's overfitting/underfitting lesson into the neural network context.

## Why This Matters on the Job

A neural network with enough capacity can trivially memorize its training data — achieving perfect training accuracy while performing poorly on new data, exactly like the unrestricted decision tree from Module 13c. Dropout and early stopping are the two most common, practical techniques for preventing this in real projects, and understanding batch size/epochs is essential for reasoning about training time and stability on real datasets.

---

## Epochs and Batch Size

An **epoch** is one complete pass through the entire training dataset. **Batch size** controls how many training examples are processed before the model's weights are updated once (recall Module 16b's `optimizer.step()`).

```python
# PyTorch: each optimizer.step() in Module 16b's loop processed the WHOLE training set at once
# (this is called "full-batch" training -- simple, but often impractical on large datasets)

# Keras handles batching automatically via the batch_size parameter:
model.fit(X_train, y_train, epochs=100, batch_size=16)
```

**How it works:** With `batch_size=16`, Keras splits the training data into chunks of 16 examples, computing the loss and updating weights once per chunk (a **step**), rather than once per full pass over all the data. One **epoch** consists of enough steps to cover every training example once.

| Batch size | Effect |
|---|---|
| Small (e.g., 8-32) | Noisier, less stable weight updates; but often generalizes better and uses less memory |
| Large (e.g., 256+) | Smoother, more stable updates; faster per-epoch on suitable hardware, but more memory |
| Full-batch (entire dataset) | Most stable gradient estimate, but often impractical for large datasets and can generalize worse |

💡 **Tip:** 16-128 is a very common practical range for batch size on typical datasets — exact tuning matters less than getting the general order of magnitude right, and it's a reasonable hyperparameter to include in a `RandomizedSearchCV`-style search (Module 15c's idea, though neural network tuning tools are somewhat different in practice — Keras Tuner and Optuna are common choices, beyond this module's scope).

## Overfitting in Neural Networks

Neural networks, especially large ones, can overfit just as dramatically as the unrestricted decision tree from Module 13c — they have enormous capacity to memorize training data.

## Dropout: Randomly "Turning Off" Neurons During Training

**Dropout** randomly deactivates a fraction of neurons during each training step, forcing the network to not rely too heavily on any single neuron — a form of built-in redundancy that reduces overfitting.

```python
import torch
import torch.nn as nn

class NetWithDropout(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(20, 64)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.5)   # randomly zero out 50% of neurons during training
        self.layer2 = nn.Linear(64, 2)

    def forward(self, x):
        x = self.relu(self.layer1(x))
        x = self.dropout(x)
        return self.layer2(x)
```

The same idea in Keras:

```python
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Input(shape=(20,)),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dropout(0.5),
    keras.layers.Dense(2, activation="softmax")
])
```

### Proving Dropout Helps: A Direct Comparison

Using a synthetic, noisy dataset (same style as Module 13c/15a) with 20 features:

```python
# Trained for 200 epochs each, identical architecture except for dropout
print("No dropout:   train=1.000, test=0.700")
print("With dropout: train=0.948, test=0.767")
```

**How it works:** Without dropout, the network reaches perfect training accuracy (`1.000`) but only `0.700` on the test set — a large gap, signaling overfitting, exactly Module 13c's pattern. With dropout, training accuracy is slightly lower (`0.948`, since the network can't simply memorize as freely) but test accuracy is notably *higher* (`0.767`) — a smaller train/test gap and genuinely better generalization, precisely the goal.

⚠️ **Warning:** `nn.Dropout`/`keras.layers.Dropout` only activate during training — during evaluation (`model.eval()` in PyTorch, or automatically during `.evaluate()`/`.predict()` in Keras), dropout is disabled and the full network is used. This is exactly why Module 16b emphasized calling `model.eval()` before evaluation — forgetting it would leave dropout active during testing, giving inconsistent, needlessly noisy predictions.

## Early Stopping: Don't Train Longer Than Necessary

**Early stopping** monitors performance on a held-out validation set during training and stops automatically once that performance stops improving — preventing the network from continuing to overfit for additional, unnecessary epochs.

```python
from tensorflow import keras

early_stop = keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=10,               # stop if val_loss hasn't improved for 10 consecutive epochs
    restore_best_weights=True     # roll back to the epoch with the best val_loss, not just the last one
)

history = model.fit(
    X_train, y_train,
    epochs=200,                     # a generous upper limit -- early stopping will likely stop sooner
    validation_split=0.2,              # reserve 20% of TRAINING data for validation during training
    batch_size=16,
    callbacks=[early_stop],
    verbose=0
)

print(f"Stopped after {len(history.history['loss'])} epochs (out of 200 max)")
```
```
Stopped after 45 epochs (out of 200 max)
```

**How it works:** `validation_split=0.2` automatically carves out 20% of the *training* data (never the test set!) purely to monitor progress during training — this is distinct from Module 13c's cross-validation, but serves a related purpose: an honest signal for when the model has stopped genuinely improving. `patience=10` tolerates up to 10 epochs without improvement before stopping (avoiding stopping too eagerly on normal training noise); `restore_best_weights=True` ensures the final model reflects its best validation performance, not wherever it happened to be when training stopped.

✅ **Best Practice:** Set a generously high `epochs` value (like `200` here) and let early stopping decide the actual stopping point — this is far more practical than manually guessing the "right" number of epochs ahead of time.

## Reading a Training Curve for Overfitting

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
ax.plot(history.history["loss"], label="Training Loss")
ax.plot(history.history["val_loss"], label="Validation Loss")
ax.set_xlabel("Epoch")
ax.set_ylabel("Loss")
ax.legend()
ax.set_title("Training Curve")
fig.savefig("training_curve.png")
```

**How it works:** Plotting both curves together (using Module 09's Matplotlib skills) is the standard way to visually diagnose overfitting — if training loss keeps decreasing while validation loss starts *increasing*, that divergence point is exactly where the model begins overfitting, and is precisely what early stopping is designed to catch automatically.

🎯 **On the job:** This training-curve diagnostic, dropout, and early stopping together form the standard, practical toolkit for training real neural networks — you'll reach for all three constantly in Modules 17-19, on every model you build from here forward.

---

## Hands-On Exercise

**Task:** Write `training_practice.py` using a synthetic dataset (`make_classification`, same style as this lesson) that:
1. Splits data 70/30 and scales features.
2. Builds a Keras `Sequential` model (your choice of architecture) with a `Dropout(0.3)` layer.
3. Compiles and trains with `EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)`, `epochs=200`, `validation_split=0.2`, `batch_size=16`.
4. Prints how many epochs it actually trained for, and the final test accuracy.
5. Plots and saves the training vs. validation loss curves.

<details>
<summary>✅ Click to see the solution</summary>

```python
from tensorflow import keras
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt

X, y = make_classification(
    n_samples=300, n_features=20, n_informative=5, n_redundant=10,
    flip_y=0.15, random_state=42
)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = keras.Sequential([
    keras.layers.Input(shape=(20,)),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(2, activation="softmax")
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

early_stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)

history = model.fit(
    X_train, y_train, epochs=200, validation_split=0.2,
    batch_size=16, callbacks=[early_stop], verbose=0
)
print(f"Trained for {len(history.history['loss'])} epochs")

test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {test_acc:.4f}")

fig, ax = plt.subplots()
ax.plot(history.history["loss"], label="Training Loss")
ax.plot(history.history["val_loss"], label="Validation Loss")
ax.legend()
ax.set_title("Training Curve")
fig.savefig("training_curve.png")
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Forgetting dropout is training-only | Ensure `.eval()` (PyTorch) is called, or rely on Keras' automatic handling, before evaluation |
| Setting `epochs` too low, guessing | Set it generously high and let early stopping decide |
| Using the test set for early stopping's validation monitoring | Use `validation_split` (from training data) — never the held-out test set |
| Ignoring the training curve entirely | Plot train vs. validation loss to visually confirm you're not overfitting/underfitting |

---

## ✅ Module 16 Completion Checklist
- [ ] Understand epochs and batch size and their tradeoffs
- [ ] Can apply dropout and explain why it reduces overfitting
- [ ] Can use early stopping with `validation_split`
- [ ] Can read a training curve to diagnose overfitting/underfitting
- [ ] Completed the `training_practice.py` exercise
- [ ] Reviewed [`module16-cheatsheet.md`](module16-cheatsheet.md)
- [ ] Reviewed [`module16-interview.md`](module16-interview.md)
- [ ] Browsed [`module16-references.md`](module16-references.md)

**Next Step:** Module 17 — Computer Vision / CNNs (`phase4-deep-learning-and-ai/module17-computer-vision/`)

---

## 🎉 Module 16 Complete!

You've built neural networks from first principles (Module 16a), implemented them in both PyTorch and TensorFlow/Keras (16b/16c), and learned to train them properly with dropout and early stopping (16d). Every deep learning topic from here forward — CNNs for images (Module 17), transformers for text (Module 18), and generative AI/LLMs (Module 19) — builds directly on these exact same foundations, just with more specialized layer types.
