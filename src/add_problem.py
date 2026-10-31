import json
import sys

PATH = "problems/problems.json"


def main(new_path):
    with open(PATH, encoding="utf-8-sig") as f:
        problems = json.load(f)
    with open(new_path, encoding="utf-8-sig") as f:
        new = json.load(f)
    if isinstance(new, dict):
        new = [new]
    existing = {p["id"] for p in problems}
    for p in new:
        if p["id"] in existing:
            print("skipping duplicate id", p["id"])
            continue
        problems.append(p)
    with open(PATH, "w", encoding="utf-8") as f:
        json.dump(problems, f, indent=2, ensure_ascii=False)
    print(len(problems), "problems:", [p["id"] for p in problems])


if __name__ == "__main__":
    main(sys.argv[1])
