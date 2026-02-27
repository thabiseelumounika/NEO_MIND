from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_mail import Mail
import sqlite3
import threading
from datetime import datetime
import os
import json
import pygame
import time

from config import MAIL_USERNAME, MAIL_PASSWORD
from assistant.alarm import set_alarm, get_all_alarms
from assistant.planner import add_task, get_upcoming_tasks
from assistant.ollama_chatbot import get_bot_response

app = Flask(__name__)
app.secret_key = 'neomind_secret_key'

# Ensure folders exist
os.makedirs('database', exist_ok=True)
DB_PATH = os.path.join('database', 'users.db')

# Email setup
app.config.update(
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME=MAIL_USERNAME,
    MAIL_PASSWORD=MAIL_PASSWORD,
    MAIL_DEFAULT_SENDER=MAIL_USERNAME
)
mail = Mail(app)

@app.template_filter('datetimeformat')
def datetimeformat(value):
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M").strftime("%I:%M %p, %d-%b-%Y")
    except:
        return value

# Background task reminder
def task_ringtone_checker():
    while True:
        try:
            with open('database/tasks.json', 'r') as f:
                tasks = json.load(f)
        except:
            tasks = []

        now = datetime.now().strftime('%Y-%m-%d %H:%M')
        for task in tasks:
            task_time = f"{task['date']} {task['time']}"
            if now == task_time:
                print(f"🔔 Task Reminder: {task['title']}")
                try:
                    pygame.mixer.init()
                    pygame.mixer.music.load("static/ringtone.mp3")
                    pygame.mixer.music.play()
                    while pygame.mixer.music.get_busy():
                        time.sleep(1)
                except Exception as e:
                    print("Ringtone error:", e)
        time.sleep(30)

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Allow login by name OR email
        c.execute("SELECT * FROM users WHERE (name=? OR email=?) AND password=?", (username, username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = username
            flash(f"Welcome {username}!", "success")
            return redirect(url_for('dashboard'))
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html')

@app.route('/reset_request', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email'].strip()
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=?", (email,))
        user = c.fetchone()
        conn.close()

        if user:
            return render_template('reset_password.html', email=email)
        else:
            flash("Email not found!", "danger")
    return render_template('reset_request.html')

@app.route('/reset', methods=['POST'])
def reset():
    email = request.form['email']
    new_password = request.form['password']
    confirm = request.form['confirm']

    if new_password == confirm:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("UPDATE users SET password=? WHERE email=?", (new_password, email))
        conn.commit()
        conn.close()
        return render_template('reset_success.html')
    else:
        flash("Passwords do not match!", "danger")
        return render_template('reset_password.html', email=email)

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    alarms = get_all_alarms()

    if request.method == 'POST':
        if 'alarm_date' in request.form:
            if len(alarms) >= 10:
                flash("Maximum 10 alarms allowed!", "danger")
            else:
                date = request.form['alarm_date']
                hour = int(request.form['alarm_hour'])
                minute = int(request.form['alarm_minute'])
                ampm = request.form['alarm_ampm']
                if ampm == "PM" and hour != 12:
                    hour += 12
                if ampm == "AM" and hour == 12:
                    hour = 0
                alarm_time = f"{date}T{hour:02}:{minute:02}"
                message = request.form['message']
                threading.Thread(target=set_alarm, args=(alarm_time, message)).start()
                flash("Alarm set!", "success")

        elif 'task_title' in request.form:
            title = request.form['task_title']
            date = request.form['task_date']
            hour = int(request.form['task_hour'])
            minute = int(request.form['task_minute'])
            ampm = request.form['task_ampm']
            note = request.form.get('task_note', '')
            if ampm == 'PM' and hour != 12:
                hour += 12
            if ampm == 'AM' and hour == 12:
                hour = 0
            task_time = f"{hour:02}:{minute:02}"
            add_task(title, date, task_time, note)
            flash("Task added!", "success")

        alarms = get_all_alarms()

    tasks = get_upcoming_tasks()
    return render_template('dashboard.html', name=session['user'], tasks=tasks, alarms=alarms)

@app.route('/clear_tasks', methods=['POST'])
def clear_tasks():
    with open('database/tasks.json', 'w') as f:
        json.dump([], f)
    flash("All tasks cleared.", "info")
    return redirect(url_for('dashboard'))

@app.route('/clear_alarms', methods=['POST'])
def clear_alarms():
    with open('database/alarms.json', 'w') as f:
        json.dump([], f)
    flash("All alarms cleared.", "info")
    return redirect(url_for('dashboard'))

@app.route('/chatbot')
def chatbot():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('chatbot.html')

@app.route('/chat', methods=['POST'])


def chat():
    user_msg = request.json.get('message')  # 👈 JSON input from frontend

    print("🟡 Message received:", user_msg)

    if not user_msg:
        return jsonify({'reply': "❌ No message received."})

    reply = get_bot_response(user_msg)
    print("🟢 NeoMind reply:", reply)

    return jsonify({'reply': reply})  # 👈 returns response back to frontend


@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out.", "info")
    return redirect(url_for('login'))

if __name__ == '__main__':
    threading.Thread(target=task_ringtone_checker, daemon=True).start()
    app.run(debug=True)


