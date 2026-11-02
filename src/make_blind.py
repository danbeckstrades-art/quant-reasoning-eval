import csv
import json
import pathlib
import random

problems = json.load(open("problems/problems.json", encoding="utf-8-sig"))
models = ["gemini", "copilot"]
pairs = [(m, p["id"]) for m in models for p in problems]
random.Random(42).shuffle(pairs)

pathlib.Path("grading").mkdir(exist_ok=True)
with open("grading/key.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["blind_id", "model", "qid"])
    for i, (m, q) in enumerate(pairs, 1):
        w.writerow([f"B{i:02d}", m, q])
print(len(pairs), "blind ids written. Do not open grading/key.csv until all grading is finished.")
