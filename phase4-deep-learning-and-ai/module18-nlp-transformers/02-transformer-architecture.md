# Module 18b: The Transformer Architecture & Attention

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [01-text-preprocessing-and-embeddings.md](01-text-preprocessing-and-embeddings.md)

## 🎯 Learning Objectives
- [ ] Explain the limitation of processing text word-by-word in strict sequence
- [ ] Explain the self-attention mechanism conceptually and mathematically
- [ ] Manually compute a simplified attention calculation
- [ ] Understand the encoder/decoder structure at a high level

---

## Module Goal

Learn the **Transformer** architecture — the innovation behind essentially every modern NLP breakthrough since 2017, including every LLM you'll use in Module 19 (GPT, and its many relatives). At its heart is a single, powerful idea: **attention**.

## Why This Matters on the Job

Every major language model you'll interact with professionally — ChatGPT, Claude, and virtually every other modern LLM — is built on the Transformer architecture. Understanding attention conceptually, even without deriving every equation, is what lets you reason about *why* these models handle long-range context well, why longer inputs cost more to process, and what's actually happening when you hear terms like "context window" or "attention heads."

---

## The Problem: Understanding Context and Relationships

Consider: `"The animal didn't cross the street because it was too tired."` — what does `"it"` refer to? A human immediately understands `"it"` = `"the animal"` (not `"the street"`), by relating that word back to earlier context. Older NLP architectures (RNNs — Recurrent Neural Networks, processing words strictly one at a time in sequence) struggled to maintain this kind of long-range relationship, especially across long sentences or documents — information from early words tended to fade by the time the model reached later ones.

## Self-Attention: Letting Every Word "Look At" Every Other Word

**Self-attention** lets each word in a sequence directly consider every *other* word when building its own representation — rather than processing strictly in order, every word can immediately "attend to" any other word, regardless of distance.

### A Simplified, Manual Attention Calculation

```python
import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / exp_x.sum(axis=-1, keepdims=True)

# 3 words, each represented by a small 4-dimensional embedding (Module 18a's concept, tiny scale)
np.random.seed(42)
embeddings = np.random.randn(3, 4)   # representing, say, "The", "cat", "sat"

# Learned weight matrices that transform embeddings into Query, Key, and Value vectors
Wq = np.random.randn(4, 4) * 0.5
Wk = np.random.randn(4, 4) * 0.5
Wv = np.random.randn(4, 4) * 0.5

Q = embeddings @ Wq   # "what am I looking for?"
K = embeddings @ Wk      # "what do I contain?"
V = embeddings @ Wv         # "what information do I actually offer?"

# Attention scores: how relevant is every word to every other word?
scores = Q @ K.T / np.sqrt(K.shape[1])
attention_weights = softmax(scores)   # normalize each row into a probability distribution
print(attention_weights)
print(attention_weights.sum(axis=1))   # each row sums to 1.0

output = attention_weights @ V   # blend each word's Value vectors, weighted by attention
print(output.shape)   # (3, 4) -- one context-aware output vector per input word
```
```
[[0.33238543 0.5416463  0.12596827]
 [0.30523121 0.36157763 0.33319116]
 [0.27500906 0.19974517 0.52524577]]
[1. 1. 1.]
(3, 4)
```

**How it works, conceptually:**
- **Query (Q):** what this word is "looking for" from other words.
- **Key (K):** what each word "advertises" about itself, to be matched against queries.
- **Value (V):** the actual information a word contributes once it's deemed relevant.
- `Q @ K.T` computes a **compatibility score** between every pair of words — how relevant is word *j* to word *i*'s query.
- `softmax` turns these raw scores into **attention weights** — a probability distribution over all words (each row sums to `1.0`), representing "how much should word *i* attend to each other word."
- The final output for each word is a weighted blend of every word's Value vector, weighted by how much attention that word receives — words highly relevant to a given position contribute more to its final representation.

💡 **Analogy:** Think of it like a classroom discussion where, for every statement someone makes, they briefly "check in" with everyone else in the room to see who has the most relevant thing to say on that topic, then blend those relevant contributions together — rather than only ever listening to the person who spoke immediately before them (as strict sequential processing would).

🎯 **On the job:** This is precisely the mechanism (scaled up enormously — real models use hundreds of dimensions, many parallel "attention heads," and many stacked layers) behind how a model resolves that `"it"` = `"the animal"` example — attention lets the word `"it"` directly attend back to `"animal"`, regardless of how many words separate them.

## Multi-Head Attention: Multiple Perspectives at Once

Real Transformers don't compute attention just once — they run several attention computations in parallel (**attention heads**), each potentially learning to focus on different kinds of relationships (one head might track grammatical subject/verb agreement, another might track topical relevance, etc.), then combine all their outputs together.

## The Transformer's Encoder/Decoder Structure

The original Transformer architecture has two main components:

| Component | Role | Used for |
|---|---|---|
| **Encoder** | Reads the entire input and builds a rich, context-aware representation of it | Understanding tasks — classification, extracting meaning (Module 18c, and the sentiment analysis model from Module 18a) |
| **Decoder** | Generates output one token at a time, attending both to the encoder's output and to what it's already generated | Generation tasks — translation, text completion, chat responses |

💡 **Tip:** Modern models often specialize in just one half: **encoder-only** models (like BERT, used in Module 18c) excel at understanding/classification tasks; **decoder-only** models (like GPT, the foundation of Module 19's LLMs) excel at text generation. Some models (like the original Transformer, designed for translation) use both halves together.

⚠️ **Warning:** Every word attending to every other word means computation scales roughly with the *square* of the input length — this is precisely why longer inputs to an LLM (Module 19) cost more and take longer to process, and why "context window" (the maximum input length a model can handle) is such a frequently discussed practical limitation.

---

## Hands-On Exercise

**Task:** Write `attention_practice.py` that:
1. Creates 4 toy word embeddings (any reasonable random 6-dimensional vectors, using `np.random.seed()` for reproducibility).
2. Defines random `Wq`, `Wk`, `Wv` weight matrices and computes `Q`, `K`, `V`.
3. Computes the attention scores, applies softmax, and prints the resulting attention weight matrix.
4. Confirms each row sums to 1.0 (print the row sums).
5. Identifies (by inspecting the printed weights) which word each of the other words "attends to" most strongly, and prints a sentence describing this for at least one word.

<details>
<summary>✅ Click to see the solution</summary>

```python
import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / exp_x.sum(axis=-1, keepdims=True)

np.random.seed(7)
embeddings = np.random.randn(4, 6)   # 4 toy words, 6-dim embeddings

Wq = np.random.randn(6, 6) * 0.5
Wk = np.random.randn(6, 6) * 0.5
Wv = np.random.randn(6, 6) * 0.5

Q = embeddings @ Wq
K = embeddings @ Wk
V = embeddings @ Wv

scores = Q @ K.T / np.sqrt(K.shape[1])
attention_weights = softmax(scores)

print(attention_weights)
print(f"Row sums: {attention_weights.sum(axis=1)}")

output = attention_weights @ V
print(f"Output shape: {output.shape}")

most_attended = attention_weights[0].argmax()
print(f"Word 0 attends most strongly to word {most_attended} "
      f"(weight: {attention_weights[0][most_attended]:.4f})")
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Assuming attention processes words strictly in order | Every word can attend to every other word simultaneously, regardless of position |
| Forgetting attention weights must sum to 1 per row | The `softmax` step guarantees this — verify it as a sanity check |
| Assuming a Transformer always has both encoder and decoder | Many modern models are encoder-only (BERT-style) or decoder-only (GPT-style) |
| Ignoring the quadratic cost of longer sequences | Be aware that input length directly and non-linearly impacts compute cost |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Understand the limitation self-attention was designed to solve
- [ ] Can explain Query/Key/Value and manually compute a simplified attention calculation
- [ ] Understand multi-head attention at a conceptual level
- [ ] Understand the encoder/decoder distinction and which tasks favor each
- [ ] Completed the `attention_practice.py` exercise

**Next:** Continue to [`03-using-pretrained-transformers.md`](03-using-pretrained-transformers.md)
