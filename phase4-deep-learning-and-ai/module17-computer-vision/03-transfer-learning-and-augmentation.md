# Module 17c: Transfer Learning & Data Augmentation

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1h | **Prerequisites:** [02-building-cnns.md](02-building-cnns.md)

## 🎯 Learning Objectives
- [ ] Explain transfer learning and why it's the standard practical approach to computer vision
- [ ] Load a pretrained model and adapt it to a new task in both PyTorch and Keras
- [ ] Explain data augmentation and why it helps with limited training data
- [ ] Apply data augmentation in both frameworks

---

## Module Goal

Learn **transfer learning** — reusing a model already trained on a massive dataset, rather than training a CNN entirely from scratch — and **data augmentation** — artificially expanding a training set by creating modified copies of existing images. Together, these are the two most practically important techniques for real-world computer vision, where you rarely have millions of labeled images like the giants who train the base models you'll reuse.

## Why This Matters on the Job

Training a CNN from scratch (Module 17b) requires enormous amounts of labeled data and compute to reach strong performance — completely impractical for most real projects, which might only have a few hundred or thousand labeled images. Transfer learning and data augmentation are exactly how real-world computer vision projects overcome this, and are used in the overwhelming majority of production image classification systems.

---

## Why Train From Scratch Rarely Makes Sense

Module 17b's MNIST CNN worked well partly because MNIST is simple and has 60,000 training images. Most real business problems — classifying defective products, categorizing user-uploaded photos, identifying plant diseases — have far fewer labeled examples, often just hundreds. Training a CNN with millions of parameters (Module 17b noted a CNN can easily have over 100,000 parameters even for a tiny task) from scratch on a small dataset overfits badly, exactly like Module 13c's overfitting lesson.

## Transfer Learning: Reusing What's Already Been Learned

**Transfer learning** takes a model already trained on a huge, general-purpose dataset (most commonly ImageNet — 1.4 million images across 1,000 categories) and adapts it to a new, specific task — reusing the early layers' already-learned general features (edges, textures, shapes — recall Module 17a's "hierarchy of features" idea) and only retraining the final layers for the new task.

💡 **Analogy:** Think of it like hiring someone who already has years of general photography experience and just needs to learn your company's specific product catalog, rather than teaching photography from absolute zero. The general skill (recognizing shapes, edges, textures) transfers; only the specific, final task needs new training.

### Transfer Learning in PyTorch

```python
import torch
import torch.nn as nn
import torchvision.models as models

# Load a model pretrained on ImageNet (downloads weights on first use)
model = models.resnet18(weights="IMAGENET1K_V1")

# Freeze all existing layers -- their learned features stay fixed
for param in model.parameters():
    param.requires_grad = False

# Replace the final classification layer for OUR new task (e.g., 10 classes instead of 1000)
num_features = model.fc.in_features   # 512 -- the size of ResNet18's final feature representation
model.fc = nn.Linear(num_features, 10)

# Only the NEW final layer has requires_grad=True (unfrozen) by default
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
total_params = sum(p.numel() for p in model.parameters())
print(f"Trainable: {trainable_params}, Total: {total_params}")
```
```
Trainable: 5130, Total: 11181642
```

**How it works:** `requires_grad = False` on every existing parameter "freezes" them — during training, gradients still flow through for the forward pass calculation, but `optimizer.step()` (Module 16b) won't update frozen weights. Replacing `model.fc` (ResNet's final layer) with a brand-new `nn.Linear(512, 10)` creates a fresh layer with `requires_grad=True` by default — only this new layer's `5,130` parameters get trained, out of the network's `11,181,642` total. Training proceeds with the *exact same* loop from Module 16b/17b — nothing about the training process itself changes, only which parameters actually get updated.

### Transfer Learning in Keras

```python
from tensorflow import keras

base_model = keras.applications.MobileNetV2(
    input_shape=(96, 96, 3), include_top=False, weights="imagenet"
)
base_model.trainable = False   # freeze the pretrained base

model = keras.Sequential([
    base_model,
    keras.layers.GlobalAveragePooling2D(),
    keras.layers.Dense(10, activation="softmax")   # new, trainable output layer
])

model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
```
```
Total params: 2,270,794 (8.66 MB)
Trainable params: 12,810 (50.04 KB)
Non-trainable params: 2,257,984 (8.61 MB)
```

**How it works:** `include_top=False` loads MobileNetV2 *without* its original 1000-class output layer, keeping only the pretrained feature-extracting layers. `base_model.trainable = False` freezes them, exactly like PyTorch's `requires_grad = False` loop. `GlobalAveragePooling2D()` condenses the base model's final feature maps down to one vector per image (a common alternative to `Flatten()` for transfer learning specifically), feeding into a fresh, trainable `Dense(10)` output layer — again, only `12,810` of the `2,270,794` total parameters actually get trained.

✅ **Best Practice:** Freezing the pretrained base and training only the new final layer(s) is called **feature extraction** — the simplest, fastest transfer learning approach, and a strong default starting point. A more advanced variant, **fine-tuning**, unfreezes some of the later pretrained layers too (with a much smaller learning rate) for potentially better performance once feature extraction alone isn't sufficient — worth exploring once the basics here feel solid.

🎯 **On the job:** Transfer learning is so effective and standard that starting from scratch on any real computer vision task is now the exception, not the rule — the first question on any new image classification project is almost always "which pretrained model should we start from?" rather than "how do we design a CNN architecture from zero?"

## Data Augmentation: Artificially Expanding Your Training Data

**Data augmentation** creates modified versions of existing training images (rotated, flipped, zoomed, slightly recolored) on the fly during training — giving the model more varied examples to learn from without collecting any new data, directly reducing overfitting (Module 13c/16d) on a limited dataset.

### In PyTorch (via `torchvision.transforms`)

```python
import torchvision.transforms as transforms

augment = transforms.Compose([
    transforms.RandomRotation(15),           # randomly rotate up to 15 degrees
    transforms.RandomHorizontalFlip(p=0.5),      # 50% chance of a horizontal flip
    transforms.ToTensor()
])
```

### In Keras (as network layers)

```python
from tensorflow import keras

data_augmentation = keras.Sequential([
    keras.layers.RandomRotation(0.05),      # rotate up to ~5% of a full circle
    keras.layers.RandomFlip("horizontal"),
    keras.layers.RandomZoom(0.1)               # randomly zoom in/out up to 10%
])
```

**How it works:** Both frameworks apply these transformations randomly, differently, on *every* training epoch — so the model effectively sees countless slightly-different variations of each original image across training, rather than the exact same fixed image repeatedly. This is applied only during training (never during evaluation, exactly like dropout, Module 16d) — a digit rotated 10 degrees is still the same digit, so teaching the model to be robust to small realistic variations like this genuinely improves how well it generalizes to new, real-world images.

⚠️ **Warning:** Choose augmentations that make sense for your actual data — flipping a photo of a handwritten "6" horizontally would turn it into something resembling a different character, which could actively *hurt* the model rather than help it. Always sanity-check that an augmentation preserves the label's meaning for your specific task (rotating a photo of a cat is fine; horizontally flipping text is usually not).

---

## Hands-On Exercise

**Task:** Write `transfer_learning_practice.py` that (in **either** PyTorch or Keras — your choice, matching this lesson's examples):
1. Loads a pretrained model (`resnet18` in PyTorch, or `MobileNetV2`/similar in Keras).
2. Freezes its existing layers and replaces the final layer for a hypothetical 5-class classification task.
3. Prints the trainable vs. total parameter counts, and calculates what percentage of the network is actually being trained.
4. Defines a data augmentation pipeline (rotation + horizontal flip, at minimum) appropriate for general photographic images (not text/digits).
5. Writes a short comment explaining why this combination (transfer learning + augmentation) is especially valuable when you only have a few hundred labeled training images.

<details>
<summary>✅ Click to see the solution (PyTorch version)</summary>

```python
import torch.nn as nn
import torchvision.models as models
import torchvision.transforms as transforms

model = models.resnet18(weights="IMAGENET1K_V1")

for param in model.parameters():
    param.requires_grad = False

num_features = model.fc.in_features
model.fc = nn.Linear(num_features, 5)   # 5 classes for our hypothetical task

trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
total_params = sum(p.numel() for p in model.parameters())
percent_trainable = (trainable_params / total_params) * 100
print(f"Trainable: {trainable_params}, Total: {total_params}, Percent trainable: {percent_trainable:.2f}%")

augment = transforms.Compose([
    transforms.RandomRotation(15),
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(brightness=0.2, contrast=0.2),
    transforms.ToTensor()
])

# With only a few hundred labeled images, training a CNN from scratch would
# badly overfit -- there simply isn't enough data to learn general features
# like edges and textures on our own. Transfer learning reuses those general
# features from a model already trained on 1.4 million ImageNet images, so we
# only need to learn the small, task-specific final layer. Data augmentation
# further stretches our limited real images into many varied training
# examples, reducing overfitting on that already-small dataset even further.
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Training a CNN from scratch on a small dataset | Use transfer learning as the default starting point |
| Forgetting to freeze the pretrained base's parameters | Explicitly set `requires_grad = False` (PyTorch) or `.trainable = False` (Keras) |
| Applying augmentations that change the label's meaning | Choose augmentations appropriate to your specific data (e.g., avoid flips for text) |
| Applying augmentation during evaluation | Augmentation is a training-only technique, exactly like dropout |

---

## ✅ Module 17 Completion Checklist
- [ ] Understand why transfer learning is the standard practical approach to computer vision
- [ ] Can load a pretrained model, freeze it, and adapt the final layer in PyTorch and/or Keras
- [ ] Understand data augmentation and why it helps with limited training data
- [ ] Can apply data augmentation appropriate to a given dataset
- [ ] Completed the `transfer_learning_practice.py` exercise
- [ ] Reviewed [`module17-cheatsheet.md`](module17-cheatsheet.md)
- [ ] Reviewed [`module17-interview.md`](module17-interview.md)
- [ ] Browsed [`module17-references.md`](module17-references.md)

**Next Step:** Module 18 — NLP & Transformers (`phase4-deep-learning-and-ai/module18-nlp-transformers/`)
