# Module 18c: Using Pretrained Transformers with Hugging Face

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [02-transformer-architecture.md](02-transformer-architecture.md)

## 🎯 Learning Objectives
- [ ] Use Hugging Face `pipeline()` for common NLP tasks
- [ ] Perform sentiment analysis, text classification, and named entity recognition with pretrained models
- [ ] Recognize this as "transfer learning for text" and connect it to Module 17c
- [ ] Understand at a high level what fine-tuning a pretrained transformer involves

---

## Module Goal

Put Module 18a/18b's concepts to work using **real, powerful pretrained Transformer models** via the Hugging Face `transformers` library — accomplishing genuinely useful NLP tasks in just a few lines of code, without training anything from scratch.

## Why This Matters on the Job

Just as Module 17c showed that training a CNN from scratch rarely makes sense, training a Transformer from scratch is almost never practical — these models are pretrained on enormous amounts of text (far beyond what any single company could realistically gather) and then adapted to specific tasks. Hugging Face's `pipeline()` API has become the standard, fastest way to get a real NLP task working, and is frequently the very first tool reached for in a real project before considering anything more custom.

---

## `pipeline()`: The Fastest Way to Use a Pretrained Model

```python
from transformers import pipeline

classifier = pipeline("sentiment-analysis")

results = classifier([
    "I love this product, it works great!",
    "This was a terrible experience, I want a refund."
])
for result in results:
    print(result)
```
```
{'label': 'POSITIVE', 'score': 0.9998767375946045}
{'label': 'NEGATIVE', 'score': 0.9993147850036621}
```

**How it works:** `pipeline("sentiment-analysis")` downloads a pretrained model (already fine-tuned specifically for sentiment classification — by default, `distilbert-base-uncased-finetuned-sst-2-english`), automatically handling tokenization (Module 18a), running the model, and converting the raw output into a readable label and confidence score — all in one function call. This is precisely the same **transfer learning** idea from Module 17c, just applied to text: reuse a model already trained (and here, even already fine-tuned) for the exact task, rather than starting from nothing.

## Other Common NLP Tasks via `pipeline()`

```python
# Text classification with custom labels (zero-shot -- no task-specific training needed at all!)
classifier = pipeline("zero-shot-classification")
result = classifier(
    "This laptop has amazing battery life but a mediocre screen.",
    candidate_labels=["technology", "sports", "politics", "review"]
)
print(result["labels"][0], result["scores"][0])

# Named Entity Recognition (NER) -- identifying people, places, organizations in text
ner = pipeline("ner", aggregation_strategy="simple")
entities = ner("Marie Curie won the Nobel Prize while working in Paris.")
for entity in entities:
    print(entity["word"], entity["entity_group"], f"{entity['score']:.4f}")
```

💡 **Tip:** These three tasks (sentiment analysis, zero-shot classification, NER) are all *understanding* tasks — the model reads text and outputs a label, score, or classification, but doesn't generate new text. Generation tasks (summarization, translation, open-ended text completion, chat) rely on the same Transformer foundation but are worth a dedicated, deeper look — that's exactly what Module 19 (Generative AI & LLMs) covers next, including how modern LLMs like GPT extend this same pretrained-model-via-pipeline idea into full text generation.

💡 **Tip:** `pipeline("zero-shot-classification")` is a particularly striking example of a model's generalized understanding — it can classify text into categories it was *never specifically trained on*, just by comparing the input's meaning against the candidate label names you provide at request time. This works because the underlying model has learned such rich, general language understanding during pretraining that it can reason about novel categories on the fly.

## Under the Hood: What `pipeline()` Is Actually Doing

```python
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

model_name = "distilbert-base-uncased-finetuned-sst-2-english"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

inputs = tokenizer("I love this product!", return_tensors="pt")

with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=1).item()

print(model.config.id2label[predicted_class])   # 'POSITIVE'
```

**How it works:** This is exactly Module 16b's `.eval()` + `torch.no_grad()` + `torch.max()`-style evaluation pattern, applied to a pretrained Transformer instead of a network you trained yourself. `pipeline()` is simply a convenient wrapper around this exact sequence of steps — tokenize, run the model, interpret the output — which is worth understanding once, so `pipeline()`'s convenience doesn't feel like unexplainable magic.

## Fine-Tuning: Adapting a Pretrained Transformer to Your Own Task

When `pipeline()`'s existing pretrained models don't fit your specific task (e.g., classifying support tickets into your company's specific categories), you can **fine-tune** a pretrained model on your own labeled data — directly analogous to Module 17c's transfer learning for images.

```python
# Conceptual sketch -- fine-tuning typically uses Hugging Face's Trainer API:
from transformers import AutoModelForSequenceClassification, TrainingArguments, Trainer

model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased", num_labels=3   # e.g., 3 custom categories
)

# training_args = TrainingArguments(output_dir="./results", num_train_epochs=3, ...)
# trainer = Trainer(model=model, args=training_args, train_dataset=your_dataset, ...)
# trainer.train()
```

**How it works:** Loading `distilbert-base-uncased` (the *base* model, not a task-specific fine-tuned version) with `num_labels=3` attaches a fresh, randomly-initialized classification head sized for your specific number of categories — exactly like Module 17c's `model.fc = nn.Linear(num_features, num_classes)` for images. Hugging Face's `Trainer` API then handles the training loop (Module 16b's `zero_grad`/forward/loss/`backward`/`step` pattern) for you, fine-tuning on your own labeled examples.

⚠️ **Warning:** Fine-tuning requires labeled training data specific to your task and meaningfully more setup than `pipeline()` — always check first whether an existing pretrained/fine-tuned model or `zero-shot-classification` already solves your problem well enough before investing in custom fine-tuning.

🎯 **On the job:** The decision tree is usually: (1) try `pipeline()` with an existing fine-tuned model first, (2) try `zero-shot-classification` if your categories are unusual but you have no labeled data, (3) only fine-tune your own model if neither gets you close enough and you have labeled data available — in that order, roughly by increasing effort.

---

## Hands-On Exercise

**Task:** Write `nlp_pipeline_practice.py` that:
1. Uses `pipeline("sentiment-analysis")` to classify 4 sentences of your own choosing (mix of clearly positive, clearly negative, and at least one ambiguous/mixed one) and prints each result.
2. Uses `pipeline("zero-shot-classification")` to classify one sentence against 4 candidate labels of your choice, printing the top predicted label and its score.
3. Uses `pipeline("ner", aggregation_strategy="simple")` on a sentence containing at least one person's name, one place, and one organization, printing each detected entity and its type.
4. Writes a short comment explaining, in your own words, why this whole exercise is a form of "transfer learning for text," referencing Module 17c.

<details>
<summary>✅ Click to see the solution</summary>

```python
from transformers import pipeline

sentiment_classifier = pipeline("sentiment-analysis")
sentences = [
    "This is the best purchase I've made all year!",
    "Absolutely awful, do not buy this.",
    "It's okay, does what it says but nothing special.",
    "I'm not sure how I feel about this yet."
]
for sentence in sentences:
    result = sentiment_classifier(sentence)[0]
    print(f"{sentence} -> {result['label']} ({result['score']:.4f})")

zero_shot = pipeline("zero-shot-classification")
result = zero_shot(
    "The new quarterly earnings report exceeded analyst expectations.",
    candidate_labels=["finance", "sports", "entertainment", "weather"]
)
print(f"Top label: {result['labels'][0]} ({result['scores'][0]:.4f})")

ner = pipeline("ner", aggregation_strategy="simple")
entities = ner("Barack Obama worked with the United Nations in New York.")
for entity in entities:
    print(f"{entity['word']}: {entity['entity_group']} ({entity['score']:.4f})")

# This entire exercise is "transfer learning for text": every pipeline() call
# reuses a model already pretrained (and often already fine-tuned) on massive
# text datasets, exactly like Module 17c's ResNet/MobileNetV2 reused features
# learned from ImageNet -- we never trained anything from scratch, just
# applied existing, general language understanding to our specific sentences.
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Fine-tuning a model from scratch before trying `pipeline()` | Check if an existing pretrained/fine-tuned model already solves your task |
| Assuming `zero-shot-classification` is as accurate as a fine-tuned model | It's remarkably capable but generally less accurate than a model fine-tuned specifically for your task/labels |
| Not specifying a model version in production | Pin an explicit model name/revision rather than relying on `pipeline()`'s default, which can change over time |
| Confusing `pipeline()`'s convenience with "no model actually running" | It's still running a full Transformer forward pass — same computational cost as doing it manually |

---

## ✅ Module 18 Completion Checklist
- [ ] Can use `pipeline()` for sentiment analysis, zero-shot classification, and NER
- [ ] Understand what `pipeline()` does internally (tokenize → model → interpret output)
- [ ] Recognize using pretrained Transformers as "transfer learning for text"
- [ ] Understand at a high level what fine-tuning involves and when it's warranted
- [ ] Completed the `nlp_pipeline_practice.py` exercise
- [ ] Reviewed [`module18-cheatsheet.md`](module18-cheatsheet.md)
- [ ] Reviewed [`module18-interview.md`](module18-interview.md)
- [ ] Browsed [`module18-references.md`](module18-references.md)

**Next Step:** Module 19 — Generative AI & LLMs (`phase4-deep-learning-and-ai/module19-genai-llms/`)
