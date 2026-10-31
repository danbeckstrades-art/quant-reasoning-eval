import json
import sys

problems = {p["id"]: p["question"] for p in json.load(open("problems/problems.json", encoding="utf-8-sig"))}
print(problems[sys.argv[1]], end="")
