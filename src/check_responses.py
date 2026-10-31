import json
import pathlib
import sys

problems = {p["id"]: p["question"] for p in json.load(open("problems/problems.json", encoding="utf-8-sig"))}
model = sys.argv[1]
done, empty, flagged = [], [], []
for qid, question in problems.items():
    f = pathlib.Path("responses") / model / f"{qid}.txt"
    text = f.read_text(encoding="utf-8-sig") if f.exists() else ""
    if not text.strip():
        empty.append(qid)
    else:
        done.append(qid)
        if question[:50] in text:
            flagged.append(qid)
print("filled:", done)
print("empty:", empty)
print("still contain the question (fix these):", flagged)
