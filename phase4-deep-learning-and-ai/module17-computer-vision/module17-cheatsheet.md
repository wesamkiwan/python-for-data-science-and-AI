# 📋 Module 17 Cheat Sheet: Computer Vision (CNNs)

Fast reference for CNN concepts, PyTorch/Keras implementation, transfer learning, and augmentation.

## Core Concepts
```
convolution: slide a small learned filter across the image -> feature map
pooling: shrink feature maps (e.g., max pooling keeps the max of each block)
CNN architecture: [conv -> activation -> pool] x N -> flatten -> dense -> output
```
Why convolution: reuses few weights across the whole image (parameter-efficient) + preserves spatial locality.

## Loading Image Data
```python
# PyTorch (torchvision)
import torchvision, torchvision.transforms as transforms
transform = transforms.Compose([transforms.ToTensor()])   # scales to [0,1] automatically
dataset = torchvision.datasets.MNIST(root="./data", train=True, download=True, transform=transform)

# Keras (built-in)
from tensorflow import keras
(X_train, y_train), (X_test, y_test) = keras.datasets.mnist.load_data()
X_train = X_train.astype("float32") / 255.0        # manual normalize
X_train = X_train.reshape(-1, 28, 28, 1)               # manual add channel dim
```
⚠️ Channel order: PyTorch `(channels, H, W)` vs. Keras `(H, W, channels)`.

## CNN in PyTorch
```python
import torch.nn as nn

class SimpleCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(32 * 7 * 7, 64)   # size depends on input size / pooling steps!
        self.fc2 = nn.Linear(64, num_classes)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))
        x = self.pool(self.relu(self.conv2(x)))
        x = x.view(x.size(0), -1)     # flatten
        x = self.relu(self.fc1(x))
        return self.fc2(x)
```

## CNN in Keras
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
    keras.layers.Dense(num_classes, activation="softmax")
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
```

## Transfer Learning
```python
# PyTorch
import torchvision.models as models
model = models.resnet18(weights="IMAGENET1K_V1")
for param in model.parameters():
    param.requires_grad = False          # freeze pretrained base
model.fc = nn.Linear(model.fc.in_features, num_classes)   # new, trainable head

# Keras
base_model = keras.applications.MobileNetV2(input_shape=(96,96,3), include_top=False, weights="imagenet")
base_model.trainable = False              # freeze pretrained base
model = keras.Sequential([base_model, keras.layers.GlobalAveragePooling2D(), keras.layers.Dense(num_classes, activation="softmax")])
```
✅ Default approach for real projects — training from scratch rarely makes sense with limited data.

## Data Augmentation
```python
# PyTorch
import torchvision.transforms as transforms
augment = transforms.Compose([
    transforms.RandomRotation(15),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ToTensor()
])

# Keras
data_augmentation = keras.Sequential([
    keras.layers.RandomRotation(0.05),
    keras.layers.RandomFlip("horizontal"),
    keras.layers.RandomZoom(0.1)
])
```
⚠️ Choose augmentations that preserve the label's meaning (don't flip text/digits horizontally).

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Shape mismatch feeding into the first `Dense`/`Linear` after conv layers | Miscalculated the flattened size after pooling | Recompute: input_size / (2^num_pooling_layers), squared, times last conv's channel count |
| Model barely improves during training | Forgot to normalize pixel values | Scale to [0,1] (or use framework-provided normalization) |
| Transfer learning model still trains slowly / large memory | Forgot to freeze the base model | Set `requires_grad=False` (PyTorch) / `.trainable=False` (Keras) |
| Augmented images look nonsensical for the task | Wrong augmentation choice for the data type | Match augmentations to what's realistic for your images (e.g., no flips for text) |
| Channel dimension errors switching between frameworks | PyTorch vs. Keras channel order differs | PyTorch: (C,H,W); Keras: (H,W,C) |

## The "New Computer Vision Task" Workflow
1. Normalize pixel values; confirm channel order matches your framework.
2. Start with transfer learning (a pretrained model) unless you have a very large labeled dataset.
3. Freeze the pretrained base; replace/add a task-specific final layer.
4. Add data augmentation appropriate to your images.
5. Train with dropout/early stopping (Module 16d) as needed; evaluate on a genuine held-out test set.
