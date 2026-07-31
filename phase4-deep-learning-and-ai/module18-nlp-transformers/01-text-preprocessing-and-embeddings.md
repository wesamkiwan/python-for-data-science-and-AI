# Module 18a: Text Preprocessing & Embeddings

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [Module 17 — Computer Vision (CNNs)](../module17-computer-vision/03-transfer-learning-and-augmentation.md)

## 🎯 Learning Objectives
- [ ] Explain why text must be converted to numbers before a model can use it
- [ ] Understand tokenization, including modern subword tokenization
- [ ] Explain word embeddings and why they capture meaning better than simple encoding
- [ ] Use a real tokenizer from the Hugging Face `transformers` library

---

## Module Goal

Begin **NLP (Natural Language Processing)** — deep learning applied to text — by learning how raw text gets converted into the numeric form every neural network requires. This mirrors Module 17's "prepare the input" lessons, just for text instead of images.

## Why This Matters on the Job

Every NLP task — sentiment analysis, chatbots, search, summarization, and the LLMs you'll use in Module 19 — starts with the same foundational step: converting text into numbers a model can process. Understanding tokenization and embeddings deeply is what lets you debug why a model handles certain inputs oddly (unusual words, typos, different languages) and understand the real cost/context-length tradeoffs when working with any modern language model.

---

## Why Text Needs Special Handling

Recall Module 06-17: every model you've built expects numeric input (`X`) — NumPy arrays or tensors of numbers. Text is fundamentally different: it's a sequence of discrete symbols (characters, words) of *varying length*, with meaning that depends heavily on order and context (`"dog bites man"` vs. `"man bites dog"`). NLP is the set of techniques for bridging this gap.

## Installing the Hugging Face `transformers` Library

```bash
pip install transformers
```

**Hugging Face** is the central hub and library ecosystem for modern NLP — providing pretrained models, tokenizers, and datasets that have become the de facto standard tooling for the field, much like scikit-learn is for classical ML.

## Tokenization: Splitting Text into Pieces

**Tokenization** splits raw text into smaller units (**tokens**) — historically whole words, but modern NLP almost universally uses **subword tokenization** instead.

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

text = "Tokenization splits text into pieces a model can understand."
tokens = tokenizer.tokenize(text)
print(tokens)
```
```
['token', '##ization', 'splits', 'text', 'into', 'pieces', 'a', 'model', 'can', 'understand', '.']
```

**How it works:** Notice `"Tokenization"` split into `'token'` + `'##ization'` — the `##` prefix marks a piece that continues the previous token rather than starting a new word. This is **subword tokenization**: instead of one token per whole word, common word *pieces* form the vocabulary, letting the tokenizer represent virtually any word — even ones it's never seen — by breaking it into familiar sub-parts.

```python
print(tokenizer.tokenize("unbelievable"))
print(tokenizer.tokenize("supercalifragilisticexpialidocious"))
```
```
['unbelievable']
['super', '##cal', '##if', '##rag', '##ilis', '##tic', '##ex', '##pia', '##lid', '##oc', '##ious']
```

**How it works:** `"unbelievable"` is common enough to exist as its own single token, but the much rarer, invented-sounding word gets broken into many familiar smaller pieces. This is precisely why modern language models can meaningfully process typos, made-up words, and even other languages to some degree — they never need a literal, exact match for every possible word, just familiar enough sub-pieces.

⚠️ **Warning:** Older NLP approaches used simple **whole-word tokenization** with a fixed vocabulary — any word not in that vocabulary became a generic `"unknown"` token, losing all information about it. Subword tokenization (used by essentially every modern model, including every LLM in Module 19) solves this "out of vocabulary" problem elegantly.

## Converting Tokens to Numbers: Token IDs

```python
encoded = tokenizer(text)
print(encoded["input_ids"])
```
```
[101, 19204, 3989, 19584, 3793, 2046, 4109, 1037, 2944, 2064, 3305, 1012, 102]
```

**How it works:** Each token maps to a unique integer ID from the tokenizer's fixed vocabulary (this specific model's vocabulary has around 30,000 entries). `101` and `102` are special tokens marking the start (`[CLS]`) and end (`[SEP]`) of the input — required by this particular model's architecture. You can reverse the process to confirm nothing was lost:

```python
print(tokenizer.decode(encoded["input_ids"]))
```
```
[CLS] tokenization splits text into pieces a model can understand. [SEP]
```

## Embeddings: Numbers That Capture Meaning

Token IDs alone (`19204`, `3989`, ...) are just arbitrary index numbers — they don't encode any relationship between words. `"cat"` (id 4937, say) and `"kitten"` (some unrelated id) look no more related than `"cat"` and `"airplane"` just by their raw ID numbers. **Word embeddings** solve this: each token ID maps to a dense vector of numbers (typically hundreds of dimensions), *learned* so that semantically similar words end up with similar vectors.

💡 **Analogy:** Imagine plotting every word as a point in space, where words with similar meanings cluster near each other — `"cat"` and `"kitten"` would be close together, `"cat"` and `"dog"` somewhat close (both animals), and `"cat"` and `"airplane"` far apart. An embedding is exactly this: a learned coordinate for each word, positioned so that geometric closeness reflects semantic closeness.

```python
import torch
from transformers import AutoModel

model = AutoModel.from_pretrained("distilbert-base-uncased")

with torch.no_grad():
    inputs = tokenizer("cat", return_tensors="pt")
    outputs = model(**inputs)
    embedding = outputs.last_hidden_state
    print(embedding.shape)   # (1, 3, 768) -- 1 sentence, 3 tokens ([CLS] cat [SEP]), 768-dim embedding each
```

**How it works:** `768` is this specific model's **embedding dimension** — every token gets represented as a 768-number vector, learned during the model's original pretraining on massive amounts of text, such that words appearing in similar contexts end up with similar vectors (this idea — "a word is characterized by the company it keeps" — is the founding insight behind essentially all modern NLP). Unlike Module 17's images (where you *see* the input directly), embeddings are the crucial, invisible translation step that turns discrete symbols into the continuous, meaningful numeric representations every neural network actually operates on.

🎯 **On the job:** You'll rarely compute raw embeddings by hand — pretrained models (this lesson) and pretrained tokenizers already encapsulate this. Understanding that this translation step exists, and why it captures *meaning* rather than arbitrary IDs, is what makes everything in the next two lessons (attention, and using pretrained models for real tasks) click.

---

## Hands-On Exercise

**Task:** Write `tokenization_practice.py` that:
1. Loads the `distilbert-base-uncased` tokenizer.
2. Tokenizes 3 sentences of your choice, at least one containing an unusual or made-up word, and prints the resulting tokens for each.
3. Encodes one of the sentences into `input_ids`, prints them, then decodes them back to confirm the round trip is lossless.
4. Loads the `distilbert-base-uncased` model and computes the embedding shape for one of your sentences, printing the shape and explaining in a comment what each dimension represents.

<details>
<summary>✅ Click to see the solution</summary>

```python
import torch
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")

sentences = [
    "The quick brown fox jumps over the lazy dog.",
    "Deep learning models require lots of preprocessing.",
    "Antidisestablishmentarianism is a famously long word."
]

for sentence in sentences:
    print(tokenizer.tokenize(sentence))

encoded = tokenizer(sentences[0])
print(encoded["input_ids"])
print(tokenizer.decode(encoded["input_ids"]))

with torch.no_grad():
    inputs = tokenizer(sentences[0], return_tensors="pt")
    outputs = model(**inputs)
    embedding = outputs.last_hidden_state
    print(embedding.shape)
    # Dimension 1: batch size (1 sentence)
    # Dimension 2: number of tokens (including [CLS]/[SEP])
    # Dimension 3: embedding dimension (768 for this model) -- one meaning-carrying
    # vector per token
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Assuming tokenization always splits on whole words | Modern subword tokenization can split within a word (`##`-prefixed pieces) |
| Treating token IDs as meaningful numbers directly | They're arbitrary vocabulary indices — embeddings are what capture meaning |
| Forgetting different models use different tokenizers/vocabularies | Always use the tokenizer that matches the specific pretrained model you're using |
| Manually building embeddings from scratch for common tasks | Use a pretrained model's embeddings (next lessons) — they already capture rich, learned meaning |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand why text must be converted to numbers before modeling
- [ ] Can explain subword tokenization and why it solves the "unknown word" problem
- [ ] Understand what a word embedding is and why it captures meaning
- [ ] Can use a Hugging Face tokenizer and pretrained model to inspect tokens and embeddings
- [ ] Completed the `tokenization_practice.py` exercise

**Next:** Continue to [`02-transformer-architecture.md`](02-transformer-architecture.md)
