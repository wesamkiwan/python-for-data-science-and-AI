# Capstone 3: Internal Helpdesk Assistant (LLM-Powered RAG App)

🔴 **Difficulty:** Advanced | ⏱️ **Estimated Time:** 4-6h | **Unlocks after:** Module 19 (Generative AI & LLMs)

## 🎯 What This Capstone Demonstrates

This project applies **Module 19 (Generative AI & LLMs)** end to end — prompt engineering, embeddings/semantic search, and a complete RAG (Retrieval-Augmented Generation) pipeline — to a realistic internal tooling scenario, the kind of "chat with our own documents" assistant that's become extremely common across real companies.

---

## ⚠️ A Note on This Capstone's Code

Matching Module 19's transparency standard: **no LLM API key (Anthropic/OpenAI) is available in this authoring environment.** Every piece of this solution that *can* run locally — the knowledge base, embeddings, FAISS retrieval, the relevance-threshold check, and a local generation model — was fully executed and verified end to end. The "swap in a real LLM API" code is written to match current, correct SDK syntax but was not executed live; this is disclosed clearly in `solution.md` at the point it appears, exactly as Module 19a/19c did.

## 📋 The Scenario

You're a data scientist at **Alderbrook Corp**, a mid-sized company. Employees constantly ask HR and IT the same handful of questions — "how many vacation days do I get," "can I work from home," "how do I reset my password" — creating a steady stream of repetitive tickets that pulls staff away from more complex issues.

> "Can you build something employees can just ask directly, that answers using our actual internal policies — not generic advice from the internet — and clearly says 'I don't know, ask HR' when a question falls outside what we've documented?"

This is a textbook RAG use case: ground an LLM's answers in your own company's specific documents, and handle the "I genuinely don't know" case gracefully and reliably.

## 📦 What You're Given

A synthetic-but-realistic company knowledge base — 10 short internal policy documents covering common HR/IT topics (remote work, PTO, health insurance, IT security, passwords, parental leave, equipment requests, performance reviews, expense reimbursement, and travel booking). Built directly into `solution.md`'s code — no external download needed.

## ✅ Requirements

Your deliverable is a complete RAG application that:

1. **Embeds and indexes the knowledge base** using `sentence-transformers` + FAISS via LangChain (Module 19b/19c).
2. **Retrieves relevant documents** for a given employee question.
3. **Detects out-of-scope questions reliably** — using similarity *scores*, not just a prompt instruction — so the system doesn't hallucinate an answer to something it genuinely has no information about (an enhancement beyond Module 19c's prompt-only approach).
4. **Generates a grounded answer**, explicitly instructed to use only the retrieved context (Module 19a's prompt engineering).
5. **Tests both in-scope and out-of-scope questions** and confirms the relevance-detection mechanism actually works, with real measured similarity scores — not assumed thresholds.
6. **Discusses the local-model-vs-real-LLM-API tradeoff honestly** — what a weak local model gets wrong, and what you'd expect a production-grade LLM to do better.

## 🗂️ Folder Contents

- `starter-guide.md` — scaffolded questions to work through yourself first.
- `solution.md` — the complete, fully-executed reference solution with all code and verified output.
- `portfolio-presentation.md` — guidance on presenting this project in a portfolio or interview.

## 💡 How to Use This Capstone

1. Work through it yourself using `starter-guide.md` for structure.
2. Compare against `solution.md` — pay particular attention to the relevance-threshold section, since reliably saying "I don't know" is one of the most practically important (and most often skipped) parts of a real RAG system.
3. If you have your own Anthropic or OpenAI API key, try swapping it into the generation step and compare the answer quality against the local model — you should see a dramatic improvement in coherence and accuracy.
4. Read `portfolio-presentation.md` once you're happy with your version.

---

**Next:** [`starter-guide.md`](starter-guide.md) →
