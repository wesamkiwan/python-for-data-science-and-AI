# Starter Guide: Product Image Categorization Capstone

Use this as a scaffold — it tells you *what* to figure out at each stage, not *how*. Try each step yourself before peeking at `solution.md`.

## Step 1: Load and Inspect

- Load Fashion-MNIST via `torchvision.datasets.FashionMNIST` (or Keras' built-in loader).
- What's the shape of a single image? How many training/test examples are there?
- Check the class balance — is it a balanced dataset (equal examples per category), or skewed?
- Look at a few example images from a couple of different classes (e.g., `Shirt` vs. `T-shirt/top`). Do any categories look like they'll be visually hard to distinguish, even for a human?

## Step 2: Build a Baseline CNN

- Design a CNN with at least 2 convolutional layers (each followed by pooling), a dropout layer, and dense layers ending in a 10-class output — following Module 17a/b's architecture pattern.
- Given the full 60,000-image training set can be slow to iterate on, consider training on a smaller subset first (as Module 17b did) while you're still developing and debugging your architecture.
- Train for a handful of epochs. Is the training loss decreasing steadily?

## Step 3: Evaluate Properly

- Report overall test accuracy.
- Also generate a full `classification_report` (precision/recall/F1 per class) and a `confusion_matrix`.
- Which categories have the lowest per-class F1 score? Look at the confusion matrix rows/columns for those categories — which OTHER category are they most often confused with?

## Step 4: Test Data Augmentation — Honestly

- Add at least 2 augmentations appropriate for photographic product images (recall Module 17c's warning: choose augmentations that preserve the label's meaning for *this specific* kind of image).
- Train a second model, identical architecture, using the augmented data.
- Compare BOTH train accuracy and test accuracy between the two models, not just the final test score. What does the *gap* between train and test accuracy tell you about overfitting in each case (Module 13c)?
- Does augmentation actually improve test accuracy here? If not, is there still evidence it's doing something useful (hint: look at the train/test gap, not just the raw test number)? Don't force a conclusion that isn't supported by your actual numbers.

## Step 5: Interpret the Confusion Matrix

- Pick the 2-3 category pairs that get confused most often. Can you explain *why*, based on what these clothing items typically look like?
- Is this confusion likely to be a real problem for the business (Step 6), or a relatively low-stakes mixup?

## Step 6: Write a Business Recommendation

- Given your accuracy and the specific confusion patterns you found, would you recommend deploying this model to fully automate tagging, or as a "first pass with human review for uncertain cases"?
- If you'd recommend human review for some cases, which specific categories would you flag for it, and why?
- What would you want to test or measure before actually deploying this (tie back to Module 20's monitoring lesson)?

---

Once you've worked through this yourself, compare with [`solution.md`](solution.md).
