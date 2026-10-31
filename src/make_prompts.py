import json
import pathlib
import sys

problems = json.load(open("problems/problems.json", encoding="utf-8-sig"))
out = pathlib.Path("responses")
out.mkdir(exist_ok=True)

lines = [f"===== {p['id']} =====\n{p['question']}\n" for p in problems]
(out / "prompts.txt").write_text("\n".join(lines), encoding="utf-8")

for model in sys.argv[1:]:
    d = out / model
    d.mkdir(parents=True, exist_ok=True)
    for p in problems:
        f = d / f"{p['id']}.txt"
        if not f.exists():
            f.write_text("", encoding="utf-8")
    meta = d / "meta.txt"
    if not meta.exists():
        meta.write_text(
            "model name and version:\ndate:\nnew or temporary chat (yes/no):\n"
            "tools or web search on (yes/no):\nnotes:\n",
            encoding="utf-8",
        )

print(len(problems), "prompts written; folders:", sys.argv[1:])
