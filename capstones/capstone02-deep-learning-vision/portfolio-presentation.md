# Presenting This Project in a Portfolio or Interview

## Why This Project Works Well as a Portfolio Piece

This project demonstrates real computer vision skill (building and evaluating a CNN from scratch) *and* something rarer and more valuable: the scientific honesty to report a genuinely mixed result (data augmentation) rather than forcing a clean narrative. Many portfolio projects show only wins — this one shows real analytical judgment under an inconclusive result, which is exactly what separates a junior from a senior mindset in interviews.

## For a GitHub Portfolio

1. **Lead with the business framing** — "Built an automated product image classifier for a clothing retailer's catalog pipeline" is a much stronger opening line than "trained a CNN on Fashion-MNIST."
2. **Show the confusion matrix visually** — a heatmap of the confusion matrix (Module 09's Seaborn skills) is far more compelling on a first skim than a wall of numbers, and immediately communicates "the model is great at some things, weak at others" — a nuanced, credible finding.
3. **Dedicate a clear section to the augmentation experiment** — specifically call out that you tested train/test gap, not just final accuracy, and that the result was genuinely mixed. This is a strong differentiator; most portfolio projects don't demonstrate this level of rigor.
4. **End with the targeted deployment recommendation** — "deploy for 6 of 10 categories, human review for the other 4" is a specific, actionable, business-minded conclusion that shows you think beyond just "the model works."

## Interview Talking Points

**If asked "walk me through a computer vision project you've built":**
> "I built a CNN to automatically categorize product images for a clothing retailer's catalog — Fashion-MNIST is actually a great fit here since it was built by an actual clothing retailer for this exact use case. I got 87.6% overall accuracy, but the more useful finding was in the per-class breakdown: trousers, sandals, and boots were essentially solved at 95%+ F1, while shirts were a real weak spot at 68%, mostly confused with t-shirts and coats — which makes sense, since those are visually similar upper-body garments at low resolution. I also tested data augmentation, which is supposed to help, but here it actually reduced the train-test gap — showing less overfitting — without improving the final test accuracy at my training budget. Rather than force a 'clean win' narrative, I reported that honestly and recommended further testing with more epochs before deciding whether to include it in production. My final recommendation was a targeted deployment: auto-tag the six reliable categories, but require human review specifically for the four confusable ones."

**This answer demonstrates:** technical CNN skills, careful per-class evaluation (not just headline accuracy), honest scientific reporting under a mixed result, and a specific, actionable business recommendation.

## Likely Follow-Up Questions to Prepare For

- **"Why didn't augmentation improve test accuracy here?"** — Be ready to discuss that augmentation's benefit often needs more training epochs or a smaller/more overfitting-prone original dataset to show up as a raw accuracy gain, and that the reduced train-test gap is still a real, meaningful signal even without a final-score improvement.
- **"How would you improve the Shirt category's performance specifically?"** — Good answers: collect/inspect more example images specifically from the confused categories to look for actual data quality issues, try a deeper architecture, or consider that color/texture information (unavailable in this grayscale dataset) might be genuinely necessary to reliably distinguish these categories — sometimes the fix is "get better/richer data," not "tune the model more."
- **"How would you deploy and monitor this model?"** — Reference Module 20 directly: package with `joblib`/`torch.save`, serve via FastAPI, and monitor prediction confidence distributions over time — a rising rate of low-confidence predictions specifically in the Shirt/T-shirt/Coat/Pullover cluster would be an early warning sign worth watching for.
- **"Would transfer learning help here?"** — A thoughtful answer: transfer learning (Module 17c) typically uses models pretrained on full-color, higher-resolution natural images (ImageNet) — applying it to small grayscale 28×28 images requires resizing and channel replication, and the benefit is less clear-cut than for typical photographic images; worth testing, but not an automatic win the way it often is for standard-resolution color photos.

## What to Avoid

- ❌ Don't hide or gloss over the augmentation result — reporting it honestly is the single most impressive part of this project for an experienced interviewer; smoothing it into a fake "augmentation helped!" story would actually make the project *less* credible on scrutiny.
- ❌ Don't present 87.6% as a single, uniform "the model works" result — the whole value of this analysis is in the per-class nuance; leading with just the headline number undersells your actual work.
- ❌ Don't claim the model is ready for full, unsupervised production deployment — the specific, targeted recommendation (partial automation + human review for hard categories) is both more honest and more impressive than an overclaim.
