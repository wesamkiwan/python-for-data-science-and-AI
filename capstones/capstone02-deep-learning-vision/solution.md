# Capstone 2: Complete Reference Solution

Every code block below was executed and its output verified. This solution uses PyTorch; a Keras version would follow the identical structure (Module 17b/c showed both side by side).

## Step 1: Load and Inspect

```python
import torchvision
import torchvision.transforms as transforms

transform = transforms.Compose([transforms.ToTensor()])
train_dataset = torchvision.datasets.FashionMNIST(root="./data", train=True, download=True, transform=transform)
test_dataset = torchvision.datasets.FashionMNIST(root="./data", train=False, download=True, transform=transform)

print(len(train_dataset), len(test_dataset))
image, label = train_dataset[0]
print(image.shape, label)
print(train_dataset.classes)
```
```
60000 10000
torch.Size([1, 28, 28]) 9
['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
```

**Findings:** 60,000 training images, 10,000 test images, each 28×28 grayscale (1 channel). Fashion-MNIST is a balanced dataset (6,000 examples per class in the training set) — unlike Capstone 1's imbalanced churn problem, so plain accuracy is a reasonable primary metric here, though per-class metrics still matter given some categories are visually similar (`Shirt`, `T-shirt/top`, `Pullover`, `Coat` are all upper-body garments that could plausibly be confused, even by a human glancing quickly).

## Step 2: Build a Baseline CNN

```python
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Subset

# Using a subset for faster iteration during development (Module 17b's approach)
train_subset = Subset(train_dataset, range(8000))
test_subset = Subset(test_dataset, range(2000))
train_loader = DataLoader(train_subset, batch_size=64, shuffle=True)
test_loader = DataLoader(test_subset, batch_size=64, shuffle=False)

class FashionCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 32, kernel_size=3, padding=1)
        self.relu = nn.ReLU()
        self.pool = nn.MaxPool2d(2, 2)
        self.conv2 = nn.Conv2d(32, 64, kernel_size=3, padding=1)
        self.dropout = nn.Dropout(0.25)
        self.fc1 = nn.Linear(64 * 7 * 7, 128)
        self.fc2 = nn.Linear(128, 10)

    def forward(self, x):
        x = self.pool(self.relu(self.conv1(x)))   # 28x28 -> 14x14
        x = self.pool(self.relu(self.conv2(x)))      # 14x14 -> 7x7
        x = x.view(x.size(0), -1)
        x = self.dropout(x)
        x = self.relu(self.fc1(x))
        return self.fc2(x)

torch.manual_seed(42)
model = FashionCNN()
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

for epoch in range(5):
    model.train()
    total_loss = 0
    for images, labels in train_loader:
        optimizer.zero_grad()
        loss = criterion(model(images), labels)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    print(f"Epoch {epoch+1}, Avg Loss: {total_loss/len(train_loader):.4f}")
```
```
Epoch 1, Avg Loss: 0.8562
Epoch 2, Avg Loss: 0.5042
Epoch 3, Avg Loss: 0.4323
Epoch 4, Avg Loss: 0.3852
Epoch 5, Avg Loss: 0.3504
```

Training loss decreases steadily and smoothly across all 5 epochs — a healthy sign the network is learning without any obvious problems (no exploding loss, no stalling).

## Step 3: Evaluate Properly

```python
from sklearn.metrics import classification_report, confusion_matrix

model.eval()
correct, total = 0, 0
all_preds, all_labels = [], []
with torch.no_grad():
    for images, labels in test_loader:
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        all_preds.extend(predicted.tolist())
        all_labels.extend(labels.tolist())

print(f"Test Accuracy: {correct/total:.4f}")
print(classification_report(all_labels, all_preds, target_names=train_dataset.classes))
print(confusion_matrix(all_labels, all_preds))
```
```
Test Accuracy: 0.8755

              precision    recall  f1-score   support
 T-shirt/top       0.89      0.74      0.81       200
     Trouser       0.98      0.99      0.98       203
    Pullover       0.82      0.83      0.82       214
       Dress       0.91      0.76      0.83       190
        Coat       0.74      0.88      0.80       219
      Sandal       0.99      0.95      0.97       195
       Shirt       0.66      0.71      0.68       197
     Sneaker       0.91      0.98      0.95       200
         Bag       0.96      0.97      0.96       194
  Ankle boot       0.99      0.94      0.96       188

    accuracy                           0.88      2000

[[149   1   7   9   1   0  31   0   2   0]
 [  0 201   0   1   0   0   1   0   0   0]
 [  1   0 177   0  29   0   7   0   0   0]
 [  4   4   3 145  15   0  18   0   1   0]
 [  0   0  12   1 192   0  13   0   1   0]
 [  0   0   0   0   0 186   0   9   0   0]
 [ 13   0  16   3  23   0 139   0   3   0]
 [  0   0   0   0   0   0   0 197   1   2]
 [  0   0   2   0   0   1   3   0 188   0]
 [  0   0   0   0   0   1   0  10   0 177]]
```

**87.55% overall accuracy** — but that single number hides an enormous range in per-class performance: `Trouser` (F1 = 0.98), `Sandal` (0.97), and `Ankle boot` (0.96) are essentially solved, while **`Shirt` is a real weak point (F1 = 0.68)**. This is exactly why Step 1's warning about "visually similar categories" mattered, and exactly why a single accuracy number is never the whole story (Module 12b).

## Step 4: Test Data Augmentation — Honestly

```python
transform_augmented = transforms.Compose([
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.RandomRotation(10),
    transforms.ToTensor()
])
transform_plain = transforms.Compose([transforms.ToTensor()])

train_dataset_plain = torchvision.datasets.FashionMNIST(root="./data", train=True, transform=transform_plain)
train_dataset_aug = torchvision.datasets.FashionMNIST(root="./data", train=True, transform=transform_augmented)

train_subset_plain = Subset(train_dataset_plain, range(8000))
train_subset_aug = Subset(train_dataset_aug, range(8000))

def train_and_eval(train_subset, epochs=15, seed=42):
    torch.manual_seed(seed)
    loader = DataLoader(train_subset, batch_size=64, shuffle=True)
    model = FashionCNN()
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(epochs):
        model.train()
        for images, labels in loader:
            optimizer.zero_grad()
            loss = criterion(model(images), labels)
            loss.backward()
            optimizer.step()

    model.eval()
    # Test accuracy
    correct, total = 0, 0
    with torch.no_grad():
        for images, labels in test_loader:
            _, predicted = torch.max(model(images), 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    test_acc = correct / total

    # Train accuracy (on the UNAUGMENTED version, for a fair, consistent comparison)
    train_loader_check = DataLoader(train_subset_plain, batch_size=64, shuffle=False)
    correct_train, total_train = 0, 0
    with torch.no_grad():
        for images, labels in train_loader_check:
            _, predicted = torch.max(model(images), 1)
            total_train += labels.size(0)
            correct_train += (predicted == labels).sum().item()
    train_acc = correct_train / total_train

    return train_acc, test_acc

train_acc_plain, test_acc_plain = train_and_eval(train_subset_plain, epochs=15)
print(f"No augmentation   - Train acc: {train_acc_plain:.4f}, Test acc: {test_acc_plain:.4f}, Gap: {train_acc_plain - test_acc_plain:.4f}")

train_acc_aug, test_acc_aug = train_and_eval(train_subset_aug, epochs=15)
print(f"With augmentation - Train acc: {train_acc_aug:.4f}, Test acc: {test_acc_aug:.4f}, Gap: {train_acc_aug - test_acc_aug:.4f}")
```
```
No augmentation   - Train acc: 0.9513, Test acc: 0.8965, Gap: 0.0548
With augmentation - Train acc: 0.9210, Test acc: 0.8860, Gap: 0.0350
```

⚠️ **Honest finding — augmentation did NOT improve raw test accuracy here** (0.8965 → 0.8860, actually slightly *lower*). If we stopped at just comparing final test scores, we'd wrongly conclude augmentation "didn't work."

**But look at the train/test gap** (Module 13c's overfitting diagnostic): the gap shrank meaningfully, from **0.0548 (no augmentation) to 0.0350 (with augmentation)** — the augmented model is demonstrably overfitting *less*. This is exactly what augmentation is supposed to do (Module 17c) — it's just that, in this specific setup (a fairly small 8,000-image subset and only 15 epochs), the *reduced overfitting* didn't translate into a *higher* test score this time.

**Why this is a genuinely useful, honest finding, not a failed experiment:**
- Augmentation's benefit typically shows up more clearly with **more training epochs** (letting the model fully exploit the added variety) or a **smaller original dataset** (where overfitting is a more severe problem to begin with). Neither model here has fully converged at 15 epochs.
- A real data scientist reports what the numbers actually show, including inconclusive or mixed results — not just the version of the story that sounds cleanest. This is exactly the discipline Module 10 and Module 15 both emphasized: separate what the data clearly demonstrates from what would need further work to confirm.
- **Recommendation for further work:** re-run this comparison with more epochs and/or the full 60,000-image training set (rather than the 8,000-image development subset) before drawing a final conclusion about whether augmentation is worth including in the production model.

## Step 5: Interpret the Confusion Matrix

Looking at the confusion matrix from Step 3, focusing on `Shirt` (row/column index 6, the weakest class):

| Confused with | Count | Plausible reason |
|---|---|---|
| T-shirt/top | 13 | Both are short-sleeved upper-body garments — silhouette can look nearly identical at 28×28 resolution |
| Coat | 23 | Both can have long sleeves and a similar boxy silhouette |
| Pullover | 16 | Shirts and pullovers can have very similar necklines/shapes without color or texture detail |

**T-shirt/top** is also confused with **Shirt** in the reverse direction (31 times) — this is clearly a genuinely hard, mutually-confusing pair for the model, not a one-directional quirk.

**Business implication:** this confusion isn't surprising — even a human glancing quickly at a small, low-resolution product photo might struggle to distinguish a shirt from a thin coat or pullover without more visual detail (color, texture, buttons) than 28×28 grayscale pixels provide. This points to a genuine **resolution/detail limitation** of the dataset itself, not just a modeling shortfall.

## Step 6: Business Recommendation

> **Findings:** Our CNN classifier achieves 87.6% overall accuracy across the 10 product categories on a representative subset, with near-perfect performance on distinctive categories (Trouser, Sandal, Ankle Boot, Sneaker, Bag — all F1 ≥ 0.95) and a clear weak spot on visually similar upper-body garments, particularly `Shirt` (F1 = 0.68), which is most often confused with `T-shirt/top`, `Coat`, and `Pullover`.
>
> We also tested data augmentation as a way to improve generalization; it reduced overfitting (a smaller gap between training and test accuracy) but did not yet improve the final test accuracy at our current training budget — we'd want to test this further with more epochs and the full dataset before deciding whether to include it in production training.
>
> **Recommendation:** Deploy this model as a **first-pass auto-tagger with mandatory human review specifically for the `Shirt`, `T-shirt/top`, `Coat`, and `Pullover` categories** — these four categories account for the overwhelming majority of misclassifications, while every other category can likely be trusted with much lighter spot-checking. This targeted approach still removes the majority of manual tagging work (6 of 10 categories are highly reliable) while protecting catalog accuracy specifically where the model is weakest. Once deployed, we'd recommend the Module 20 monitoring approach — logging predictions and confidence scores, and periodically re-checking accuracy on newly tagged items — to catch any drift as new product styles enter the catalog.

---

**Next:** [`portfolio-presentation.md`](portfolio-presentation.md) — how to present this project.
