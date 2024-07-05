import json

with open("olx_osobowe.json", "r", encoding="utf-8") as f:
    data = json.load(f)


res = []

for d in data:
    val = d["drive"]
    res.append(val)

print(set(res))