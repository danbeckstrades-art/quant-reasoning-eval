import csv
import json
import pathlib
from collections import Counter

import numpy as np
from scipy import stats

key = {r["blind_id"]: r for r in csv.DictReader(open("grading/key.csv", encoding="utf-8"))}
problems = {p["id"]: p for p in json.load(open("problems/problems.json", encoding="utf-8-sig"))}

rows = []
for r in csv.DictReader(open("grading/scores.csv", encoding="utf-8")):
    k = key[r["blind_id"]]
    assert k["qid"] == r["qid"], r["blind_id"]
    items = [int(r[f"item{i}"]) for i in range(1, 7) if r[f"item{i}"] != ""]
    rows.append({
        "model": k["model"], "qid": r["qid"],
        "overall": int(r["overall_correct"]),
        "frac": sum(items) / len(items),
        "error": r["error_type"],
    })


def wilson(k, n, z=1.96):
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / d
    return c - h, c + h


models = ["gemini", "copilot"]
print("PER ASSISTANT (15 answers each)")
for m in models:
    rs = [r for r in rows if r["model"] == m]
    k = sum(r["overall"] for r in rs)
    lo, hi = wilson(k, len(rs))
    cov = np.mean([r["frac"] for r in rs])
    print(f"  {m:8s} fully correct {k}/{len(rs)} = {k / len(rs):.0%} "
          f"(95% Wilson CI {lo:.0%} to {hi:.0%}); mean rubric coverage {cov:.1%}")

by = {(r["model"], r["qid"]): r for r in rows}
qids = sorted({r["qid"] for r in rows})

b = sum(1 for q in qids if by[("gemini", q)]["overall"] == 1 and by[("copilot", q)]["overall"] == 0)
c = sum(1 for q in qids if by[("gemini", q)]["overall"] == 0 and by[("copilot", q)]["overall"] == 1)
p_sign = stats.binomtest(b, b + c, 0.5).pvalue if b + c else 1.0
print("\nPAIRED COMPARISON (same 15 problems)")
print(f"  gemini right and copilot wrong on {b} problems; copilot right and gemini wrong on {c}")
print(f"  exact sign test p = {p_sign:.3f}")

diffs = np.array([by[("gemini", q)]["frac"] - by[("copilot", q)]["frac"] for q in qids])
rng = np.random.default_rng(42)
boot = [rng.choice(diffs, len(diffs)).mean() for _ in range(5000)]
lo, hi = np.percentile(boot, [2.5, 97.5])
print(f"  mean rubric-coverage difference (gemini - copilot) = {diffs.mean():+.3f} "
      f"(95% bootstrap CI {lo:+.3f} to {hi:+.3f})")

print("\nERROR TYPES (non-correct answers)")
for m in models:
    errs = Counter(r["error"] for r in rows if r["model"] == m and r["overall"] == 0)
    print(f"  {m:8s} {dict(errs) if errs else 'none'}")

print("\nPER PROBLEM")
out = [["qid", "topic", "gemini_overall", "gemini_coverage", "copilot_overall", "copilot_coverage"]]
for q in qids:
    g, cp = by[("gemini", q)], by[("copilot", q)]
    out.append([q, problems[q]["topic"], g["overall"], round(g["frac"], 2), cp["overall"], round(cp["frac"], 2)])
    print(f"  {q} {problems[q]['topic']:24s} gemini {g['overall']} ({g['frac']:.0%})   copilot {cp['overall']} ({cp['frac']:.0%})")

pathlib.Path("reports").mkdir(exist_ok=True)
with open("reports/per_problem.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(out)
print("\nSaved reports/per_problem.csv")
