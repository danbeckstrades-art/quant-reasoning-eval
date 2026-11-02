import csv
import json
import pathlib

problems = {p["id"]: p for p in json.load(open("problems/problems.json", encoding="utf-8-sig"))}
key = list(csv.DictReader(open("grading/key.csv", encoding="utf-8")))
out_path = pathlib.Path("grading/scores.csv")
fields = ["blind_id", "qid"] + [f"item{i}" for i in range(1, 7)] + ["overall_correct", "error_type", "notes"]
ERRORS = {"c": "calculation", "k": "concept", "u": "unjustified_claim", "i": "incomplete", "o": "other"}

if out_path.exists():
    done = {r["blind_id"] for r in csv.DictReader(open(out_path, encoding="utf-8"))}
else:
    done = set()
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow(fields)


def ask(prompt, allowed):
    while True:
        a = input(prompt).strip().lower()
        if a in allowed:
            return a
        print("  enter one of:", "/".join(sorted(allowed)))


for row in key:
    bid, model, qid = row["blind_id"], row["model"], row["qid"]
    if bid in done:
        continue
    p = problems[qid]
    text = pathlib.Path("responses", model, f"{qid}.txt").read_text(encoding="utf-8-sig", errors="replace")
    print("\n" + "=" * 70)
    print(f"{bid}  (problem {qid}, topic: {p['topic']})")
    print("=" * 70)
    print("QUESTION:\n" + p["question"])
    print("\nRESPONSE:\n" + text)
    print("\n" + "-" * 70)
    print("REFERENCE ANSWER:\n" + p["reference_answer"])
    print("\nRUBRIC ITEMS:")
    for i, item in enumerate(p["rubric"], 1):
        print(f"  {i}. {item}")
    items = []
    for i in range(1, 7):
        if i <= len(p["rubric"]):
            items.append("1" if ask(f"Item {i} met? (y/n): ", {"y", "n"}) == "y" else "0")
        else:
            items.append("")
    overall = "1" if ask("Fully correct overall? (y/n): ", {"y", "n"}) == "y" else "0"
    etype = "none"
    if overall == "0":
        print("Main error: c=calculation, k=concept, u=unjustified claim, i=incomplete, o=other")
        etype = ERRORS[ask("Error type: ", set(ERRORS))]
    notes = input("Notes (optional): ").strip()
    with open(out_path, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([bid, qid] + items + [overall, etype, notes])
    if ask("Next? (enter = continue, q = quit): ", {"", "q"}) == "q":
        break
print("Saved to", out_path)
