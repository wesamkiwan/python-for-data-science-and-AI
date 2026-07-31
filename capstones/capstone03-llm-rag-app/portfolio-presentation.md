# Presenting This Project in a Portfolio or Interview

## Why This Project Works Well as a Portfolio Piece

RAG/LLM applications are extremely hot right now, and most portfolio projects in this space are shallow — "I called an LLM API with some context." This project goes further: it demonstrates a genuinely production-minded detail (a *measured*, code-enforced relevance threshold for out-of-scope detection) that most junior candidates never think to build, and it's honest about exactly where a small local model falls short versus a real LLM — showing real engineering judgment, not just API-calling.

## For a GitHub Portfolio

1. **Lead with the business problem** — "Built an internal RAG assistant that answers employee HR/IT questions from company policy and reliably says 'I don't know' for anything outside them" is a much stronger opening than "built a RAG pipeline with LangChain."
2. **Show the relevance-threshold table** (Step 3's measured scores) prominently — this is the most technically interesting part of the project, and it's backed by real numbers, not a guess.
3. **Be upfront about the local-model limitation** — showing the incorrect "2 weeks" answer alongside the discussion of what a real LLM would do differently demonstrates maturity and honesty that stands out.
4. **Include the "swap in a real LLM" code** even though it's unverified in your dev environment — clearly labeled, it shows you understand exactly how the production version would differ, and that the retrieval architecture is what actually matters.

## Interview Talking Points

**If asked "walk me through a generative AI / LLM project you've built":**
> "I built an internal RAG assistant for answering common HR and IT policy questions, grounded in the company's own documents rather than an LLM's general knowledge. The part I'm most proud of is the out-of-scope detection — instead of just asking the model nicely to say 'I don't know' in the prompt, which isn't fully reliable, I measured actual similarity scores across labeled test questions and found a clean separation: genuinely relevant questions scored under 1.3, irrelevant ones scored over 1.8. I used that to build a code-level threshold check that runs before generation even happens, so the system never even attempts to hallucinate an answer to something it has no information about. I tested the full pipeline with a small local model to keep everything free and reproducible during development, and I was honest in my writeup that the local model's actual generated answers were sometimes wrong even when retrieval found the correct context — which isolated that the weakness was specifically in the generation step, not the retrieval architecture, and is exactly what you'd fix by swapping in a production LLM API."

**This answer demonstrates:** RAG architecture understanding, a genuinely non-obvious engineering improvement (measured threshold vs. prompt-only), scientific honesty about a component's limitations, and clear separation of concerns (retrieval quality vs. generation quality).

## Likely Follow-Up Questions to Prepare For

- **"How did you choose your relevance threshold?"** — Walk through Step 3 directly: you measured actual scores on labeled test questions rather than guessing, and picked a value with margin on both sides of the observed gap. Be honest that a larger, more adversarial test set would be needed to fully validate it before real production use.
- **"What would break this system in production?"** — Good answers: a question that's *topically* related but not actually answerable from the knowledge base (e.g., asking about a nuanced edge case of a policy that's only partially covered) could still score below the threshold and lead to an incomplete or misleading answer; the knowledge base would need continuous updates as company policy changes; and the threshold itself might need recalibration as the knowledge base grows and its embedding space becomes denser.
- **"Why use a local model at all if it gets the answer wrong?"** — Explain the practical development benefit: it lets you build, test, and validate the entire retrieval/relevance pipeline for free and without needing an API key, isolating exactly which component (retrieval vs. generation) needs the real LLM's quality — a genuinely useful development practice, not just a workaround.
- **"How would you monitor this in production?"** — Reference Module 20 directly: log every query along with its top retrieval score and whether the fallback triggered — a rising fallback rate over time is a direct, actionable signal for what topics to add to the knowledge base next.

## What to Avoid

- ❌ Don't claim the local model's answers were good — the whole point of a strong presentation here is the honest gap analysis between retrieval quality (excellent) and local generation quality (weak), and what that isolates.
- ❌ Don't skip mentioning that the threshold was empirically measured, not guessed — this is the single most impressive, defensible detail in the entire project.
- ❌ Don't present this as "production-ready as-is" — the honest recommendation (pilot with a real LLM, expand the knowledge base, monitor fallback rates) is more credible than an overclaim.
