# 📋 Module 19 Cheat Sheet: Generative AI & LLMs

Fast reference for prompting, embeddings/semantic search, and RAG with LangChain.

## Prompt Engineering Techniques

| Technique | What it does | Example |
|---|---|---|
| Zero-shot | Describe the task in words only | "Classify this review's sentiment." |
| Few-shot | Provide labeled examples before the task | Show 2-3 example Q→A pairs, then the real question |
| Chain-of-thought | Ask for step-by-step reasoning | "Think through this step by step before answering." |
| Format specification | Explicitly request output structure | "Respond only with valid JSON: {...}" |

## Calling an LLM API (Anthropic example — needs your own API key)
```python
import os
import anthropic

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

response = client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=1024,
    temperature=0.0,             # 0 = deterministic; higher = more creative/varied
    system="You are a helpful assistant.",
    messages=[{"role": "user", "content": "Your prompt here"}]
)
print(response.content[0].text)
```
```python
try:
    response = client.messages.create(...)
except anthropic.RateLimitError:
    ...   # wait and retry
except anthropic.APIError as e:
    ...   # log/handle
```
⚠️ Never hard-code an API key — load from an environment variable.

## Embeddings & Semantic Search
```python
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(["sentence one", "sentence two"])   # (n, 384)

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```
💡 Semantically similar texts get similar embeddings, even with zero exact word overlap.

## Vector Search with FAISS
```python
import faiss

index = faiss.IndexFlatL2(embedding_dim)
index.add(document_embeddings)
distances, indices = index.search(query_embedding, k=2)   # LOWER distance = more similar
```

## RAG Pipeline with LangChain
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# 1. Split long documents
splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=20)
chunks = splitter.split_text(long_text)

# 2. Embed + index
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_texts(documents, embeddings)

# 3. Retrieve
retrieved = vectorstore.similarity_search(query, k=2)
context = "\n".join(doc.page_content for doc in retrieved)

# 4. Augment + Generate
prompt = f"""Answer using ONLY this context. If it doesn't contain the answer, say so.
Context: {context}
Question: {query}
Answer:"""
# ... pass `prompt` to an LLM API (Module 19a) or a local pipeline for generation
```

## RAG: The Three Steps
1. **Retrieve** — semantic search finds relevant chunks of your own documents.
2. **Augment** — insert retrieved text into the prompt as context.
3. **Generate** — LLM answers using that context, not just its pretrained knowledge.

## Quick Troubleshooting

| Symptom | Likely Cause | Fix |
|---|---|---|
| Inconsistent/random-feeling API output | `temperature` too high for a factual task | Use `temperature=0` for reproducible/structured tasks |
| LLM answers using outside knowledge, ignoring your documents | Prompt didn't instruct it to stick to context | Explicitly say "answer using ONLY the context provided" |
| Retrieval returns irrelevant chunks for an uncovered topic | FAISS always returns its top-k closest matches, relevant or not | Always allow the prompt to say "I don't know" |
| Documents split awkwardly mid-sentence | Chunk size too small, no overlap | Increase `chunk_size` and/or `chunk_overlap` |
| API key exposed in source code | Hard-coded key | Load from an environment variable instead |

## The "New RAG Task" Workflow
1. Split your documents into reasonably-sized, overlapping chunks.
2. Embed all chunks once with `sentence-transformers`/`HuggingFaceEmbeddings`; store in FAISS.
3. At query time: embed only the query, retrieve top-k relevant chunks.
4. Build a prompt that explicitly grounds the LLM in that retrieved context.
5. Call a capable LLM API for generation; handle errors with `try`/`except`.
