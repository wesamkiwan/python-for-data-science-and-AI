# 🎤 Module 19 Interview Prep: Generative AI & LLMs

## Conceptual Questions

### 🟢 Beginner

**Q: What is an LLM, in terms of the architecture you already know?**
> A: An LLM is a very large decoder-only Transformer (Module 18b), trained to predict the next token in a sequence over enormous amounts of text. At sufficient scale (billions of parameters, huge training datasets), this simple next-token-prediction objective produces models capable of coherent writing, question answering, and complex instruction-following — it's the same self-attention foundation from Module 18, just scaled up dramatically.

**Q: What's the difference between zero-shot and few-shot prompting?**
> A: Zero-shot prompting describes the task in words only, with no examples. Few-shot prompting provides a small number of labeled examples within the prompt before the actual task, showing the model the exact desired format and reasoning pattern — this often improves reliability and consistency compared to a description alone.

**Q: Why shouldn't you hard-code an API key directly in your source code?**
> A: If that code is ever committed to version control (Module 05b) or shared, the key becomes exposed to anyone with access to the repository or file, potentially letting them run up charges or access data under your account. API keys should always be loaded from an environment variable or a dedicated secrets manager, kept out of source code entirely.

### 🟡 Intermediate

**Q: Explain RAG (Retrieval-Augmented Generation) and the specific problem it solves.**
> A: RAG combines semantic search (retrieving relevant chunks from your own documents based on meaning) with an LLM's generation capability — the retrieved context gets inserted into the prompt before asking the question, so the model's answer is grounded in that specific, provided information rather than relying solely on its frozen pretraining knowledge. This solves the problem that an LLM knows nothing about your company's internal documents, recent events past its training cutoff, or anything genuinely private/proprietary to your use case.

**Q: Why does chunk size matter when preparing documents for a RAG pipeline?**
> A: Chunks that are too small may lose important context (a sentence split awkwardly across two chunks loses coherence), while chunks that are too large dilute the specificity of retrieval and can waste prompt space with irrelevant surrounding text. Chunk overlap (a small amount of shared text between consecutive chunks) helps mitigate the "awkward split" problem specifically. The right size is a practical tuning decision balanced against your specific documents and how precisely you need retrieval to work.

**Q: Why is it important to explicitly instruct an LLM to answer "using only the provided context" in a RAG prompt?**
> A: Without that instruction, the LLM may blend in its own general pretrained knowledge alongside (or instead of) the retrieved context, producing answers that aren't actually grounded in or traceable to your specific documents — undermining much of RAG's purpose, which is to ensure accuracy and source-traceability for domain-specific or private information. It also matters for correctly recognizing when the retrieved context genuinely doesn't answer the question, rather than the model confidently guessing from its general knowledge instead.

## Practical/Coding Questions

**Q: Write code that computes the cosine similarity between two sentence embeddings and interprets the result.**
```python
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
embedding_a = model.encode("The weather is sunny today.")
embedding_b = model.encode("It's a bright, clear day outside.")

similarity = np.dot(embedding_a, embedding_b) / (
    np.linalg.norm(embedding_a) * np.linalg.norm(embedding_b)
)
print(f"Similarity: {similarity:.4f}")   # expect a relatively high score -- similar meaning, different words
```
> Explanation: cosine similarity measures how closely two vectors point in the same direction, regardless of magnitude — a high score here confirms the model recognizes these two differently-worded sentences share essentially the same meaning.

**Q: Write a basic RAG retrieval function using LangChain's FAISS integration.**
```python
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_texts(documents, embeddings)

def retrieve_context(query, k=2):
    results = vectorstore.similarity_search(query, k=k)
    return "\n".join(doc.page_content for doc in results)
```
> Explanation: `FAISS.from_texts()` embeds and indexes every document in one call; `similarity_search()` finds the top-k most semantically relevant documents for a given query, ready to be inserted into a generation prompt as context.

## Scenario Questions

**Q: A company wants a chatbot that can answer employee questions using their internal HR policy documents. How would you approach this?**
> A: This is a textbook RAG use case — I'd split the HR documents into reasonably-sized chunks, embed and index them (e.g., with `sentence-transformers` and FAISS via LangChain), then at query time retrieve the most relevant policy chunks for each employee question and hand them to an LLM with an explicit instruction to answer only using that retrieved context. This ensures answers stay grounded in the company's actual, current policies rather than the LLM's general pretrained knowledge, which could be outdated, generic, or simply wrong for this specific company's rules.

**Q: An LLM-powered support tool sometimes gives confidently wrong answers about topics your documents don't actually cover. How would you address this?**
> A: I'd first check the prompt explicitly instructs the model to say when the provided context doesn't contain the answer, rather than assuming the model will infer this on its own. I'd also consider adding a relevance threshold on the retrieval step — if the top retrieved chunk's similarity score is below some cutoff, treat that as "no relevant information found" and respond accordingly, rather than handing genuinely irrelevant context to the LLM and letting it attempt an answer regardless.

## "Gotcha" Questions

**Q: A RAG pipeline retrieves documents even for a query completely unrelated to anything in the document set. Why does this happen, and is it a bug?**
> A: This isn't a bug — a standard similarity search index (like FAISS's `IndexFlatL2`) always returns its top-k *closest* matches by design, even if none of them are genuinely relevant to the query; there's no built-in concept of "no good match exists" unless you explicitly check similarity scores against a threshold. This is exactly why RAG prompts should always include an explicit "say you don't know if the context doesn't help" instruction, and why real systems often add a relevance-score cutoff before even attempting generation.

**Q: Why might increasing an LLM's `temperature` improve creative writing tasks but hurt tasks like data extraction or classification?**
> A: Higher temperature makes the model's next-token choices more varied and less deterministic, which is valuable when you want creative, diverse output. But for tasks requiring a single precise, consistent, reproducible answer (extracting a specific number from text, classifying into a fixed category), that same randomness introduces unwanted inconsistency — the same input might produce different outputs on different runs. `temperature=0` is generally preferred for these more deterministic, structured tasks.

## Quick-Fire Rapid Review

- Q: What kind of Transformer is a typical LLM? → **decoder-only**
- Q: Prompting technique that provides labeled examples before the task? → **few-shot**
- Q: Prompting technique that asks for step-by-step reasoning? → **chain-of-thought**
- Q: What does `temperature=0` produce? → **deterministic, reproducible output**
- Q: What does RAG stand for? → **Retrieval-Augmented Generation**
- Q: What are the three steps of RAG? → **retrieve, augment, generate**
- Q: Why must retrieval always allow for "I don't know" in the prompt? → **similarity search always returns its closest matches, even when none are truly relevant**
- Q: Where should an API key be stored, never in source code? → **an environment variable or secrets manager**
