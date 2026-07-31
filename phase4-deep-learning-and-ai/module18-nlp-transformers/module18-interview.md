# 🎤 Module 18 Interview Prep: NLP & Transformers

## Conceptual Questions

### 🟢 Beginner

**Q: What is tokenization, and why does modern NLP use subword tokenization instead of whole-word tokenization?**
> A: Tokenization splits raw text into smaller units a model can process numerically. Whole-word tokenization requires a fixed vocabulary — any word not in that vocabulary becomes a generic "unknown" token, losing all information. Subword tokenization instead breaks rare or unseen words into familiar smaller pieces (e.g., "unbelievable" might stay whole, but a made-up word splits into recognizable fragments), so virtually any input text can be represented without ever hitting a true "unknown word" wall.

**Q: What is a word embedding, and why is it better than just using a token's raw ID number?**
> A: A raw token ID is just an arbitrary index into a vocabulary — the numbers themselves carry no meaning (token 500 isn't inherently "more related" to token 501 than to token 90000). An embedding is a dense, learned vector (often hundreds of dimensions) for each token, positioned so that semantically similar words end up with similar vectors — capturing actual meaning and relationships between words, not just an arbitrary index.

**Q: What problem does self-attention solve that older sequential models (RNNs) struggled with?**
> A: Sequential models process words strictly one at a time, so information from early words tends to fade by the time the model reaches later ones, making it hard to capture relationships between distant words (e.g., resolving what a pronoun refers to several words earlier). Self-attention lets every word directly consider every other word simultaneously, regardless of distance, solving this long-range dependency problem.

### 🟡 Intermediate

**Q: Explain Query, Key, and Value in the context of self-attention.**
> A: Query represents what a given word is "looking for" in other words; Key represents what each word "advertises" about itself, to be matched against queries; Value is the actual content a word contributes once it's deemed relevant. The dot product of Query and Key produces compatibility scores between word pairs, which get normalized via softmax into attention weights, and those weights determine how much of each word's Value gets blended into the final output for a given position.

**Q: What's the difference between an encoder-only model like BERT and a decoder-only model like GPT?**
> A: An encoder reads the entire input at once and builds a rich, bidirectional, context-aware understanding of it — well-suited to understanding/classification tasks (sentiment analysis, NER). A decoder generates output one token at a time, attending to both the encoder's output (if present) and to what it has already generated — well-suited to generation tasks (text completion, chat, translation). Many modern models specialize in just one half rather than using the full original encoder-decoder architecture.

**Q: What does `pipeline("zero-shot-classification")` do, and why is it remarkable?**
> A: It classifies text into categories the model was never specifically trained on, by comparing the input's meaning against candidate label names provided at request time, rather than requiring labeled training examples for each specific category. This works because the underlying model has learned such rich, general language understanding during its original large-scale pretraining that it can reason about novel categories on the fly — a strong illustration of how much "general knowledge" a pretrained Transformer actually captures.

## Practical/Coding Questions

**Q: Write code to load a tokenizer and model, and classify a sentence's sentiment without using `pipeline()`.**
```python
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

inputs = tokenizer("This movie was fantastic!", return_tensors="pt")
with torch.no_grad():
    logits = model(**inputs).logits
    predicted_class = torch.argmax(logits, dim=1).item()

print(model.config.id2label[predicted_class])
```
> Explanation: this is exactly what `pipeline("sentiment-analysis")` does internally — tokenize, run the model without gradient tracking (since we're only predicting, not training), then map the highest-scoring output back to a human-readable label.

**Q: Write a simplified NumPy implementation of self-attention scores for 3 words with 4-dimensional embeddings.**
```python
import numpy as np

def softmax(x):
    exp_x = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return exp_x / exp_x.sum(axis=-1, keepdims=True)

Q = embeddings @ Wq
K = embeddings @ Wk
V = embeddings @ Wv

scores = Q @ K.T / np.sqrt(K.shape[1])
attention_weights = softmax(scores)
output = attention_weights @ V
```
> Explanation: dividing by `sqrt(K.shape[1])` (the embedding dimension) is a standard scaling step that keeps the scores in a numerically stable range before the softmax; the final output blends every word's Value vector according to the computed attention weights.

## Scenario Questions

**Q: Your company needs to classify support tickets into 15 custom categories specific to your product, and you have no labeled historical data yet. What would you try first?**
> A: I'd start with `pipeline("zero-shot-classification")`, passing the 15 category names as candidate labels — this requires no labeled training data at all and could be usable in production immediately if accuracy is sufficient. I'd evaluate its accuracy on a small manually-labeled sample first; if it's not accurate enough, I'd use it to bootstrap an initial labeled dataset (having humans verify/correct its predictions) and then fine-tune a dedicated classifier once enough labeled data accumulates.

**Q: A teammate suggests training a Transformer model completely from scratch for a company-specific text classification task. What would you advise?**
> A: I'd strongly recommend starting with transfer learning instead — using a pretrained model (via `pipeline()` or fine-tuning a base model like `distilbert-base-uncased`) rather than training from scratch, exactly as Module 17c argued for images. Training a Transformer from scratch requires enormous amounts of text data and compute that virtually no individual company's dataset can match, and would almost certainly underperform a fine-tuned pretrained model trained on a fraction of that data.

## "Gotcha" Questions

**Q: A pipeline call that used to work (e.g., with a `grouped_entities=True` argument) suddenly raises a `TypeError` after a library upgrade. What's the most likely explanation?**
> A: Library APIs evolve, and pipeline arguments occasionally get renamed or deprecated between major versions — for example, the NER pipeline's `grouped_entities` argument was replaced by `aggregation_strategy="simple"` in more recent `transformers` versions. Always check the current library's documentation (or the error's suggested alternative) after an upgrade, rather than assuming older tutorial code will work unchanged indefinitely.

**Q: Why can a pretrained sentiment classifier confidently return "NEGATIVE" for a genuinely neutral or ambiguous sentence like "It's okay, does what it says but nothing special"?**
> A: Many sentiment models are trained as strictly binary classifiers (positive/negative only), with no "neutral" category available — the model must force even genuinely mixed or lukewarm sentiment into one of the two available buckets, sometimes with high confidence despite the input being genuinely ambiguous to a human reader. This is a useful reminder to check what categories a pretrained model actually supports before trusting its output uncritically on edge cases.

## Quick-Fire Rapid Review

- Q: What does the `##` prefix mean in subword tokenization output? → **this piece continues the previous token, not a new word**
- Q: What does an embedding capture that a raw token ID doesn't? → **semantic meaning/similarity between words**
- Q: What lets every word attend to every other word regardless of distance? → **self-attention**
- Q: What must every row of an attention weight matrix sum to? → **1 (via softmax)**
- Q: Encoder-only models are best suited for? → **understanding/classification tasks**
- Q: Decoder-only models are best suited for? → **generation tasks**
- Q: What Hugging Face function gives the fastest way to use a pretrained model? → **`pipeline()`**
- Q: What should you try before fine-tuning your own model? → **an existing pretrained model via `pipeline()`, or `zero-shot-classification`**
