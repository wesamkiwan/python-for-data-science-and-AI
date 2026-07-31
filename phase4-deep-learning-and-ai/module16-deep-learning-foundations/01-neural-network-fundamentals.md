# Module 16a: Neural Network Fundamentals

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [Module 15 — Ensemble Methods & Advanced ML](../../phase3-machine-learning/module15-ensemble-advanced-ml/03-hyperparameter-tuning.md)

## 🎯 Learning Objectives
- [ ] Explain what a neural network is, in terms of neurons, layers, weights, and biases
- [ ] Explain activation functions and why they're necessary
- [ ] Trace through a forward pass by hand on a tiny example
- [ ] Explain gradient descent and backpropagation conceptually

---

## Module Goal

Welcome to **Phase 4: Deep Learning & AI**! This module builds the conceptual foundation for neural networks — the family of models behind everything from image recognition (Module 17) to large language models (Module 19) — before you write a single line of PyTorch or TensorFlow code in the next two lessons.

## Why This Matters on the Job

Every deep learning framework — PyTorch, TensorFlow, and the APIs behind every LLM you'll call in Module 19 — is built on the exact same handful of ideas: neurons, weights, activation functions, and gradient descent. Understanding these deeply, rather than just memorizing framework syntax, is what lets you debug a model that isn't learning, reason about *why* a particular architecture might work for a problem, and read new deep learning papers/tools without getting lost in unfamiliar terminology.

---

## From scikit-learn to Neural Networks: What Changes?

Recall Phase 3's `.fit()`/`.predict()` pattern (Module 12a) — it still applies here! Neural networks are still supervised (or, in some cases, unsupervised/self-supervised) learning models with the same core setup: features in, prediction out, trained on labeled data. What's new is the model's internal structure: instead of a single mathematical formula (linear regression) or a set of if/else splits (decision trees), a neural network is built from **layers of interconnected artificial neurons**, capable of learning far more complex, non-linear patterns.

## The Building Block: An Artificial Neuron

A single artificial neuron does something remarkably simple: it takes several numeric inputs, multiplies each by a learned **weight**, sums them up (plus a **bias** term), then passes that sum through an **activation function**.

```python
import numpy as np

inputs = np.array([1.0, 2.0, 3.0])      # e.g., 3 input features
weights = np.array([0.5, -0.2, 0.1])       # learned during training
bias = 0.3                                    # learned during training

weighted_sum = np.dot(inputs, weights) + bias
print(weighted_sum)   # 0.7

def relu(x):
    return np.maximum(0, x)

output = relu(weighted_sum)
print(output)   # 0.7  (positive input passes through unchanged with ReLU)
```

**How it works:** `np.dot(inputs, weights)` computes the weighted sum — exactly the same linear combination as linear regression's `intercept + coef_1*x_1 + coef_2*x_2 + ...` from Module 12c! The **weights** are precisely analogous to those regression coefficients — they're the numbers the model *learns* during training.

## Why Activation Functions Matter

If you only ever combined weighted sums (without an activation function), stacking multiple layers would mathematically collapse into a single linear equation — no matter how many layers you added, the whole network could only ever learn a straight-line relationship, exactly like `LinearRegression` (Module 12c). **Activation functions** introduce non-linearity, which is what lets deep networks learn far more complex patterns (curves, interactions, thresholds) than a single linear model ever could.

```python
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

x = np.array([-2, -1, 0, 1, 2])
print(relu(x))         # [0 0 0 1 2]              -- zero for negative input, unchanged for positive
print(sigmoid(x))         # [0.119 0.269 0.5 0.731 0.881]  -- squashes everything into (0, 1)
```

| Activation | Behavior | Common use |
|---|---|---|
| **ReLU** (Rectified Linear Unit) | `max(0, x)` — zero for negative inputs, unchanged for positive | Default choice for hidden layers in most modern networks |
| **Sigmoid** | Squashes any input into `(0, 1)` | Output layer for binary classification (interpretable as a probability) |
| **Softmax** | Converts multiple outputs into probabilities summing to 1 | Output layer for multi-class classification (used in this module's Iris examples) |

💡 **Tip:** ReLU is the default modern choice for hidden layers — it's simple, fast to compute, and avoids a technical problem (the "vanishing gradient") that older activation functions like sigmoid suffer from deep in a network. You'll see `ReLU` used constantly in the next two lessons.

## Layers: Stacking Neurons Together

A neural network organizes neurons into **layers**:

- **Input layer:** one "neuron" per input feature (not really computing anything — just holding the input values).
- **Hidden layer(s):** layers between input and output, where the actual learned computation happens. "Deep" learning simply means having multiple hidden layers.
- **Output layer:** produces the final prediction — one neuron for regression/binary classification, or one neuron per class for multi-class classification (using softmax).

💡 **Analogy:** Think of layers like an assembly line — each layer takes the previous layer's output, transforms it further, and passes it forward. Early layers might learn simple patterns (in an image: edges, colors); later layers combine those into increasingly complex, abstract patterns (shapes, then objects) — this "learning a hierarchy of features automatically" is precisely why deep learning excels at complex, unstructured data like images (Module 17) and text (Module 18).

## The Forward Pass

The **forward pass** is simply feeding an input through the network, layer by layer, to produce a prediction — exactly the calculation shown above, repeated across every neuron in every layer.

```python
# A tiny 2-input, 2-hidden-neuron, 1-output network, computed manually
inputs = np.array([1.0, 0.5])

# Hidden layer: 2 neurons, each with its own weights/bias
hidden_weights = np.array([[0.3, 0.6], [0.2, -0.4]])   # shape (2 inputs, 2 hidden neurons)
hidden_bias = np.array([0.1, 0.05])

hidden_input = inputs @ hidden_weights + hidden_bias
hidden_output = relu(hidden_input)
print(hidden_output)   # values after the first layer + activation

# Output layer: 1 neuron
output_weights = np.array([0.7, -0.3])
output_bias = 0.2

final_input = hidden_output @ output_weights + output_bias
final_output = sigmoid(final_input)   # e.g., a probability for binary classification
print(final_output)
```

**How it works:** This is the exact same idea as the single-neuron example, just applied twice (once per layer), with the first layer's output becoming the second layer's input. Every framework you'll use (PyTorch, TensorFlow) automates this exact chain of matrix multiplications — you'll never compute it by hand again after this lesson, but understanding it demystifies everything the framework does internally.

## Learning: Gradient Descent & Backpropagation

So far, we've assumed the weights are already known. But how does a network *learn* them?

1. **Forward pass:** feed training data through the network to get predictions.
2. **Loss function:** measure how wrong those predictions are compared to the true labels (conceptually similar to Module 12's MSE for regression or cross-entropy for classification).
3. **Backpropagation:** calculate exactly how much each individual weight in the network contributed to that error, working backward from the output layer to the input layer.
4. **Gradient descent:** nudge every weight slightly in the direction that reduces the error, repeat for many iterations (**epochs**).

💡 **Analogy:** Imagine trying to find the lowest point in a hilly, foggy landscape by feeling the slope under your feet and taking a small step downhill, repeatedly. **Gradient descent** is exactly this: at each step, it computes the "slope" (gradient) of the error with respect to each weight, and nudges that weight a small amount in the downhill direction. **Backpropagation** is the specific, efficient algorithm for computing that slope for every weight in a multi-layer network, by working backward from the final error.

⚠️ **Warning:** The size of each "step downhill" is controlled by the **learning rate** — too large, and training can overshoot and never settle down; too small, and training takes a very long time to improve. Tuning the learning rate is one of the most common practical challenges in deep learning, revisited in the next lessons.

🎯 **On the job:** You will never manually implement backpropagation — PyTorch and TensorFlow both compute it automatically (a feature called **automatic differentiation**), which is precisely what makes modern deep learning frameworks so powerful. But understanding that this process exists, and roughly what a "loss," "gradient," "epoch," and "learning rate" mean, is essential for debugging a model that isn't training well (e.g., loss not decreasing usually means the learning rate needs adjusting).

---

## Hands-On Exercise

**Task:** Write `forward_pass_practice.py` that:
1. Manually implements a `sigmoid` and a `relu` function using NumPy (as shown in this lesson).
2. Builds a tiny network with 3 inputs, one hidden layer of 4 neurons (using ReLU), and one output neuron (using sigmoid) — define your own weight matrices and biases (any reasonable numbers).
3. Runs a forward pass on the input `[1.0, -0.5, 2.0]` and prints the final output.
4. Explains, in a printed comment, why this output could be interpreted as a probability if this were a binary classification problem.

<details>
<summary>✅ Click to see the solution</summary>

```python
import numpy as np

def relu(x):
    return np.maximum(0, x)

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

inputs = np.array([1.0, -0.5, 2.0])

hidden_weights = np.array([
    [0.2, 0.4, -0.1, 0.3],
    [0.5, -0.3, 0.2, 0.1],
    [-0.4, 0.6, 0.3, -0.2]
])   # shape (3 inputs, 4 hidden neurons)
hidden_bias = np.array([0.1, 0.0, -0.1, 0.2])

hidden_output = relu(inputs @ hidden_weights + hidden_bias)
print(f"Hidden layer output: {hidden_output}")

output_weights = np.array([0.3, -0.5, 0.6, 0.2])
output_bias = -0.1

final_output = sigmoid(hidden_output @ output_weights + output_bias)
print(f"Final output: {final_output:.4f}")

# Because sigmoid squashes any value into the range (0, 1), this output can be
# interpreted as the model's estimated probability of the "positive" class in
# a binary classification problem -- e.g., 0.73 would mean "73% confident this
# is the positive class," exactly like LogisticRegression's predict_proba()
# from Module 12b.
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Skipping activation functions between layers | Without them, stacked layers collapse into one linear model — no better than Module 12c's `LinearRegression` |
| Confusing weights (learned) with hyperparameters (chosen) | Weights are learned automatically via gradient descent; things like learning rate, number of layers/neurons are hyperparameters you set (Module 13c/15c) |
| Assuming backpropagation must be implemented by hand | Every modern framework (PyTorch, TensorFlow) computes it automatically |
| Picking a learning rate that's too large or too small | Start with common defaults (e.g., 0.001-0.01) and adjust based on whether the loss decreases smoothly |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand neurons, weights, biases, and layers
- [ ] Understand why activation functions are necessary
- [ ] Can trace a forward pass through a small network by hand
- [ ] Understand gradient descent and backpropagation conceptually
- [ ] Completed the `forward_pass_practice.py` exercise

**Next:** Continue to [`02-building-networks-with-pytorch.md`](02-building-networks-with-pytorch.md)
