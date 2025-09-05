import requests

from my_secrets import TELEGRAM_API_TOKEN, TELEGRAM_DEBUG_CHANNEL


def send_telegram_message(text: str):
    url: str = f"https://api.telegram.org/bot{TELEGRAM_API_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": TELEGRAM_DEBUG_CHANNEL, "text": text})

