# 🎤 Module 17 Interview Prep: Computer Vision (CNNs)

## Conceptual Questions

### 🟢 Beginner

**Q: Why don't we just flatten an image and feed it into a plain feedforward network?**
> A: Flattening destroys the 2D spatial structure, so the network loses any inherent sense that nearby pixels are related — making it much harder to learn patterns like edges or shapes. It also requires an enormous number of weights (one per pixel per neuron in the first layer), which is both computationally wasteful and prone to severe overfitting. Convolutional layers solve both problems by reusing a small set of filters across the whole image and preserving spatial locality.

**Q: What does a convolutional filter actually do?**
> A: It's a small grid of learned weights that slides across the image, computing a weighted sum at each position — functioning as a local pattern detector (e.g., detecting edges, corners, or textures). The same filter is reused at every position in the image, which is what makes convolution so parameter-efficient compared to a fully-connected layer.

**Q: What is pooling, and why is it used?**
> A: Pooling (most commonly max pooling) reduces the size of a feature map by summarizing small regions down to a single representative value. It reduces computation in later layers and makes the network more robust to small shifts in exactly where a detected pattern appears in the image.

### 🟡 Intermediate

**Q: Explain transfer learning and why it's the standard approach for most real-world computer vision projects.**
> A: Transfer learning starts from a model already trained on a massive, general dataset (commonly ImageNet), reusing its early layers' already-learned general features (edges, textures, shapes) and only retraining a new final layer for the specific task at hand. This matters because most real projects have far too little labeled data to train a large CNN from scratch without severe overfitting — transfer learning gets strong performance from a fraction of the data and compute that training from scratch would require.

**Q: How would you adapt a pretrained ImageNet model (1000 classes) to classify your own dataset with only 5 classes?**
> A: I'd load the pretrained model, freeze all of its existing layers (setting `requires_grad=False` in PyTorch, or `.trainable=False` in Keras) so their learned features stay fixed, then replace the final classification layer with a new one sized for 5 outputs instead of 1000. Only this new layer's parameters would then be trained on my dataset, while the rest of the network continues extracting the same general features it already learned from ImageNet.

**Q: Why does data augmentation help when you have a limited training dataset?**
> A: It artificially creates varied versions of existing images (rotated, flipped, zoomed) on the fly during training, exposing the model to more diversity than the raw dataset alone provides — without needing to collect any new data. This directly reduces overfitting, since the model can't simply memorize a small, fixed set of exact images; it must learn patterns robust enough to survive reasonable, realistic variations.

## Practical/Coding Questions

**Q: Write PyTorch code that freezes a pretrained ResNet18's layers and adapts it for a new 20-class classification task.**
```python
import torch.nn as nn
import torchvision.models as models

model = models.resnet18(weights="IMAGENET1K_V1")

for param in model.parameters():
    param.requires_grad = False

model.fc = nn.Linear(model.fc.in_features, 20)
```
> Explanation: freezing every existing parameter preserves the pretrained features; replacing `model.fc` (ResNet's final layer) with a fresh `nn.Linear` creates a new, trainable output layer sized for the new number of classes.

**Q: Write a Keras data augmentation pipeline appropriate for classifying photos of animals, and explain your choices.**
```python
from tensorflow import keras

data_augmentation = keras.Sequential([
    keras.layers.RandomFlip("horizontal"),   # an animal facing left vs. right is still the same animal
    keras.layers.RandomRotation(0.1),           # small rotations are realistic camera angle variations
    keras.layers.RandomZoom(0.1)                    # zoom variation mimics different photo distances
])
```
> Explanation: each augmentation is chosen because it preserves the label's meaning for photographic animal images — a horizontally-flipped or slightly rotated/zoomed animal photo is still clearly the same class, unlike, say, flipping a photo of text.

## Scenario Questions

**Q: You have only 300 labeled images for a new product-defect classification task and need a model in production quickly. What approach would you take?**
> A: I'd start with transfer learning from a pretrained model (e.g., ResNet or MobileNet), freezing the base and training only a new final layer on my 300 images — training from scratch would badly overfit with so little data. I'd also apply data augmentation (rotations, flips, slight color/brightness jitter, chosen to still look like realistic product photos) to further stretch the effective size of my training set, and use dropout/early stopping (Module 16d) to guard against overfitting on the small new layer's training.

**Q: A CNN trained on clean, well-lit product photos performs poorly on real customer-submitted photos with varied lighting and angles. What might you investigate?**
> A: I'd first check whether the training data's variety matches the real-world conditions the model needs to handle — if training images were all clean and well-lit, the model likely hasn't learned to be robust to the lighting/angle variation present in real customer photos. I'd add data augmentation that specifically mimics this real-world variability (brightness/contrast jitter, rotation, perhaps simulated blur), and if feasible, incorporate some real, messier customer photos into training rather than relying solely on augmented clean images.

## "Gotcha" Questions

**Q: A PyTorch CNN throws a shape mismatch error at the first `nn.Linear` layer after the convolutional layers. What's the most likely cause?**
> A: The `in_features` size passed to `nn.Linear` doesn't match the actual flattened size of the feature maps coming out of the convolutional/pooling layers. This size depends on the input image's dimensions and how many pooling steps were applied (each 2×2 max pool halves both spatial dimensions) — it needs to be calculated precisely (e.g., a 28×28 input after two 2×2 poolings becomes 7×7, times the final number of channels) rather than guessed.

**Q: Someone applies a `RandomHorizontalFlip` augmentation while training a model to recognize handwritten digits. Why might this hurt performance?**
> A: Horizontally flipping a digit can change its actual meaning or make it look like an invalid/different character (e.g., flipping certain digits can make them resemble entirely different shapes) — the augmentation doesn't preserve the label's meaning for this specific data type. Augmentations must be chosen based on what realistically preserves the correct label for the actual images being used, not applied as a generic default.

## Quick-Fire Rapid Review

- Q: What does a convolutional filter detect? → **local patterns (edges, textures, shapes) via a weighted sum over a small image patch**
- Q: Why is convolution more parameter-efficient than a fully-connected layer on images? → **the same small filter is reused across the entire image**
- Q: What does pooling do? → **shrinks feature maps, reducing computation and adding robustness to small shifts**
- Q: What dataset are most pretrained vision models originally trained on? → **ImageNet**
- Q: What must you do to a pretrained model's existing layers before fine-tuning just the final layer? → **freeze them (`requires_grad=False` / `.trainable=False`)**
- Q: Does data augmentation apply during evaluation? → **No — training only, like dropout**
- Q: PyTorch's channel order vs. Keras' for images? → **PyTorch: (C,H,W); Keras: (H,W,C)**
- Q: When is training a CNN from scratch (no transfer learning) actually reasonable? → **when you have a very large labeled dataset, similar in spirit to ImageNet's scale**
