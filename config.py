# config.py

# ----------------- Flask Mail Configuration -----------------

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True

# 🔐 Your Gmail address (used to send reset emails)
MAIL_USERNAME = 'your_email@gmail.com'

# 🔐 App password generated from your Google Account (not your real password)
MAIL_PASSWORD = 'your_16_character_app_password'

# 📩 Default sender for outgoing emails
MAIL_DEFAULT_SENDER = MAIL_USERNAME
