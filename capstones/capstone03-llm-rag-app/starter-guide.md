# Starter Guide: Internal Helpdesk RAG Assistant Capstone

Use this as a scaffold — it tells you *what* to figure out at each stage, not *how*. Try each step yourself before peeking at `solution.md`.

## Step 1: Build the Knowledge Base

- Write out at least 8-10 short "policy documents" for a fictional company, covering common HR/IT topics (PTO, remote work, benefits, IT security, etc.). Keep each one focused — 2-4 sentences is plenty.
- Combine each document's title and content into a single string ready for embedding.

## Step 2: Embed and Index

- Use `HuggingFaceEmbeddings` with the `sentence-transformers/all-MiniLM-L6-v2` model (Module 19b) and `FAISS.from_texts()` (Module 19c) to build a searchable index of your knowledge base.
- Write a handful of test questions you'd expect employees to ask, and confirm `vectorstore.similarity_search()` retrieves the correct document(s) for each.

## Step 3: Detect Out-of-Scope Questions

- Write a few questions that are clearly *not* covered by your knowledge base (e.g., something totally unrelated to company policy).
- Use `vectorstore.similarity_search_with_score()` (note: lower score = more similar for FAISS's default L2 distance) to see what scores your in-scope vs. out-of-scope test questions actually get.
- Based on your own measured scores (not a guessed number), pick a similarity-score threshold that separates "genuinely relevant" from "not covered" reasonably well across your test questions.

## Step 4: Build the Full Answer Function

- Write a function `answer_question(query)` that:
  1. Retrieves the top-k documents and their scores.
  2. If no retrieved document beats your threshold from Step 3, return a clear "I don't have that information" message *without* even calling a generation model.
  3. Otherwise, build a prompt that explicitly instructs the model to answer using only the retrieved context (Module 19a), and generate a response.
- For generation, use a local Hugging Face `pipeline("text-generation", ...)` model so your whole pipeline is runnable without needing an API key.

## Step 5: Test Both Cases

- Test at least 3 in-scope questions and confirm the retrieved context is genuinely relevant.
- Test at least 2 out-of-scope questions and confirm your threshold correctly triggers the "I don't know" fallback.
- Print the actual similarity scores alongside each result — don't just trust that your threshold works, show the numbers.

## Step 6: Discuss the Local Model's Limitations

- Look closely at what the local generation model actually produced for your in-scope questions. Is it coherent? Does it get specific numbers/facts right, even when the correct information was in the retrieved context?
- Write a short paragraph on what you'd expect a production-grade LLM API (Claude, GPT) to do differently/better here, and why the retrieval/threshold logic (Steps 2-4) matters regardless of which generation model you ultimately use.

---

Once you've worked through this yourself, compare with [`solution.md`](solution.md).
