# 📋 Module 18 Cheat Sheet: NLP & Transformers

Fast reference for tokenization, attention, and using pretrained Transformers.

## Tokenization
```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")

tokenizer.tokenize(text)          # -> list of tokens/subwords (## prefix = word continuation)
encoded = tokenizer(text)             # -> dict with input_ids, attention_mask, etc.
tokenizer.decode(encoded["input_ids"])   # -> back to text (lossless round trip)
```
💡 Subword tokenization handles any word (even unseen/made-up ones) by splitting into familiar pieces.

## Embeddings
```python
from transformers import AutoModel
import torch

model = AutoModel.from_pretrained("distilbert-base-uncased")
inputs = tokenizer(text, return_tensors="pt")
with torch.no_grad():
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state   # shape: (batch, num_tokens, embedding_dim)
```
Embeddings are dense vectors where semantically similar words end up close together.

## Self-Attention (conceptual)
```python
Q = embeddings @ Wq   # "what am I looking for?"
K = embeddings @ Wk      # "what do I contain?"
V = embeddings @ Wv         # "what do I actually offer?"

scores = Q @ K.T / sqrt(dim)
attention_weights = softmax(scores)   # each row sums to 1
output = attention_weights @ V           # context-aware blend of all words' Values
```
Every word attends to every other word directly — no strict sequential processing.

| Concept | Role |
|---|---|
| Query (Q) | What this word is looking for |
| Key (K) | What each word advertises |
| Value (V) | The actual info contributed |
| Multi-head attention | Several attention computations in parallel, different learned "perspectives" |
| Encoder | Reads input, builds understanding (classification tasks — BERT-style) |
| Decoder | Generates output token-by-token (generation tasks — GPT-style) |

## Using Pretrained Transformers (`pipeline()`)
```python
from transformers import pipeline

pipeline("sentiment-analysis")(text)
pipeline("zero-shot-classification")(text, candidate_labels=[...])
pipeline("ner", aggregation_strategy="simple")(text)
```
This is "transfer learning for text" — reusing a model already (fine-)tuned, exactly like Module 17c's image transfer learning.

## Under the Hood (what `pipeline()` does)
```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

inputs = tokenizer(text, return_tensors="pt")
with torch.no_grad():
    logits = model(**inputs).logits
    predicted_class = torch.argmax(logits, dim=1).item()
label = model.config.id2label[predicted_class]
```

## Fine-Tuning (when pipeline() isn't enough)
```python
model = AutoModelForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=N)
# then use Hugging Face's Trainer API with your own labeled dataset
```
Decision order: 1) try `pipeline()` with an existing model → 2) try `zero-shot-classification` → 3) fine-tune only if neither works well enough.

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| `KeyError: Unknown task` on `pipeline("...")` | Task name not supported in your installed transformers version | Check `PIPELINE_REGISTRY` / library version; task names change between major versions |
| `TypeError` on a pipeline kwarg like `grouped_entities` | Deprecated/renamed parameter | Check current docs — e.g., NER now uses `aggregation_strategy="simple"` |
| Tokenizer/model mismatch errors | Using a tokenizer from a different model than the one loaded | Always load both from the exact same `model_name` |
| Slow first run | Model weights downloading | Expected on first use — cached locally afterward |
| Attention weight rows don't sum to 1 | Missing or incorrect softmax | `softmax` must be applied across the correct axis (each row = one word's distribution) |

## The "New NLP Task" Workflow
1. Check if `pipeline("task-name")` with an existing model already solves it.
2. If categories are unusual but you lack labeled data, try `zero-shot-classification`.
3. Only fine-tune a pretrained model on your own labeled data as a last resort.
4. Always match tokenizer and model to the same `model_name`.
