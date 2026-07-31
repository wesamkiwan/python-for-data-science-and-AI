# Module 17b: Building CNNs with PyTorch & Keras

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 2h | **Prerequisites:** [01-cnn-fundamentals.md](01-cnn-fundamentals.md)

## 🎯 Learning Objectives
- [ ] Load and prepare an image dataset for a CNN
- [ ] Build a CNN classifier in PyTorch using `Conv2d` and `MaxPool2d`
- [ ] Build the equivalent CNN in TensorFlow/Keras using `Conv2D` and `MaxPooling2D`
- [ ] Train and evaluate both, comparing results

---

## Module Goal

Implement Module 17a's convolution/pooling concepts as a real, trainable CNN in both PyTorch and TensorFlow/Keras — classifying handwritten digits from the classic **MNIST** dataset, a standard "hello world" benchmark for computer vision.

## Why This Matters on the Job

MNIST is deliberately simple (small, grayscale, well-cleaned images) so you can focus entirely on the architecture and training mechanics without fighting data-loading complexity — exactly the right first real image dataset to build confidence with CNNs, before Module 17c's transfer learning tackles more realistic, complex images.

---

## Loading Image Data: MNIST

MNIST contains 70,000 grayscale images of handwritten digits (0-9), each 28×28 pixels.

### In PyTorch (via `torchvision`)

```bash
pip install torchvision
```

```python
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader

transform = transforms.Compose([transforms.ToTensor()])   # converts images to tensors, scales to [0, 1]

train_dataset = torchvision.datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_dataset = torchvision.datasets.MNIST(root="./data", train=False, download=True, transform=transform)

print(len(train_dataset), len(test_dataset))   # 60000 10000
image, label = train_dataset[0]
print(image.shape, label)                            # torch.Size([1, 28, 28]) 5
```

**How it works:** `download=True` fetches MNIST automatically the first time (then caches locally, exactly like Module 12c's `fetch_california_housing`). `transforms.ToTensor()` converts each image into a PyTorch tensor and automatically scales pixel values from `[0, 255]` to `[0, 1]` — a form of feature scaling (Module 13a) specifically suited to images. The image shape `(1, 28, 28)` means 1 color channel (grayscale — color images would have 3, for red/green/blue) by 28×28 pixels.

`DataLoader` handles batching (Module 16d) automatically:

```python
train_loader = DataLoader(train_dataset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False)
```

### In Keras (built-in)

```python
from tensorflow import keras

(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
print(X_train.shape, y_train.shape)   # (60000, 28, 28) (60000,)

# Normalize pixel values to [0, 1] and add the channel dimension
X_train = X_train.astype("float32") / 255.0
X_test = X_test.astype("float32") / 255.0
X_train = X_train.reshape(-1, 28, 28, 1)
X_test = X_test.reshape(-1, 28, 28, 1)
```

**How it works:** Keras' built-in MNIST loader returns plain NumPy arrays, requiring you to manually normalize (`/255.0`) and reshape to add the channel dimension — PyTorch's `transforms.ToTensor()` does both automatically. Note Keras' channel dimension convention is `(height, width, channels)` — the reverse order from PyTorch's `(channels, height, width)`, a common point of confusion when switching between frameworks.

## Building a CNN in PyTorch

```python
import torch
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)    # 1 input channel -> 16 filters
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, 2)                                 # 2x2 max pooling
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)          # 16 -> 32 filters
        self.fc1 = nn.Linear(32 * 7 * 7, 64)                                 # flatten -> dense
        self.fc2 = nn.Linear(64, 10)                                            # 10 output classes (digits 0-9)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))    # conv -> activation -> pool (28x28 -> 14x14)
        x = self.pool(self.relu(self.conv2(x)))       # conv -> activation -> pool (14x14 -> 7x7)
        x = x.view(x.size(0), -1)                          # flatten: (batch, 32, 7, 7) -> (batch, 32*7*7)
        x = self.relu(self.fc1(x))
        x = self.fc2(x)
        return x
```

**How it works:** `nn.Conv2d(1, 16, kernel_size=3, padding=1)` creates 16 different learnable 3×3 filters, each scanning the single-channel input (`padding=1` keeps the output the same 28×28 size, rather than shrinking at the edges). Each `MaxPool2d(2, 2)` halves the spatial dimensions (28→14→7). `x.view(x.size(0), -1)` is PyTorch's flatten operation — reshaping the final `(batch, 32, 7, 7)` feature maps into `(batch, 32*7*7)`, ready for the `Linear` (dense) layers from Module 16, exactly matching Module 17a's architecture diagram.

## Training the PyTorch CNN

```python
model = SimpleCNN()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(3):
    model.train()
    total_loss = 0
    for images, labels in train_loader:
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Avg Loss: {total_loss/len(train_loader):.4f}")

model.eval()
correct, total = 0, 0
with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print(f"Test Accuracy: {correct/total:.4f}")
```

**How it works:** This is the *exact same* training loop pattern from Module 16b — the only difference from a plain feedforward network is the model architecture itself (`SimpleCNN` instead of a stack of `Linear` layers). Notice `DataLoader` handles batching automatically here (unlike Module 16b's full-batch example), so the loop now has an inner `for images, labels in train_loader:` step to process one batch at a time.

## Building the Same CNN in Keras

```python
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Input(shape=(28, 28, 1)),
    keras.layers.Conv2D(16, kernel_size=3, padding="same", activation="relu"),
    keras.layers.MaxPooling2D(2),
    keras.layers.Conv2D(32, kernel_size=3, padding="same", activation="relu"),
    keras.layers.MaxPooling2D(2),
    keras.layers.Flatten(),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dense(10, activation="softmax")
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
history = model.fit(X_train, y_train, epochs=3, batch_size=64, verbose=0)

test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
print(f"Test Accuracy: {test_accuracy:.4f}")
```

**How it works:** Directly mirrors the PyTorch architecture — `Conv2D(16, ...)` then `MaxPooling2D(2)` then `Conv2D(32, ...)` then `MaxPooling2D(2)`, then `Flatten()` (Keras' built-in flatten layer, doing exactly what `.view()` did manually in PyTorch), then the same `Dense(64)` → `Dense(10, softmax)` output. `padding="same"` is Keras' equivalent of PyTorch's `padding=1` here — both keep the spatial size unchanged after each convolution.

| | PyTorch | Keras |
|---|---|---|
| Convolution | `nn.Conv2d(in_channels, out_channels, kernel_size, padding)` | `keras.layers.Conv2D(filters, kernel_size, padding, activation)` |
| Pooling | `nn.MaxPool2d(pool_size, stride)` | `keras.layers.MaxPooling2D(pool_size)` |
| Flatten | `x.view(x.size(0), -1)` (manual, in `forward()`) | `keras.layers.Flatten()` (a layer) |
| Activation | Separate `nn.ReLU()` layer/call | `activation="relu"` argument on the layer itself |

🎯 **On the job:** Both frameworks converge on essentially the same total accuracy on a dataset like MNIST — the choice between them, once again (Module 16c), usually comes down to team convention and how much explicit control you need over training, not raw capability.

---

## Hands-On Exercise

**Task:** Write `cnn_practice.py` that builds and trains a CNN on MNIST **in either PyTorch or Keras (your choice)**:
1. Load MNIST (use a reasonable subset, e.g., the first 5,000 training images and 1,000 test images, for faster iteration while learning).
2. Build a CNN with at least 2 convolutional layers (each followed by pooling) and 1-2 dense layers, matching this lesson's architecture style.
3. Train for at least 3 epochs, printing the loss each epoch.
4. Evaluate and print the final test accuracy.
5. In a comment, note how many total parameters your model has (via `model.summary()` in Keras, or by summing `p.numel() for p in model.parameters()` in PyTorch) and briefly compare that to how many parameters an equivalent plain feedforward network (Module 16, flattening the image directly) would need for its first layer alone.

<details>
<summary>✅ Click to see the solution (PyTorch version)</summary>

```python
import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, Subset

transform = transforms.Compose([transforms.ToTensor()])
train_dataset = torchvision.datasets.MNIST(root="./data", train=True, download=True, transform=transform)
test_dataset = torchvision.datasets.MNIST(root="./data", train=False, download=True, transform=transform)

train_subset = Subset(train_dataset, range(5000))
test_subset = Subset(test_dataset, range(1000))
train_loader = DataLoader(train_subset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_subset, batch_size=64, shuffle=False)

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(32 * 7 * 7, 64)
        self.fc2 = nn.Linear(64, 10)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)
        x = self.relu(self.fc1(x))
        return self.fc2(x)

model = SimpleCNN()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(3):
    model.train()
    total_loss = 0
    for images, labels in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(images), labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Avg Loss: {total_loss/len(train_loader):.4f}")

model.eval()
correct, total = 0, 0
with torch.no_grad():
    for images, labels in test_loader:
        _, predicted = torch.max(model(images), 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
print(f"Test Accuracy: {correct/total:.4f}")

total_params = sum(p.numel() for p in model.parameters())
print(f"Total CNN parameters: {total_params}")
# A plain feedforward network flattening the 28x28=784 pixel image directly
# into even a modest 64-neuron first layer would need 784*64 = 50,176 weights
# for JUST that first layer -- versus this CNN's convolutional layers, which
# reuse a small set of filters across the entire image.
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Forgetting to normalize pixel values to [0, 1] | Always scale image data, exactly like any other feature (Module 13a) |
| Mixing up channel order between frameworks | PyTorch: `(channels, height, width)`; Keras: `(height, width, channels)` |
| Forgetting the channel dimension for grayscale images | Reshape to include it explicitly (`1` for grayscale, `3` for RGB) |
| Manually computing flatten dimensions incorrectly in PyTorch | Double-check the spatial size after each pooling step (28→14→7 here) before defining `nn.Linear` |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Can load and prepare MNIST in both PyTorch and Keras
- [ ] Can build a CNN with `Conv2d`/`Conv2D` and `MaxPool2d`/`MaxPooling2D`
- [ ] Can train and evaluate a CNN in either framework
- [ ] Understand the parameter-efficiency advantage of convolution over flattening
- [ ] Completed the `cnn_practice.py` exercise

**Next:** Continue to [`03-transfer-learning-and-augmentation.md`](03-transfer-learning-and-augmentation.md)
