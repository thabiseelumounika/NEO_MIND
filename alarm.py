import os
import json
import time
import threading
import pygame
from datetime import datetime

# Path to alarms file
ALARMS_FILE = os.path.join('database', 'alarms.json')

# -------------------- Get All Alarms --------------------
def get_all_alarms():
    try:
        with open(ALARMS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# -------------------- Save Alarm to File --------------------
def save_alarm(alarm_time, message):
    try:
        with open(ALARMS_FILE, 'r') as f:
            alarms = json.load(f)
    except FileNotFoundError:
        alarms = []

    alarms.append({
        "time": alarm_time,
        "message": message
    })

    with open(ALARMS_FILE, 'w') as f:
        json.dump(alarms, f, indent=2)

# -------------------- Set Alarm and Play Ringtone --------------------
def set_alarm(alarm_time, message):
    # Save the alarm first
    save_alarm(alarm_time, message)

    # Alarm job runs in a thread
    def alarm_job():
        while True:
            now = datetime.now().strftime("%Y-%m-%dT%H:%M")
            if now == alarm_time:
                print(f"\n🔔 Alarm Ringing: {message}")
                try:
                    pygame.mixer.init()
                    pygame.mixer.music.load("static/ringtone.mp3")
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(1)
                except Exception as e:
                    print(f"Error playing alarm ringtone: {e}")
                break
            time.sleep(10)

    threading.Thread(target=alarm_job, daemon=True).start()

