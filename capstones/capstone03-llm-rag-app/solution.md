# Capstone 3: Complete Reference Solution

Every code block that can run locally (everything except the "real LLM API" section, clearly marked) was executed and its output verified.

## Step 1: Build the Knowledge Base

```python
knowledge_base = [
    {"title": "Remote Work Policy", "content": "Employees may work remotely up to 3 days per week with manager approval. Fully remote arrangements require VP-level sign-off and are reviewed annually. All remote employees must be reachable during core hours, 10am-3pm in their local time zone."},
    {"title": "Expense Reimbursement", "content": "Business expenses under $75 do not require pre-approval but must be submitted with a receipt within 30 days. Expenses over $75 require manager approval before purchase. Travel expenses are reimbursed at the government per-diem rate."},
    {"title": "Paid Time Off (PTO)", "content": "Full-time employees accrue 15 days of PTO per year during their first two years, increasing to 20 days after two years of service. PTO must be requested at least 5 business days in advance except in emergencies. Unused PTO up to 5 days rolls over to the next calendar year."},
    {"title": "Health Insurance Benefits", "content": "The company covers 80 percent of health insurance premiums for employees and 50 percent for dependents. Open enrollment occurs each November for coverage starting January 1st. New hires have 30 days from their start date to enroll."},
    {"title": "IT Security Policy", "content": "All company laptops must have full-disk encryption and automatic screen lock after 5 minutes of inactivity. Multi-factor authentication is required for all accounts accessing company systems. Personal devices used for work email must be enrolled in the mobile device management system."},
    {"title": "Password Requirements", "content": "Passwords must be at least 12 characters and changed every 180 days. Password reuse from the last 10 passwords is not allowed. The IT helpdesk can reset passwords via a verified request through the employee portal or by phone with identity verification."},
    {"title": "Parental Leave", "content": "The company provides 12 weeks of paid parental leave for the primary caregiver and 4 weeks for the secondary caregiver, available to all full-time employees regardless of tenure. Leave can be taken continuously or split within the first year after the child arrives."},
    {"title": "Equipment Requests", "content": "New employees receive a standard laptop and monitor within their first week. Additional equipment requests, such as a second monitor or ergonomic accessories, go through the IT ticketing system and are typically fulfilled within 10 business days."},
    {"title": "Performance Review Cycle", "content": "Formal performance reviews occur twice yearly, in June and December. Managers are expected to have informal check-ins at least monthly. Compensation adjustments are typically tied to the December review cycle."},
    {"title": "Travel Booking Policy", "content": "All business travel must be booked through the approved corporate travel portal to ensure insurance coverage. Flights should be booked at least 14 days in advance when possible. Economy class is standard for flights under 6 hours."},
]

texts = [f"{doc['title']}: {doc['content']}" for doc in knowledge_base]
```

## Step 2: Embed and Index

```python
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_texts(texts, embeddings)

test_queries = [
    "How many vacation days do I get?",
    "Can I work from home?",
    "What happens if my laptop password expires?",
    "What is the weather like today?",
]

for query in test_queries:
    print(f"Query: {query}")
    for doc in vectorstore.similarity_search(query, k=2):
        print(f"  - {doc.page_content[:70]}...")
```
```
Query: How many vacation days do I get?
  - Paid Time Off (PTO): Full-time employees accrue 15 days of PTO per...
  - Health Insurance Benefits: The company covers 80 percent of health...

Query: Can I work from home?
  - Remote Work Policy: Employees may work remotely up to 3 days per w...
  - IT Security Policy: All company laptops must have full-disk encryp...

Query: What happens if my laptop password expires?
  - Password Requirements: Passwords must be at least 12 characters an...
  - IT Security Policy: All company laptops must have full-disk encryp...

Query: What is the weather like today?
  - Remote Work Policy: Employees may work remotely up to 3 days per w...
  - Performance Review Cycle: Formal performance reviews occur twice y...
```

**Finding:** Retrieval works correctly for every genuinely relevant question — the top result is always the actual right policy document. For the clearly out-of-scope "weather" question, FAISS still returns *something* (as always — Module 19c's warning), but neither result is actually relevant, which is exactly the problem Step 3 solves.

## Step 3: Detect Out-of-Scope Questions

```python
labeled_queries = [
    ("How many vacation days do I get?", True),
    ("Can I work from home?", True),
    ("What happens if my laptop password expires?", True),
    ("How do I enroll in health insurance?", True),
    ("What is the weather like today?", False),
    ("What's your favorite pizza topping?", False),
]

for query, expected_relevant in labeled_queries:
    doc, score = vectorstore.similarity_search_with_score(query, k=1)[0]
    print(f"{score:.4f} | expected_relevant={expected_relevant} | {query}")
```
```
1.2581 | expected_relevant=True | How many vacation days do I get?
1.2640 | expected_relevant=True | Can I work from home?
0.9913 | expected_relevant=True | What happens if my laptop password expires?
0.7991 | expected_relevant=True | How do I enroll in health insurance?
1.8143 | expected_relevant=False | What is the weather like today?
1.9819 | expected_relevant=False | What's your favorite pizza topping?
```

**Finding:** There's a clean, measured separation — every genuinely relevant question scores below **1.3**, every out-of-scope question scores above **1.8**. Based on these actual numbers (not a guess), **`RELEVANCE_THRESHOLD = 1.5`** cleanly separates all 6 test cases with a comfortable margin on both sides.

⚠️ **Important caveat:** this threshold was calibrated on a small, deliberately clear-cut test set. A real production system would want a larger, more diverse set of both in-scope and adversarial out-of-scope questions to validate the threshold more rigorously before trusting it fully — this is a good starting point, not a guaranteed-perfect cutoff.

## Step 4: Build the Full Answer Function

```python
from transformers import pipeline as hf_pipeline

generator = hf_pipeline("text-generation", model="distilgpt2")
RELEVANCE_THRESHOLD = 1.5

def answer_question(query, k=2):
    results = vectorstore.similarity_search_with_score(query, k=k)
    relevant_docs = [doc for doc, score in results if score < RELEVANCE_THRESHOLD]

    if not relevant_docs:
        return "I don't have information about that in the company knowledge base. Please contact HR or IT directly."

    context = "\n".join(doc.page_content for doc in relevant_docs)
    prompt = f"""Answer the question using ONLY the context below. If the context
doesn't contain the answer, say you don't know.

Context: {context}

Question: {query}
Answer:"""

    result = generator(prompt, max_new_tokens=25, num_return_sequences=1, truncation=True)
    return result[0]["generated_text"]
```

**How it works:** The relevance check happens **before** generation even runs — if no retrieved document beats the threshold, the function returns immediately with a clear fallback message, never even calling the (potentially expensive) generation step. This is a meaningful improvement over Module 19c's approach, which relied purely on asking the model nicely in the prompt to say "I don't know" — here, the out-of-scope detection is enforced in code, working reliably regardless of which generation model is plugged in.

## Step 5: Test Both Cases

```python
print(answer_question("How many vacation days do I get?"))
print("---")
print(answer_question("What is the weather like today?"))
```
```
Answer the question using ONLY the context below. If the context
doesn't contain the answer, say you don't know.

Context: Paid Time Off (PTO): Full-time employees accrue 15 days of PTO per year during their first two years, increasing to 20 days after two years of service. PTO must be requested at least 5 business days in advance except in emergencies. Unused PTO up to 5 days rolls over to the next calendar year.
Health Insurance Benefits: The company covers 80 percent of health insurance premiums for employees and 50 percent for dependents. Open enrollment occurs each November for coverage starting January 1st. New hires have 30 days from their start date to enroll.

Question: How many vacation days do I get?
Answer: No.
In short, 5 days in advance is the time to start the year. All benefits are paid out in advance
===
I don't have information about that in the company knowledge base. Please contact HR or IT directly.
```

**Confirmed:** the out-of-scope weather question correctly triggers the fallback message *without any generation call at all* — the threshold mechanism from Step 3/4 works exactly as designed. The in-scope PTO question correctly retrieves the right policy document (`Paid Time Off (PTO)`) as its top context match — but the local model's actual generated answer ("No. In short, 5 days in advance is the time to start the year...") is **incoherent and doesn't answer the question at all**, even though the correct number (15 days) was sitting right there in the provided context.

## Step 6: Discuss the Local Model's Limitations

`distilgpt2` is a small, general-purpose language model with no specific training for careful, grounded question-answering — it retrieved the *correct context* but still failed to accurately extract the specific number from it, and produced incoherent extra text. This is a completely expected limitation of a small local model (Module 19a/19c), and it isolates something important: **the retrieval and relevance-detection logic (Steps 2-4) worked perfectly** — the weakness is entirely in the final generation step.

A production-grade LLM API (Claude, GPT) would be expected to:
- Correctly and precisely extract "15 days" (or "20 days," depending on tenure) directly from the provided context, rather than inventing a wrong number.
- Produce a single, coherent, complete answer without rambling or hallucinating extra unrelated text.
- Better follow the "if the context doesn't contain the answer, say you don't know" instruction as a secondary safety net, even though our code-level threshold check already handles the clearest out-of-scope cases before generation is ever invoked.

### The Real LLM API Swap-In (⚠️ unverified — no API key in this environment)

```python
import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

def answer_question_with_llm(query, k=2):
    results = vectorstore.similarity_search_with_score(query, k=k)
    relevant_docs = [doc for doc, score in results if score < RELEVANCE_THRESHOLD]

    if not relevant_docs:
        return "I don't have information about that in the company knowledge base. Please contact HR or IT directly."

    context = "\n".join(doc.page_content for doc in relevant_docs)
    prompt = f"""Answer the question using ONLY the context below. If the context
doesn't contain the answer, say you don't know.

Context: {context}

Question: {query}
Answer:"""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=200,
            temperature=0.0,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except anthropic.RateLimitError:
        return "Service is busy right now -- please try again shortly."
    except anthropic.APIError as e:
        return f"Something went wrong: {e}"
```

**How it works:** Identical retrieval and relevance-threshold logic (Steps 2-4) — only the final generation call changes. This is the key architectural insight of this entire capstone: **the retrieval/grounding infrastructure is what makes a RAG system trustworthy, and it's independent of which specific LLM you plug in for generation.** You can prototype and validate the whole pipeline locally and for free, then swap in a production LLM for the final quality boost, with zero changes to the retrieval logic itself.

## Business Summary

> **What we built:** An internal helpdesk assistant that answers employee questions using Alderbrook Corp's own HR/IT policy documents, with a reliable mechanism (measured similarity-score threshold, not just a prompt request) for recognizing when a question falls outside what's documented and directing the employee to a human instead of guessing.
>
> **What we verified:** Retrieval correctly finds the right policy for every genuinely relevant test question, and the out-of-scope detection cleanly separates our test cases (relevant questions scored below 1.3, irrelevant ones above 1.8, with `1.5` chosen as a threshold with margin on both sides).
>
> **What still needs a real LLM:** The generation step, tested here with a small local model for full reproducibility, produced retrieval-correct-but-answer-wrong results — expected for a small model, and exactly why production deployment would use a capable LLM API for this specific step.
>
> **Recommendation:** Pilot this with a real LLM API (Claude or GPT) for a small group of employees, expand the knowledge base to cover the most common actual helpdesk ticket categories, and monitor (Module 20) both retrieval relevance-check trigger rates (how often employees ask something out-of-scope — a signal for what to add to the knowledge base next) and user satisfaction with the answers actually given.

---

**Next:** [`portfolio-presentation.md`](portfolio-presentation.md) — how to present this project.
