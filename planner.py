import json
import os

# File path
TASK_FILE = os.path.join('database', 'tasks.json')

# Ensure task file and folder exist
os.makedirs(os.path.dirname(TASK_FILE), exist_ok=True)
if not os.path.exists(TASK_FILE):
    with open(TASK_FILE, 'w') as f:
        json.dump([], f)

# Add new task to file
def add_task(title, date, time, note):
    with open(TASK_FILE, 'r') as f:
        try:
            tasks = json.load(f)
        except json.JSONDecodeError:
            tasks = []

    tasks.append({
        'title': title,
        'date': date,
        'time': time,
        'note': note.strip() if note.strip() else "📝 No notes provided"
    })

    with open(TASK_FILE, 'w') as f:
        json.dump(tasks, f, indent=2)

# Get all upcoming tasks
def get_upcoming_tasks():
    if not os.path.exists(TASK_FILE):
        return []

    with open(TASK_FILE, 'r') as f:
        try:
            tasks = json.load(f)
            print("📋 Loaded tasks from JSON:", tasks)
        except Exception as e:
            print("❌ Error reading tasks.json:", e)
            tasks = []

    return tasks
