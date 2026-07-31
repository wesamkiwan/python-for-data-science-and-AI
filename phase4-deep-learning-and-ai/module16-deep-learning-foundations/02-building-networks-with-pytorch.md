# Module 16b: Building Neural Networks with PyTorch

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 2h | **Prerequisites:** [01-neural-network-fundamentals.md](01-neural-network-fundamentals.md)

## 🎯 Learning Objectives
- [ ] Create and manipulate PyTorch tensors
- [ ] Define a neural network with `nn.Module`
- [ ] Write a complete PyTorch training loop
- [ ] Evaluate a trained PyTorch model

---

## Module Goal

Build your first real neural network using **PyTorch**, one of the two dominant deep learning frameworks (alongside TensorFlow, next lesson) and the most widely used framework in research and increasingly in production. You'll implement every concept from the last lesson — layers, activation functions, the forward pass, gradient descent — using PyTorch's tools instead of manual NumPy.

## Why This Matters on the Job

PyTorch's explicit, "you write the training loop yourself" style gives you full visibility and control over exactly what happens during training — which is precisely why it dominates research and is increasingly the default choice in industry too. Every concept from Module 16a (forward pass, loss, backpropagation, gradient descent) becomes concrete, visible Python code in this lesson, rather than something hidden inside a framework.

---

## Installing PyTorch

```bash
pip install torch
```

## Tensors: PyTorch's Core Data Structure

A PyTorch **tensor** is essentially a NumPy array (Module 06) with extra deep-learning-specific superpowers: automatic gradient tracking and GPU support.

```python
import torch

x = torch.tensor([1.0, 2.0, 3.0])
print(x)              # tensor([1., 2., 3.])
print(x.shape)           # torch.Size([3])

a = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
b = torch.tensor([[5.0, 6.0], [7.0, 8.0]])
print(a + b)                 # element-wise addition, exactly like NumPy
print(a @ b)                    # matrix multiplication
```

**How it works:** PyTorch tensors support the exact same vectorized operations and broadcasting rules from Module 06 — if NumPy felt familiar, PyTorch tensors will too. You can even convert directly between them:

```python
import numpy as np

arr = np.array([1, 2, 3])
tensor_from_numpy = torch.from_numpy(arr)
print(tensor_from_numpy)
```

### Automatic Differentiation: PyTorch's "Magic"

Recall Module 16a's gradient descent — PyTorch computes gradients (the "slope" used to update weights) automatically:

```python
w = torch.tensor(2.0, requires_grad=True)   # track gradients for this tensor
y = w ** 2

y.backward()          # computes dy/dw automatically (backpropagation!)
print(w.grad)             # tensor(4.0) -- the derivative of w^2 at w=2 is 2w = 4
```

**How it works:** `requires_grad=True` tells PyTorch to track every operation performed on `w`, building an internal computation graph. Calling `.backward()` on the final result triggers **automatic differentiation** — PyTorch walks that graph backward, computing the exact gradient of `y` with respect to `w` (and every other tracked tensor involved), with zero manual calculus required. This is precisely the backpropagation mechanism from Module 16a, made concrete.

## Defining a Neural Network with `nn.Module`

```python
import torch.nn as nn

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()   # exactly Module 03's super().__init__() pattern!
        self.layer1 = nn.Linear(4, 16)   # 4 inputs -> 16 hidden neurons
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(16, 3)      # 16 hidden neurons -> 3 outputs (3 classes)

    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        return x

model = SimpleNet()
print(model)
```

**How it works:** This is a direct application of Module 03's OOP lesson — `SimpleNet` is a class inheriting from `nn.Module`, calling `super().__init__()` to set up the parent's required internal state, exactly like the `Dog(Animal)` example from Module 03b. `nn.Linear(4, 16)` creates one "layer" — internally, a weight matrix and bias vector, initialized randomly, exactly like Module 16a's manual weight matrices, but managed automatically. The `forward()` method defines the forward pass — precisely the chain of operations from Module 16a's manual example, now expressed with PyTorch's building blocks instead of raw NumPy.

## The Training Loop

Unlike scikit-learn's one-line `.fit()` (Module 12), PyTorch requires you to write the training loop explicitly — giving you full visibility into every step from Module 16a.

```python
import torch
import torch.nn as nn
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)      # scaling matters for neural networks too (Module 13a)
X_test = scaler.transform(X_test)

# Convert to PyTorch tensors with the right dtypes
X_train_t = torch.tensor(X_train, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.long)     # long (integer) for classification labels
X_test_t = torch.tensor(X_test, dtype=torch.float32)
y_test_t = torch.tensor(y_test, dtype=torch.long)

model = SimpleNet()
criterion = nn.CrossEntropyLoss()                          # the LOSS FUNCTION from Module 16a
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)     # Adam: a common, effective gradient descent variant

epochs = 100
for epoch in range(epochs):
    optimizer.zero_grad()               # 1. reset gradients from the previous step
    outputs = model(X_train_t)             # 2. forward pass
    loss = criterion(outputs, y_train_t)      # 3. compute the loss
    loss.backward()                              # 4. backpropagation -- compute gradients
    optimizer.step()                                # 5. gradient descent -- update the weights

    if (epoch + 1) % 20 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")
```
```
Epoch 20, Loss: 0.6118
Epoch 40, Loss: 0.2868
Epoch 60, Loss: 0.1732
Epoch 80, Loss: 0.1069
Epoch 100, Loss: 0.0783
```

**How it works, mapping directly to Module 16a's four steps:**
1. `optimizer.zero_grad()` — PyTorch accumulates gradients by default, so you must clear them before each new step, or they'd incorrectly stack across iterations.
2. `model(X_train_t)` — the **forward pass**: calling the model like a function runs `.forward()` internally.
3. `criterion(outputs, y_train_t)` — computes the **loss**: `CrossEntropyLoss` is the standard choice for multi-class classification (conceptually similar to how `LogisticRegression`, Module 12b, is evaluated, but used *during* training here, not just for final evaluation).
4. `loss.backward()` — **backpropagation**: automatically computes how much every weight in the network contributed to the loss.
5. `optimizer.step()` — **gradient descent**: nudges every weight slightly in the direction that reduces the loss, using the `lr=0.01` learning rate.

Notice the steadily decreasing loss across epochs — direct, visible evidence the network is learning, exactly as Module 16a described.

## Evaluating the Trained Model

```python
model.eval()    # switch to evaluation mode (matters more with certain layers, Module 16d)

with torch.no_grad():   # disable gradient tracking -- we're not training, just predicting
    test_outputs = model(X_test_t)
    _, predicted_classes = torch.max(test_outputs, 1)   # pick the highest-scoring class per sample
    accuracy = (predicted_classes == y_test_t).float().mean()
    print(f"Test Accuracy: {accuracy.item():.4f}")
```
```
Test Accuracy: 1.0000
```

**How it works:** `torch.no_grad()` tells PyTorch not to bother tracking gradients during this block — we're only predicting, not training, so this saves memory/computation. `torch.max(test_outputs, 1)` finds the highest-scoring output neuron per sample (`dim=1`, across the 3 class-score columns) — exactly analogous to how `LogisticRegression.predict()` (Module 12b) picks the most likely class from `predict_proba()`'s scores.

🎯 **On the job:** This exact train-loop skeleton (`zero_grad` → forward → loss → `backward` → `step`, repeated for many epochs) is the foundation of virtually every PyTorch project you'll ever write, from a simple classifier like this to the transformer architectures in Module 18.

---

## Hands-On Exercise

**Task:** Write `pytorch_practice.py` that:
1. Loads `load_wine()` from `sklearn.datasets`, splits 80/20 with `random_state=42`, and scales features with `StandardScaler`.
2. Defines a `nn.Module` subclass with one hidden layer of 32 neurons (ReLU activation) taking Wine's 13 features, outputting 3 class scores.
3. Trains it for 150 epochs using `CrossEntropyLoss` and the `Adam` optimizer with `lr=0.01`, printing the loss every 30 epochs.
4. Evaluates test accuracy using the `torch.no_grad()` pattern shown in this lesson.

<details>
<summary>✅ Click to see the solution</summary>

```python
import torch
import torch.nn as nn
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

X_train_t = torch.tensor(X_train, dtype=torch.float32)
y_train_t = torch.tensor(y_train, dtype=torch.long)
X_test_t = torch.tensor(X_test, dtype=torch.float32)
y_test_t = torch.tensor(y_test, dtype=torch.long)

class WineNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(13, 32)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(32, 3)

    def forward(self, x):
        x = self.layer1(x)
        x = self.relu(x)
        x = self.layer2(x)
        return x

model = WineNet()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

for epoch in range(150):
    optimizer.zero_grad()
    outputs = model(X_train_t)
    loss = criterion(outputs, y_train_t)
    loss.backward()
    optimizer.step()
    if (epoch + 1) % 30 == 0:
        print(f"Epoch {epoch+1}, Loss: {loss.item():.4f}")

model.eval()
with torch.no_grad():
    test_outputs = model(X_test_t)
    _, predicted = torch.max(test_outputs, 1)
    accuracy = (predicted == y_test_t).float().mean()
    print(f"Test Accuracy: {accuracy.item():.4f}")
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Forgetting `optimizer.zero_grad()` each iteration | Gradients accumulate by default — always clear them before each new forward/backward pass |
| Wrong tensor dtype (e.g., using `float` labels for classification) | Classification labels need `dtype=torch.long`; features need `dtype=torch.float32` |
| Forgetting `model.eval()` and `torch.no_grad()` during evaluation | Both matter for correctness and efficiency at inference time |
| Skipping feature scaling | Neural networks are gradient-based, just like logistic regression (Module 13a) — scale your features |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Can create and manipulate PyTorch tensors
- [ ] Understand automatic differentiation (`requires_grad`, `.backward()`)
- [ ] Can define a network with `nn.Module`
- [ ] Can write a complete training loop and evaluate the trained model
- [ ] Completed the `pytorch_practice.py` exercise

**Next:** Continue to [`03-building-networks-with-keras.md`](03-building-networks-with-keras.md)
