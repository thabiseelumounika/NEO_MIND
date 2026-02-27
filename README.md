# NEO_MIND


NeoMind is a personalized AI assistant built with Flask, SQLite, and Ollama. It features a task planner, alarm system, and an integrated chatbot.

## ✨ Features
- **Smart Chatbot**: Integrated with local LLMs via Ollama.
- **Task Planner**: Add and manage upcoming tasks.
- **Alarm System**: Set custom alarms with audio notifications.
- **Secure Login**: Simple authentication for personalized sessions.

## 🛠️ Requirements
- Python 3.11+
- [Ollama](https://ollama.com/) (running locally)
- Python packages: `flask`, `flask-mail`, `pygame`, `requests`

## 🚀 Installation

1. **Clone or Download** the project files.
2. **Install Dependencies**:
   ```bash
   pip install flask flask-mail pygame requests
   ```
3. **Set Up Ollama**:
   Ensure Ollama is running and you have the `phi3:latest` model pulled:
   ```bash
   ollama pull phi3:latest
   ```

## ⚙️ Setup & Configuration

1. **Initialize Database**:
   Run the database creation script to set up the `users` table and a test user.
   ```bash
   python create_db.py
   ```
2. **Configure Email**:
   Update `config.py` with your Gmail address and 16-character App Password if you intend to use the password reset feature.

## 🏁 Running the App

Always run the application from the `NeoMind` subdirectory to ensure correct file path resolution:

```bash
cd NeoMind
python app.py
```

### 👤 Test Credentials
- **Username or Email**: `Mounika`
- **Password**: `123456`

## 🔧 Recent Fixes & Optimizations
- **Model Choice**: Optimized to use `phi3:latest` for better response times.
- **Timeout**: Increased chatbot timeout to 60 seconds to support complex queries.
- **Login**: Simplified login flow to accept either username or email.
