import requests

def get_bot_response(message):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:latest",
                "prompt": message,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "num_predict": 200
                }
            },
            timeout=60
        )

        if response.status_code == 200:
            # ✅ Return just the string (not a generator)
            return response.json().get("response", "").strip()
        else:
            return f"⚠️ Ollama error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"❌ Error: {e}"


