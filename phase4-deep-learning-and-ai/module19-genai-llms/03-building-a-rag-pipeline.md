# Module 19c: Building a RAG Pipeline with LangChain

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 2h | **Prerequisites:** [02-embeddings-and-semantic-search.md](02-embeddings-and-semantic-search.md)

## 🎯 Learning Objectives
- [ ] Explain RAG (Retrieval-Augmented Generation) and the problem it solves
- [ ] Build a document retrieval pipeline using LangChain
- [ ] Combine retrieval with an LLM to answer questions grounded in your own documents
- [ ] Understand this as the foundation for Capstone 3

---

## Module Goal

Combine Module 19a's LLM prompting and Module 19b's semantic search into a complete **RAG (Retrieval-Augmented Generation)** pipeline — the technique that lets an LLM answer questions using *your own* documents, rather than only its general pretraining knowledge. This is the final skill this course builds toward, and it directly powers Capstone 3.

## Why This Matters on the Job

An LLM's knowledge is frozen at whatever data it was trained on — it knows nothing about your company's internal documents, your product's latest updates, or anything created after its training cutoff. RAG solves this by retrieving relevant information from your own data (Module 19b's semantic search) and handing it to the LLM as context *before* asking it to answer — this is exactly how most production "chat with your documents" and internal knowledge-base assistants actually work.

## Installing LangChain

```bash
pip install langchain langchain-community langchain-huggingface langchain-text-splitters faiss-cpu
```

**LangChain** is a framework for building applications on top of LLMs — it provides standardized building blocks for exactly the retrieval → prompt → generate pipeline this lesson builds, so you don't have to wire every piece together manually.

---

## RAG: The Core Idea

**Retrieval-Augmented Generation** works in three steps:
1. **Retrieve:** given a question, use semantic search (Module 19b) to find the most relevant chunks of your own documents.
2. **Augment:** insert that retrieved text into the prompt as context.
3. **Generate:** ask the LLM to answer the question *using that provided context*, rather than relying solely on its own pretrained knowledge.

💡 **Analogy:** Think of RAG like an open-book exam versus a closed-book one — instead of relying purely on what the model memorized during training (closed-book), you hand it the relevant page of the textbook right before asking the question (open-book), letting it answer accurately even about things it was never specifically trained on.

## Step 1: Load and Split Documents

Real documents are often too long to embed as one single chunk — LangChain's text splitters break them into manageable pieces first.

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

long_document = """
The Eiffel Tower is a wrought-iron lattice tower located in Paris, France. It was
designed by Gustave Eiffel's engineering company and completed in 1889 as the
entrance arch for the World's Fair. Standing at 330 meters tall, it was the
tallest man-made structure in the world for 41 years. Today, it is one of the
most visited paid monuments in the world, attracting millions of tourists annually.
"""

text_splitter = RecursiveCharacterTextSplitter(chunk_size=150, chunk_overlap=20)
chunks = text_splitter.split_text(long_document)
for chunk in chunks:
    print(repr(chunk))
```

**How it works:** `chunk_size=150` splits text into pieces of roughly 150 characters; `chunk_overlap=20` lets consecutive chunks share a little text, reducing the chance that an important sentence gets awkwardly split right at a chunk boundary and loses meaning. Choosing good chunk sizes is itself a practical tuning consideration — small enough for precise, focused retrieval, but large enough that each chunk retains meaningful context.

## Step 2: Embed and Index the Chunks

```python
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

documents = [
    "The Eiffel Tower is located in Paris, France, and was completed in 1889.",
    "Python is a popular programming language known for its readable syntax.",
    "The Great Wall of China is over 13,000 miles long.",
    "Machine learning models learn patterns from data without explicit programming.",
    "The Amazon rainforest produces about 20% of the world's oxygen supply."
]

vectorstore = FAISS.from_texts(documents, embeddings)
```

**How it works:** `HuggingFaceEmbeddings` wraps the exact same `sentence-transformers` model from Module 19b in LangChain's standard interface; `FAISS.from_texts()` embeds every document and builds a searchable index in one call — the same FAISS library from Module 19b, now accessed through LangChain's more convenient abstraction.

## Step 3: Retrieve Relevant Context

```python
query = "Where is the Eiffel Tower located?"
retrieved_docs = vectorstore.similarity_search(query, k=1)

for doc in retrieved_docs:
    print(doc.page_content)
```
```
The Eiffel Tower is located in Paris, France, and was completed in 1889.
```

**How it works:** `similarity_search()` performs exactly the same semantic search from Module 19b — LangChain just wraps it in a consistent, standard interface (`doc.page_content` for the text) that works identically regardless of which underlying vector store you choose.

## Step 4: Generate an Answer Using the Retrieved Context

```python
context = retrieved_docs[0].page_content

prompt = f"""Answer the question using ONLY the context provided below. If the
context doesn't contain the answer, say "I don't have that information."

Context: {context}

Question: {query}
Answer:"""

# Using a real LLM API (Module 19a) -- requires your own API key
import anthropic
client = anthropic.Anthropic()   # reads ANTHROPIC_API_KEY from the environment

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=200,
    messages=[{"role": "user", "content": prompt}]
)
print(response.content[0].text)
```

⚠️ **Note:** Like Module 19a, this specific API call requires your own API key and was not executed live in this course's authoring environment. The instruction *"answer using ONLY the context provided"* is a critical prompt engineering detail (Module 19a) — without it, the LLM might blend in its own general pretrained knowledge instead of strictly grounding its answer in your retrieved documents, which defeats much of RAG's purpose (keeping answers accurate and traceable to a specific source).

### A Fully Local, Verifiable Alternative

To let you run and see a *complete* RAG pipeline without needing an API key, here's the same retrieve-then-generate pattern using a local, open-source generation model instead of a hosted LLM API:

```python
from transformers import pipeline as hf_pipeline

generator = hf_pipeline("text-generation", model="distilgpt2")

result = generator(prompt, max_new_tokens=20, num_return_sequences=1, truncation=True)
print(result[0]["generated_text"])
```
```
Context: The Eiffel Tower is located in Paris, France, and was completed in 1889.

Question: Where is the Eiffel Tower located?
Answer: The Eiffel Tower is located in Paris, France, and was completed in 1889.
```

**How it works:** This runs the exact same retrieve → augment → generate pipeline, fully locally, no API key required — `distilgpt2` is a small, much less capable model than a production LLM, but the underlying RAG mechanics (retrieve relevant context, hand it to a generation model as part of the prompt) are identical. In a real project, you'd swap this local model for a genuinely capable LLM API (as shown above) for meaningfully better answer quality — the *pipeline structure* doesn't change, only which model does the final generation step.

✅ **Best Practice:** When learning or prototyping a RAG pipeline, using a free local model (like this section) lets you iterate on the retrieval logic without incurring API costs; switch to a production-grade LLM API once the pipeline structure works correctly.

---

## Hands-On Exercise

**Task:** Write `rag_pipeline_practice.py` that:
1. Creates a list of at least 6 short "documents" about a topic of your choice (e.g., facts about several countries, several programming languages, or several historical events).
2. Splits, embeds, and indexes them using `RecursiveCharacterTextSplitter`, `HuggingFaceEmbeddings`, and `FAISS`.
3. Writes a function `answer_question(query)` that retrieves the top 2 most relevant chunks, builds a grounded prompt (explicitly instructing the model to only use the provided context), and generates an answer using **either** the local `distilgpt2` approach **or** a real LLM API if you have a key.
4. Tests it with 2 questions, printing the retrieved context and the generated answer for each.
5. Tests it with one question your documents genuinely don't cover, and confirms/discusses whether the prompt's "say you don't know" instruction was followed.

<details>
<summary>✅ Click to see the solution (local model version, fully runnable without an API key)</summary>

```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from transformers import pipeline as hf_pipeline

documents_text = [
    "Python was created by Guido van Rossum and first released in 1991.",
    "JavaScript is the primary language used for interactive web pages and runs in browsers.",
    "Rust is known for its memory safety guarantees without needing a garbage collector.",
    "Go was designed at Google to be simple and efficient for building network services.",
    "Ruby emphasizes programmer happiness and is well known for the Rails web framework.",
    "SQL is a declarative language used to query and manage relational databases."
]

text_splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = text_splitter.split_text(" ".join(documents_text))

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_texts(documents_text, embeddings)

generator = hf_pipeline("text-generation", model="distilgpt2")

def answer_question(query):
    retrieved_docs = vectorstore.similarity_search(query, k=2)
    context = "\n".join(doc.page_content for doc in retrieved_docs)

    prompt = f"""Answer the question using ONLY the context provided below. If the
context doesn't contain the answer, say "I don't have that information."

Context: {context}

Question: {query}
Answer:"""

    print(f"Retrieved context:\n{context}\n")
    result = generator(prompt, max_new_tokens=20, num_return_sequences=1, truncation=True)
    return result[0]["generated_text"]

print(answer_question("Who created Python?"))
print(answer_question("What is Rust known for?"))
print(answer_question("What is the capital of France?"))   # not covered by our documents
```

**Expected outcome:** The first two questions should retrieve genuinely relevant context (the Python and Rust facts). The third, uncovered question should retrieve *something* (FAISS always returns its top-k closest matches, even if none are truly relevant), which is exactly why the explicit "if the context doesn't contain the answer, say so" instruction matters — a weak local model like `distilgpt2` may not follow it reliably, but a capable production LLM API is generally much better at correctly recognizing when the provided context doesn't answer the question.
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Not instructing the model to stick to the provided context | Explicitly say "answer using ONLY the context" to reduce ungrounded, made-up answers |
| Retrieving too few or too many chunks | Tune `k` — too few risks missing relevant info; too many dilutes the prompt with irrelevant text |
| Assuming retrieval always finds something truly relevant | FAISS returns its *closest* matches regardless — always allow for "I don't know" in the prompt |
| Using a weak local model to judge RAG quality | For real quality evaluation, test with a genuinely capable LLM API, not a tiny model like `distilgpt2` |

---

## ✅ Module 19 Completion Checklist
- [ ] Understand RAG and the problem it solves (grounding an LLM in your own data)
- [ ] Can split, embed, and index documents with LangChain
- [ ] Can retrieve relevant context and build a grounded prompt
- [ ] Can combine retrieval with generation into a complete pipeline
- [ ] Completed the `rag_pipeline_practice.py` exercise
- [ ] Reviewed [`module19-cheatsheet.md`](module19-cheatsheet.md)
- [ ] Reviewed [`module19-interview.md`](module19-interview.md)
- [ ] Browsed [`module19-references.md`](module19-references.md)

**Next Step:** Module 20 — MLOps & Deployment (`phase5-deployment/module20-mlops-deployment/`)

---

## 🎉 Phase 4 Complete!

You've finished **Phase 4: Deep Learning & AI** — from neural network fundamentals through CNNs, Transformers, and now a complete RAG pipeline combining semantic search with LLM generation. This is precisely the skillset Capstone 3 (LLM-powered RAG application) will ask you to apply end-to-end on a real project. Module 20 rounds out the entire course by teaching you how to package and deploy any of these models into production.
