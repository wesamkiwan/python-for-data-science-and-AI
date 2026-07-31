# Capstone 2: Automated Product Image Categorization (CNN Classifier)

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 4-6h | **Unlocks after:** Module 17 (Computer Vision / CNNs)

## 🎯 What This Capstone Demonstrates

This project applies **Module 16 (Deep Learning Foundations)** and **Module 17 (Computer Vision / CNNs)** to a realistic computer vision business problem — building an image classifier from scratch, evaluating it properly, and critically examining a common "should obviously help" technique (data augmentation) with genuine rigor rather than assuming it works.

---

## 📋 The Scenario

You're a data scientist at **ThreadLine**, an online clothing retailer. Sellers upload thousands of new product photos every week, and each one needs to be tagged with a category (T-shirt, Dress, Sneaker, etc.) before it can appear correctly in the catalog and search filters. Right now, this tagging is done manually — slow, inconsistent, and a growing bottleneck as the catalog scales.

> "Can you build a model that automatically categorizes a product photo into one of our 10 core categories? It doesn't need to be perfect — even getting most of the easy cases right would free up our catalog team to focus on the genuinely ambiguous ones."

## 📦 What You're Given

- **Dataset:** [Fashion-MNIST](https://github.com/zalandoresearch/fashion-mnist) — 70,000 grayscale, 28×28 product images across 10 categories: `T-shirt/top`, `Trouser`, `Pullover`, `Dress`, `Coat`, `Sandal`, `Shirt`, `Sneaker`, `Bag`, `Ankle boot`. This is a real, widely-used benchmark dataset (not synthetic) — genuinely built by a clothing retailer (Zalando) for exactly this kind of product-categorization task, making it an unusually direct match for this scenario.
- Loadable directly via `torchvision.datasets.FashionMNIST(download=True)` (or `keras.datasets.fashion_mnist.load_data()`) — no manual download needed, it fetches automatically on first use (see Module 17b).

## ✅ Requirements

Your deliverable is a complete analysis and model that:

1. **Loads and inspects the data** — confirm shape, class balance, and look at a few example images per class (Module 17b).
2. **Builds a CNN from scratch** — at least 2 convolutional layers with pooling, plus dense layers, following Module 17a/b's architecture pattern.
3. **Trains and evaluates properly** — report overall accuracy AND a full per-class classification report + confusion matrix (not just one accuracy number — some categories are visually much harder to tell apart than others).
4. **Tests data augmentation honestly** — apply at least 2 augmentations (Module 17c) and compare against the non-augmented baseline using BOTH train and test accuracy (to check its effect on overfitting, not just its effect on the final score). Report what you actually find, even if it's not a clean "augmentation wins" story — real ML work often isn't.
5. **Interprets the confusion matrix** — identify which categories the model confuses most often, and connect this to a plausible visual/business explanation.
6. **Writes a business-facing recommendation** — should this model be deployed as-is, used as a "first pass" with human review for uncertain cases, or does it need more work? Be specific about which categories would need the most human oversight.

## 🗂️ Folder Contents

- `starter-guide.md` — scaffolded questions to work through yourself first.
- `solution.md` — the complete, fully-executed reference solution with all code and verified output.
- `portfolio-presentation.md` — guidance on presenting this project in a portfolio or interview.

## 💡 How to Use This Capstone

1. Work through it yourself using `starter-guide.md` for structure.
2. Compare against `solution.md` — pay particular attention to the data augmentation section, since it demonstrates a genuinely important lesson: a technique that's "supposed to help" doesn't always show a clean win in every setting, and a good data scientist reports that honestly rather than cherry-picking a result.
3. Read `portfolio-presentation.md` once you're happy with your version.

---

**Next:** [`starter-guide.md`](starter-guide.md) →
