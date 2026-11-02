# Evaluating AI Answers to Statistics Problems

I put together a set of 15 statistics and machine-learning problems with reference answers and rubrics, collected answers from two AI assistants, and graded all 30 answers against the rubrics. The aim was to practice the work of evaluating quantitative reasoning: checking the arithmetic, the method, and the claims, and recording where answers go wrong.

## Problem set
- 15 problems on p-values, confidence intervals, Simpson's paradox, data leakage, base rates, sample size, multiple comparisons, imbalanced metrics, regression to the mean, paired tests, overfitting, margin of error, ROC-AUC, and peeking in A/B tests.
- Each problem has a reference answer, a rubric of specific items, and failure modes I wrote down before collecting any answers. See `problems/problems.json`.
- I checked the numbers in every reference answer by hand.

## Collecting answers
- Two assistants, Gemini and Copilot, both in the web app on default (Auto) mode, with no specific model version shown.
- Each question was pasted exactly as written into a new chat, with nothing added and no follow-ups. The assistants never saw the rubrics.
- I did not switch on search or other tools. I could not see whether Auto mode used them on its own.

## Grading
- I shuffled the 30 answers under neutral IDs (B01 to B30) and graded them without knowing which assistant wrote each one.
- For each answer I checked every rubric item against the response and the reference answer, recomputed numbers where I was unsure, and scored an item as met only if the answer stated it explicitly and correctly. When in doubt I scored it as not met.
- "Fully correct" means that nothing stated was wrong and every part of the question was answered correctly. An answer can be fully correct and still miss a rubric item.

## Results (15 answers each)

| Assistant | Fully correct | 95% Wilson CI | Mean rubric coverage |
|---|---|---|---|
| Gemini (Auto) | 12 of 15 (80%) | 55% to 93% | 88.9% |
| Copilot (Auto) | 14 of 15 (93%) | 70% to 99% | 95.7% |

- **Paired comparison:** Gemini was right and Copilot wrong on 0 problems, and Copilot was right and Gemini wrong on 2 (data leakage and confidence-interval interpretation). Exact sign test p = 0.50.
- **Rubric coverage difference** (Gemini minus Copilot): -0.068, 95% bootstrap CI -0.141 to +0.000. With 15 problems this interval is fragile, so I rely on the sign test.
- **I cannot say one assistant is better.** The intervals overlap heavily and only two problems separated them.
- **The one problem both missed was q15 (peeking).** Both overestimated the false-positive rate for ten looks, one with a 20 to 30% range and one with 40% from assuming independent looks. The usual figure is about 19%, which my own A/A simulation in the A/B project also found (19.2%).
- **Other errors:** an overstated claim about how large leakage from plain scaling is (q04), a verdict labelled "incorrect" on a statement that the same answer's reasoning showed was true (q09), and a loose range for the peeking rate (q15).
- Per-problem results are in `reports/per_problem.csv`.

## What I take from this
Both assistants handle textbook calculations and standard interpretations reliably. The failures were in quantitative claims that need the right model of a procedure (sequential testing) and in internal consistency between a verdict and its explanation. A problem set like this one is too easy to rank the assistants, and the next version needs harder problems.

## Limitations
- **One grader, no second independent grader.** I did not measure grading consistency. A re-grade after a delay would be the next check.
- **The blind was imperfect.** I recognized the first answer I had collected (q01), which also revealed its pair by elimination, and one answer's saved copy had been cut off by a copy error, so I repaired it from the chat and re-graded it, which showed me its author. Three of the 30 scores were therefore not fully blind.
- **Rubric flaws.** On the paired-test problem the last rubric item demanded a p-value the question never asked for, which lowers rubric coverage for both assistants. I kept the rubric unchanged after seeing answers to keep grading consistent, and noted the flaw.
- **Small and easy problem set:** 15 problems, 15 answers per assistant, 26 of 30 fully correct. Differences below about 20 percentage points cannot be detected.
- **One answer per question per assistant.** Re-asking would give different text, so these are single draws, not stable properties of the assistants.
- **Settings I could not control:** Auto mode and unknown model versions. The numbers describe these assistants on 31 October 2026 and may not transfer.
- **Copy formatting:** math notation was garbled when I copied answers into files. I did not penalize formatting.

## Reproduce
    python src/make_prompts.py gemini copilot
    python src/make_blind.py
    python src/grade.py
    python src/analyze.py

`src/get_q.py` prints one question for pasting, and `src/check_responses.py` checks for empty or question-echo answer files. The grading key is `grading/key.csv`, and my scores are in `grading/scores.csv`. Random seeds are fixed at 42.
