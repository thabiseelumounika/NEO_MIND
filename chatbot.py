# assistant/chatbot.py

import ollama

chat_history = []  # to maintain session-based memory

def get_bot_response(message):
    try:
        global chat_history
        chat_history.append({'role': 'user', 'content': message})
        
        response = ollama.chat(
            model='llama3',
            messages=chat_history,
            options={
                "temperature": 0.7,
                "num_predict": 60
            }
        )

        reply = response['message']['content'].strip()
        chat_history.append({'role': 'assistant', 'content': reply})
        return reply

    except Exception as e:
        return f"❌ Error: {e}"
