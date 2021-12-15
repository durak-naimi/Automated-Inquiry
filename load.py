import json
record = open("read.json", "r", encoding="utf-8")
records = json.load(record)
value = records["statement"]

