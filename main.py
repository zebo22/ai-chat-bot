import os
import time
import requests

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")

TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

def get_ai_reply(text):
    try:
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "user", "content": text}
                ]
            },
            timeout=30
        )
        data = response.json()
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("AI error:", e)
        return "AI error."

def main():
    last_update_id = None
    print("Bot is alive. Send me a message.")

    while True:
        updates = requests.get(
            f"{TELEGRAM_API}/getUpdates",
            params={"offset": last_update_id, "timeout": 30}
        ).json()

        for update in updates.get("result", []):
            last_update_id = update["update_id"] + 1
            message = update.get("message")
            if not message or "text" not in message:
                continue

            chat_id = message["chat"]["id"]
            text = message["text"]

            reply = get_ai_reply(text)

            requests.post(
                f"{TELEGRAM_API}/sendMessage",
                json={"chat_id": chat_id, "text": reply}
            )

        time.sleep(1)

if __name__ == "__main__":
    main()