import json
record = open("C:\\users\\HOME\\futurelearn\\read.json", "r", encoding="utf-8")
records = json.load(record)
value = records["statement"]

