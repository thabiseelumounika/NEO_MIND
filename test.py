import json

info = {
    "name": "Mouni",
    "project": "NeoMind",
    "features": ["chatbot", "alarms", "tasks"]
}

# Convert to JSON and save to a file
with open("info.json", "w") as file:
    json.dump(info, file)

# Read it back
with open("info.json", "r") as file:
    data = json.load(file)

print("Loaded from JSON file:", data)


