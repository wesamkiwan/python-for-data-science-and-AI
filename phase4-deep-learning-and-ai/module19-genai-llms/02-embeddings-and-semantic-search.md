# Module 19b: Embeddings & Semantic Search

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 1.5h | **Prerequisites:** [01-prompting-and-llm-apis.md](01-prompting-and-llm-apis.md)

## 🎯 Learning Objectives
- [ ] Generate sentence/document embeddings with `sentence-transformers`
- [ ] Measure semantic similarity between texts with cosine similarity
- [ ] Explain semantic search and how it differs from keyword search
- [ ] Build a simple similarity-based document retrieval system

---

## Module Goal

Extend Module 18a's word-embedding concept to whole sentences and documents, and use it to build **semantic search** — finding relevant text based on *meaning*, not just matching exact keywords. This is the foundational skill for Module 19c's RAG (Retrieval-Augmented Generation) pipeline.

## Why This Matters on the Job

Traditional keyword search (like Module 11's SQL `WHERE column LIKE '%word%'`) fails when someone searches for "vehicle" but your documents say "car," or searches in different phrasing entirely. Semantic search solves this by comparing *meaning* rather than exact text — it's the technology behind modern search engines, recommendation systems, and (critically for the next lesson) letting an LLM find relevant information in your own documents before answering a question.

---

## Installing `sentence-transformers`

```bash
pip install sentence-transformers
```

## Generating Sentence Embeddings

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "The cat sat on the mat.",
    "A feline rested on the rug.",
    "The stock market crashed yesterday.",
    "Investors panicked as share prices fell."
]

embeddings = model.encode(sentences)
print(embeddings.shape)   # (4, 384) -- 4 sentences, each a 384-dimensional vector
```

**How it works:** `SentenceTransformer` is built on the exact same Transformer architecture from Module 18 (this specific model, `all-MiniLM-L6-v2`, is a small, fast, widely-used encoder model), but trained specifically so that entire *sentences* with similar meaning end up with similar embedding vectors — extending Module 18a's word-level embedding idea to full sentences and documents.

## Measuring Similarity: Cosine Similarity

**Cosine similarity** measures how similar two vectors' *directions* are, regardless of their magnitude — a value from -1 (opposite) to 1 (identical direction), with 0 meaning unrelated.

```python
import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

print(f"cat/feline similarity: {cosine_similarity(embeddings[0], embeddings[1]):.4f}")
print(f"cat/stock similarity: {cosine_similarity(embeddings[0], embeddings[2]):.4f}")
print(f"stock/investors similarity: {cosine_similarity(embeddings[2], embeddings[3]):.4f}")
```
```
cat/feline similarity: 0.5560
cat/stock similarity: 0.1110
stock/investors similarity: 0.6718
```

**How it works:** Despite sharing *zero* exact words, `"The cat sat on the mat"` and `"A feline rested on the rug"` score a meaningfully high similarity (`0.556`) because they mean nearly the same thing — the model has learned that "cat" and "feline," "mat" and "rug," "sat" and "rested" are semantically related concepts. Meanwhile, the cat sentence and the stock market sentence — genuinely unrelated topics — score much lower (`0.111`). This is the core mechanism that makes semantic search possible.

🎯 **On the job:** This is precisely why searching "affordable laptop" can correctly surface a product page titled "budget-friendly notebook computer" in a well-built semantic search system — keyword matching alone would completely miss this, since not a single word overlaps.

## Building a Simple Semantic Search System

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "The Eiffel Tower is located in Paris, France, and was completed in 1889.",
    "Python is a popular programming language known for its readable syntax.",
    "The Great Wall of China is over 13,000 miles long.",
    "Machine learning models learn patterns from data without explicit programming.",
    "The Amazon rainforest produces about 20% of the world's oxygen supply."
]

document_embeddings = model.encode(documents)

def search(query, top_k=2):
    query_embedding = model.encode(query)
    similarities = [
        cosine_similarity(query_embedding, doc_embedding)
        for doc_embedding in document_embeddings
    ]
    top_indices = np.argsort(similarities)[::-1][:top_k]
    return [(documents[i], similarities[i]) for i in top_indices]

results = search("Where is the Eiffel Tower?")
for text, score in results:
    print(f"({score:.4f}) {text}")
```

**How it works:** Every document gets embedded *once* (typically done ahead of time, in a batch); a query gets embedded at search time, and cosine similarity ranks every document by how semantically close it is to the query. `np.argsort(similarities)[::-1][:top_k]` sorts indices by similarity descending and takes the top `k` — the same pattern as Module 06's array indexing/sorting skills.

## Scaling Up: Vector Databases

Comparing a query against every document one-by-one (as above) works for small examples, but becomes slow at scale (thousands to millions of documents). **Vector databases/libraries** (like FAISS, used in the next lesson) index embeddings for much faster similarity search:

```python
import faiss
import numpy as np

dimension = document_embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)     # a simple, exact similarity index
index.add(document_embeddings)               # add all document embeddings

query_embedding = model.encode(["Where is the Eiffel Tower?"])
distances, indices = index.search(query_embedding, k=2)

for idx, dist in zip(indices[0], distances[0]):
    print(f"(distance={dist:.4f}) {documents[idx]}")
```
```
(distance=0.4316) The Eiffel Tower is located in Paris, France, and was completed in 1889.
(distance=1.4625) The Great Wall of China is over 13,000 miles long.
```

**How it works:** `IndexFlatL2` searches using Euclidean distance (lower = more similar, the reverse convention from cosine similarity) rather than manually looping through every document in Python — for small document sets like this, the difference is negligible, but the same `faiss` code scales to millions of documents far more efficiently than a manual loop would.

---

## Hands-On Exercise

**Task:** Write `semantic_search_practice.py` that:
1. Creates a list of at least 8 short documents covering at least 3 distinct topics (e.g., cooking, sports, technology).
2. Embeds all documents with `SentenceTransformer("all-MiniLM-L6-v2")`.
3. Writes 3 test queries (phrased differently from the documents' exact wording, testing genuine semantic matching) and retrieves the top 2 most similar documents for each, using either the manual cosine similarity approach or FAISS.
4. Prints each query alongside its retrieved documents and their similarity scores.
5. Writes a comment identifying at least one case where semantic search correctly matched a query to a document with little/no word overlap.

<details>
<summary>✅ Click to see the solution</summary>

```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

documents = [
    "To make a good omelette, whisk the eggs thoroughly before cooking.",
    "Searing a steak on high heat locks in the juices.",
    "The home team won the championship after a dramatic overtime goal.",
    "She trained for months before completing her first marathon.",
    "The new smartphone features a faster processor and better camera.",
    "Cloud computing lets businesses scale their infrastructure on demand.",
    "Basil and oregano are common herbs in Italian cooking.",
    "The tennis match went to five sets before a winner was decided."
]

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

document_embeddings = model.encode(documents)

def search(query, top_k=2):
    query_embedding = model.encode(query)
    similarities = [cosine_similarity(query_embedding, doc_emb) for doc_emb in document_embeddings]
    top_indices = np.argsort(similarities)[::-1][:top_k]
    return [(documents[i], similarities[i]) for i in top_indices]

queries = [
    "What ingredients go well in pasta dishes?",
    "Tell me about a recent athletic competition.",
    "How does technology help companies grow?"
]

for query in queries:
    print(f"\nQuery: {query}")
    for text, score in search(query):
        print(f"  ({score:.4f}) {text}")

# "What ingredients go well in pasta dishes?" correctly retrieves the basil/oregano
# sentence despite sharing zero exact words with "pasta" or "ingredients" as phrased
# -- the model matches on the shared cooking/Italian-food MEANING, not literal text.
```
</details>

## Common Pitfalls & Best Practices

| ⚠️ Pitfall | ✅ Best Practice |
|---|---|
| Comparing embeddings from different models | Always use the SAME embedding model for both documents and queries |
| Confusing cosine similarity (higher=better) with L2 distance (lower=better) | Check which convention your specific search method uses |
| Re-embedding all documents on every search | Embed documents once, store the embeddings, embed only the query at search time |
| Assuming semantic search always beats keyword search | Semantic search excels at meaning-based matches; exact keyword/ID lookups (e.g., a specific product SKU) are often still better served by exact matching |

---

## ✅ Module Completion Checklist (Part B)
- [ ] Can generate sentence embeddings with `sentence-transformers`
- [ ] Can compute cosine similarity between embeddings
- [ ] Understand semantic search and how it differs from keyword search
- [ ] Can build a simple similarity-based retrieval system, with or without FAISS
- [ ] Completed the `semantic_search_practice.py` exercise

**Next:** Continue to [`03-building-a-rag-pipeline.md`](03-building-a-rag-pipeline.md)
