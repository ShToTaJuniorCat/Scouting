import csv
from pyperclip import copy
import update_app

with open(f"data.csv", encoding="utf-8") as file:
    handle = csv.reader(file)

    data = list(handle)


quest = data[0]
excluded_questions = ["Timestamp"]
team_number = input("Team number: #")
info = ""

for row in data:
    if row[1] != team_number:
        continue

    for i, col in enumerate(row):
        if quest[i] in excluded_questions:
            continue
        
        a = f"*{quest[i]}:* {col}"
        print(a)
        info += a + "\n"

copy(info)
