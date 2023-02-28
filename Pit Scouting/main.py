import csv

with open(f"C:/Users/USER/AppData/Local/Programs/Python/Python310/desktop_client/pit scouting/data.csv", encoding="utf-8") as file:
    handle = csv.reader(file)
    data = list(handle)


quest = data[0]
excluded_questions = []

for row in data:
    if row[1] == "מספר קבוצה":
        continue

    for i, col in enumerate(row):
        if quest[i] in excluded_questions:
            continue
        
        print(quest[i])
        print(col)
        print()

    print("\n\n\n\n\n")
