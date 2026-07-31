# 📋 Module 16 Cheat Sheet: Deep Learning Foundations

Fast reference for neural network concepts, PyTorch, and TensorFlow/Keras.

## Core Concepts
```
neuron: weighted_sum(inputs) + bias  ->  activation function  ->  output
layer: many neurons, same input
forward pass: input -> layer -> layer -> ... -> output
loss function: measures how wrong predictions are
backpropagation: computes each weight's contribution to the loss
gradient descent: nudges weights to reduce the loss, repeated over epochs
```

## Activation Functions
| Function | Behavior | Use |
|---|---|---|
| ReLU | `max(0, x)` | Default for hidden layers |
| Sigmoid | squashes to (0, 1) | Binary classification output |
| Softmax | probabilities summing to 1 | Multi-class classification output |

## PyTorch
```python
import torch
import torch.nn as nn

# Tensors
x = torch.tensor([1.0, 2.0], dtype=torch.float32)
x.requires_grad_(True)   # or requires_grad=True at creation -- track gradients

# Define a network
class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.layer1 = nn.Linear(in_features, hidden)
        self.relu = nn.ReLU()
        self.layer2 = nn.Linear(hidden, out_features)
    def forward(self, x):
        return self.layer2(self.relu(self.layer1(x)))

model = Net()
criterion = nn.CrossEntropyLoss()                       # classification
optimizer = torch.optim.Adam(model.parameters(), lr=0.01)

# Training loop
for epoch in range(epochs):
    optimizer.zero_grad()      # 1. clear old gradients
    outputs = model(X_train)      # 2. forward pass
    loss = criterion(outputs, y_train)   # 3. compute loss
    loss.backward()                         # 4. backpropagation
    optimizer.step()                           # 5. update weights

# Evaluation
model.eval()
with torch.no_grad():
    predictions = model(X_test)
    _, predicted_classes = torch.max(predictions, 1)
```

## TensorFlow/Keras
```python
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Input(shape=(n_features,)),
    keras.layers.Dense(hidden, activation="relu"),
    keras.layers.Dropout(0.3),                          # optional
    keras.layers.Dense(n_classes, activation="softmax")
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
history = model.fit(X_train, y_train, epochs=100, batch_size=16, validation_split=0.2, verbose=0)

test_loss, test_acc = model.evaluate(X_test, y_test)
predictions = model.predict(X_test)         # softmax probabilities
predicted_classes = predictions.argmax(axis=1)
```

## PyTorch vs. Keras

| | PyTorch | Keras |
|---|---|---|
| Training loop | Explicit, manual | Hidden inside `.fit()` |
| Code volume | More | Less |
| Control | Full, step-by-step | High-level |
| Best for | Research, custom logic | Rapid prototyping, standard architectures |

## Overfitting Prevention
```python
# Dropout -- PyTorch
nn.Dropout(0.5)      # randomly zero 50% of neurons DURING TRAINING ONLY

# Dropout -- Keras
keras.layers.Dropout(0.5)

# Early stopping -- Keras
early_stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
model.fit(..., validation_split=0.2, callbacks=[early_stop])
```

## Batch Size & Epochs
| Term | Meaning |
|---|---|
| Epoch | One full pass through the training data |
| Batch size | Number of samples processed per weight update |
| Small batch | Noisier updates, often generalizes better |
| Large batch | Smoother/faster updates, more memory |

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Loss not decreasing | Learning rate too high/low, or forgot `optimizer.zero_grad()` | Adjust `lr`; check the training loop |
| `RuntimeError` about tensor dtype | Wrong dtype (e.g., float labels for classification) | Labels: `torch.long`; features: `torch.float32` |
| Train accuracy 1.0, test much lower | Overfitting | Add dropout, use early stopping, get more data |
| Both train and test accuracy low | Underfitting | Bigger network, more epochs, check learning rate |
| Dropout seems to have no effect at test time | Correct — it's disabled automatically during eval/`.predict()` | Not a bug — verify with `.eval()` (PyTorch) |

## The "New Neural Network" Workflow
1. Scale features (Module 13a) — gradient-based, just like logistic regression.
2. Choose architecture: input size, hidden layer(s), output size/activation (sigmoid/softmax).
3. PyTorch: write the explicit training loop. Keras: `.compile()` + `.fit()`.
4. Add `Dropout` and use `EarlyStopping`/a validation split to control overfitting.
5. Evaluate on the untouched test set; plot the training curve to sanity-check.
