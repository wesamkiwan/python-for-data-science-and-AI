# 🎤 Module 16 Interview Prep: Deep Learning Foundations

## Conceptual Questions

### 🟢 Beginner

**Q: What does a single artificial neuron compute?**
> A: It takes several numeric inputs, multiplies each by a learned weight, sums them together with a bias term, and passes that sum through an activation function to produce its output. The weighted sum itself is structurally identical to a linear regression formula (Module 12c) — the activation function is what makes a neural network capable of more than a single model's linear relationship.

**Q: Why are activation functions necessary in a neural network?**
> A: Without them, stacking multiple layers of neurons would mathematically collapse into one single linear transformation, no matter how many layers were stacked — the network could only ever learn a straight-line relationship, exactly like plain linear regression. Activation functions introduce non-linearity, which is what allows deep networks to learn far more complex patterns.

**Q: What's the difference between a parameter (weight) and a hyperparameter in a neural network?**
> A: Weights (and biases) are learned automatically during training via gradient descent — you never set them directly. Hyperparameters are choices you make before training: the number of layers, neurons per layer, learning rate, batch size, and so on — these control *how* learning happens but aren't themselves learned from the data.

### 🟡 Intermediate

**Q: Explain backpropagation and gradient descent, and how they work together.**
> A: Backpropagation is the algorithm that computes exactly how much each individual weight in the network contributed to the final prediction error (the loss), working backward from the output layer to the input layer using calculus (the chain rule). Gradient descent then uses those computed gradients to nudge every weight slightly in the direction that reduces the loss, repeating this process over many iterations (epochs) until the loss stops meaningfully improving. Backpropagation computes *how* to adjust; gradient descent performs the actual adjustment.

**Q: How does dropout reduce overfitting, and why is it only active during training?**
> A: Dropout randomly deactivates a fraction of neurons on each training step, preventing the network from relying too heavily on any single neuron or narrow combination of neurons — this forces the network to learn more redundant, robust representations, similar in spirit to how Random Forest's bagging (Module 15a) reduces variance by preventing any single feature/split from dominating. It's disabled during evaluation because at prediction time you want the full, complete network making the best possible prediction, not a randomly weakened version of it.

**Q: What's the practical difference between PyTorch and Keras, given that both implement the same underlying concepts?**
> A: PyTorch requires writing the training loop explicitly (`zero_grad`, forward pass, loss, `backward`, `step`, per epoch), giving full visibility and fine-grained control — valuable in research or when custom training logic is needed. Keras condenses that same process into `.compile()` and `.fit()`, trading away step-by-step visibility for dramatically less code — valuable for rapid prototyping and standard architectures. The underlying mathematical concepts (Module 16a) are identical in both; only the amount of boilerplate and control differs.

## Practical/Coding Questions

**Q: Write a minimal PyTorch training loop for a classification model, given `model`, `criterion`, `optimizer`, `X_train`, and `y_train` are already defined.**
```python
for epoch in range(100):
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()
```
> Explanation: this is the canonical five-step PyTorch training loop — clear old gradients, forward pass, compute loss, backpropagate, update weights — repeated once per epoch.

**Q: Write Keras code that adds dropout and early stopping to a simple classifier.**
```python
from tensorflow import keras

model = keras.Sequential([
    keras.layers.Input(shape=(n_features,)),
    keras.layers.Dense(64, activation="relu"),
    keras.layers.Dropout(0.3),
    keras.layers.Dense(n_classes, activation="softmax")
])
model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])

early_stop = keras.callbacks.EarlyStopping(monitor="val_loss", patience=10, restore_best_weights=True)
model.fit(X_train, y_train, epochs=200, validation_split=0.2, callbacks=[early_stop])
```
> Explanation: `Dropout(0.3)` randomly deactivates 30% of the preceding layer's neurons during training; `EarlyStopping` monitors validation loss and halts training once it stops improving for `patience` consecutive epochs, restoring the best-performing weights found along the way.

## Scenario Questions

**Q: You train a neural network and its training accuracy reaches 100% quickly, but test accuracy plateaus much lower and doesn't improve with more epochs. What would you try?**
> A: This is a clear overfitting signature (identical in spirit to Module 13c's unrestricted decision tree) — I'd add dropout layers to reduce the network's ability to memorize training data, consider reducing the network's size/capacity if it's very large relative to the dataset, and use early stopping with a validation split to stop training at the point where validation performance is actually best, rather than continuing to train on an already-overfit model.

**Q: A colleague asks whether they should use PyTorch or TensorFlow for a new project. How would you help them decide?**
> A: I'd ask about the team's existing codebase and expertise first — consistency with what the team already knows often matters more than either framework's individual merits. I'd also ask about the specific project: highly custom, research-style architectures or training procedures often favor PyTorch's explicitness; a fairly standard architecture where rapid iteration matters most might favor Keras' conciseness. Since the underlying concepts are identical, I'd note that skills transfer well between them regardless of which is chosen.

## "Gotcha" Questions

**Q: A model's loss is stuck at a high, unchanging value across many epochs and never decreases. What are the most likely causes?**
> A: The learning rate might be too high (causing the optimizer to overshoot and never settle) or too low (causing imperceptibly slow progress) — checking both extremes is a natural first step. Another common cause in PyTorch specifically is forgetting `optimizer.zero_grad()`, which causes gradients to accumulate incorrectly across steps rather than reflecting only the current batch. I'd also verify the labels and loss function match (e.g., using a classification loss with correctly-typed integer labels).

**Q: Why might a PyTorch model perform noticeably worse at evaluation time than its training-time metrics suggested, even without any train/test data leakage?**
> A: If the model uses dropout (or batch normalization) and the developer forgot to call `model.eval()` before evaluation, dropout would still be randomly deactivating neurons during "test" predictions — producing noisier, worse, and non-deterministic results compared to the fully-active network the training metrics implicitly benefited from during forward passes without dropout applied at those same points (dropout only applies in `model.train()` mode). Always call `model.eval()` before evaluating or predicting with a trained PyTorch model.

## Quick-Fire Rapid Review

- Q: What does an activation function add that a plain weighted sum can't? → **non-linearity**
- Q: Default activation function for hidden layers in modern networks? → **ReLU**
- Q: Algorithm that computes each weight's contribution to the error? → **backpropagation**
- Q: Algorithm that updates weights using those gradients? → **gradient descent**
- Q: One full pass through the training data is called a...? → **epoch**
- Q: Technique that randomly deactivates neurons during training? → **dropout**
- Q: Callback that halts training once validation performance stops improving? → **early stopping**
- Q: Must you call `model.eval()` before evaluating a PyTorch model? → **Yes**
