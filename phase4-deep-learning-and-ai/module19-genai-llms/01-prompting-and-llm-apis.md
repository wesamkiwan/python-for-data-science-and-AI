# Module 19a: Prompting & Calling LLM APIs

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [Module 18 — NLP & Transformers](../module18-nlp-transformers/03-using-pretrained-transformers.md)

## 🎯 Learning Objectives
- [ ] Explain what a large language model (LLM) is and how it relates to Module 18's Transformers
- [ ] Apply core prompt engineering principles
- [ ] Call an LLM API from Python and handle its response
- [ ] Understand key API parameters: temperature, max tokens, system prompts

---

## ⚠️ A Note on This Lesson's Code

Every code example in this course so far was executed and its output verified. This lesson is a deliberate, transparent exception for one section: **calling a live LLM API requires an API key**, and none is configured in this authoring environment. The API-calling code below is written to match the current, stable SDK syntax precisely, but was **not executed live** — you'll need your own API key (from Anthropic, OpenAI, or another provider) to run it yourself. Everything else in this lesson (prompt engineering principles, parameter explanations) is standard, well-established knowledge, not dependent on a live call.

## Module Goal

Welcome to **Generative AI** — using large language models to generate text, answer questions, and reason about problems, rather than just classify or predict, as every previous module has done. This lesson covers the practical basics: writing effective prompts and calling an LLM via its API.

## Why This Matters on the Job

LLMs (ChatGPT, Claude, and their many relatives) have become a standard tool in the data scientist's toolkit — for generating synthetic training data, summarizing findings, powering chatbots, and (as you'll see in Module 19c) answering questions grounded in your own company's documents. Every one of these applications starts with the same two skills: writing a good prompt, and correctly calling the API.

---

## What Is a Large Language Model (LLM)?

An **LLM** is a very large **decoder-only Transformer** (Module 18b) — trained on enormous amounts of text to predict the next token in a sequence, over and over, at a massive scale. This deceptively simple training objective, applied to models with billions of parameters and trained on a huge fraction of publicly available text, produces models capable of writing coherent text, answering questions, reasoning through problems, and following complex instructions.

💡 **Tip:** Everything from Module 18 still applies — LLMs still tokenize input (Module 18a) and rely on self-attention (Module 18b) internally. What's new here is *scale* (far more parameters, far more training data) and how you interact with them: not by fine-tuning, but by **prompting** — giving instructions in plain natural language.

## Prompt Engineering: Writing Effective Instructions

**Prompt engineering** is the practice of crafting inputs (prompts) that reliably get the output you want from an LLM. A few core principles:

### 1. Be Specific and Explicit

```
❌ Vague:    "Summarize this."
✅ Specific: "Summarize this article in exactly 3 bullet points, each under 15 words,
              focusing on the financial impact discussed."
```

### 2. Provide Context and Examples (Few-Shot Prompting)

```
Classify the sentiment of each review as Positive, Negative, or Neutral.

Review: "This product changed my life!"
Sentiment: Positive

Review: "Broke after one day, total waste of money."
Sentiment: Negative

Review: "It's fine, does what it says."
Sentiment:
```

**How it works:** Providing a few labeled examples (**few-shot prompting**) before the actual task teaches the model your exact desired output format and reasoning pattern, often dramatically improving reliability compared to just describing the task in words (**zero-shot prompting** — no examples at all, similar in spirit to Module 18c's `zero-shot-classification`, but here achieved through the prompt itself rather than a specialized model).

### 3. Ask for Step-by-Step Reasoning (Chain-of-Thought)

```
❌ "What is 17% of 240, minus 12?"
✅ "What is 17% of 240, minus 12? Think through this step by step before giving
    your final answer."
```

**How it works:** Explicitly asking a model to reason through steps before answering (**chain-of-thought prompting**) frequently improves accuracy on tasks requiring multi-step logic or arithmetic, since it gives the model "space" to work through intermediate steps rather than jumping straight to a final answer.

### 4. Specify the Output Format

```
"Extract the person's name, company, and role from this text. Respond ONLY with
valid JSON in this exact format: {"name": "...", "company": "...", "role": "..."}"
```

✅ **Best Practice:** When you need output your code will parse programmatically (as in Module 19c's RAG pipeline), always explicitly request a specific format (JSON, a numbered list, etc.) — this makes the response far more reliable to parse than free-form prose.

## Calling an LLM API

Every major LLM provider offers a Python SDK with broadly similar patterns. Here's the Anthropic API (Claude):

```bash
pip install anthropic
```

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key-here")   # or set the ANTHROPIC_API_KEY env var

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    system="You are a helpful assistant that explains concepts clearly and concisely.",
    messages=[
        {"role": "user", "content": "Explain what a p-value is in one paragraph."}
    ]
)

print(response.content[0].text)
```

**How it works:** `client.messages.create()` sends your prompt to the model and returns its response. The `system` parameter sets overall behavior/persona for the entire conversation (distinct from the `user` message, which is the specific request). `max_tokens` caps how long the response can be — note that both your prompt *and* the model's response consume tokens (Module 18a's subword units), and API pricing is typically based on token counts.

⚠️ **Security Warning:** Never hard-code an API key directly in your source code, especially if it might be committed to git (Module 05b) or shared. Always load it from an environment variable or a secrets manager instead:

```python
import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
```

## Key API Parameters

| Parameter | Controls | Typical range |
|---|---|---|
| `temperature` | Randomness/creativity of output. `0` = deterministic, always picks the most likely next token; higher = more varied/creative | `0.0`-`1.0` |
| `max_tokens` | Maximum length of the response | Depends on task — short answers: 100s; long documents: 1000s+ |
| `system` | Overall behavior/persona instructions, separate from the specific request | A clear, concise role description |

```python
# Lower temperature for factual/deterministic tasks (e.g., data extraction)
response = client.messages.create(
    model="claude-sonnet-4-5", max_tokens=500, temperature=0.0,
    messages=[{"role": "user", "content": "Extract the total price from: 'Order #123, 3 items, $45.99 total'"}]
)

# Higher temperature for creative tasks
response = client.messages.create(
    model="claude-sonnet-4-5", max_tokens=500, temperature=0.9,
    messages=[{"role": "user", "content": "Write a short, creative product tagline for a coffee brand."}]
)
```

💡 **Tip:** For any task where you need consistent, reproducible output (data extraction, classification, structured parsing), use a low or zero temperature. Reserve higher temperatures for genuinely creative tasks (brainstorming, varied writing) where some randomness is desirable.

## Handling Errors and Rate Limits

Exactly like Module 04's `requests` lesson, real API calls need error handling:

```python
import anthropic

client = anthropic.Anthropic()

try:
    response = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=500,
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.content[0].text)
except anthropic.RateLimitError:
    print("Rate limit hit -- wait and retry.")
except anthropic.APIError as e:
    print(f"API error: {e}")
```

**How it works:** This mirrors Module 04c's `try`/`except` pattern for `requests` exactly — `RateLimitError` and `APIError` are specific exception types the SDK raises, letting you handle known failure modes (too many requests, a server-side issue) distinctly rather than letting your program crash.

---

## Hands-On Exercise

**Task:** Write `prompting_practice.py` that (you'll need your own API key to actually run this):
1. Writes a zero-shot prompt asking the model to classify 3 product reviews as Positive/Negative/Neutral.
2. Rewrites the same task as a few-shot prompt with 2 example classifications provided first, and explains in a comment why this might improve reliability.
3. Writes a prompt requesting the model extract structured data (name, date, amount) from a sample invoice-like text, explicitly requesting JSON output.
4. Wraps all API calls in `try`/`except` blocks handling `RateLimitError` and `APIError`.

<details>
<summary>✅ Click to see the solution (requires your own API key to run)</summary>

```python
import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def ask(prompt, temperature=0.0):
    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=500,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except anthropic.RateLimitError:
        return "Rate limit hit -- wait and retry."
    except anthropic.APIError as e:
        return f"API error: {e}"

zero_shot_prompt = """Classify each review as Positive, Negative, or Neutral:
1. "Fast shipping and great quality!"
2. "Never arrived, terrible service."
3. "It's an average product, nothing special."
"""
print(ask(zero_shot_prompt))

few_shot_prompt = """Classify the sentiment of each review as Positive, Negative, or Neutral.

Review: "This product changed my life!"
Sentiment: Positive

Review: "Broke after one day, total waste of money."
Sentiment: Negative

Review: "Fast shipping and great quality!"
Sentiment:"""
print(ask(few_shot_prompt))
# Few-shot prompting shows the model the exact desired label format and
# reasoning pattern via examples, which typically improves consistency
# compared to describing the task in words alone.

extraction_prompt = """Extract the customer name, invoice date, and total amount from
this text. Respond ONLY with valid JSON: {"name": "...", "date": "...", "amount": "..."}

Text: "Invoice for Jane Doe, dated 2026-03-15, total due: $245.00"
"""
print(ask(extraction_prompt))
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Vague, underspecified prompts | Be explicit about format, length, and focus |
| Hard-coding an API key in source code | Load from an environment variable or secrets manager |
| Using a high temperature for tasks needing consistent output | Use `temperature=0` for factual/structured/reproducible tasks |
| Not handling API errors | Wrap calls in `try`/`except`, exactly like Module 04's `requests` pattern |
| Assuming zero-shot always works well | Try few-shot examples or chain-of-thought prompting if results are unreliable |

---

## ✅ Module Completion Checklist (Part A)
- [ ] Understand what an LLM is and its relationship to Module 18's Transformers
- [ ] Can apply zero-shot, few-shot, and chain-of-thought prompting techniques
- [ ] Can call an LLM API and handle its response (with your own API key)
- [ ] Understand `temperature`, `max_tokens`, and `system` prompts
- [ ] Reviewed the `prompting_practice.py` exercise (run it if you have an API key)

**Next:** Continue to [`02-embeddings-and-semantic-search.md`](02-embeddings-and-semantic-search.md)
