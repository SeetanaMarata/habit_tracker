import requests
from django.conf import settings

TELEGRAM_URL = "https://api.telegram.org/bot"


def send_telegram_message(chat_id, text):
    """Отправка сообщения в Telegram"""
    token = settings.TELEGRAM_TOKEN
    url = f"{TELEGRAM_URL}{token}/sendMessage"
    data = {"chat_id": chat_id, "text": text}
    try:
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return None


def set_webhook():
    """Установка вебхука (если понадобится)"""
    token = settings.TELEGRAM_TOKEN
    webhook_url = f"{settings.SITE_URL}/tg/webhook/"  # настроим позже
    url = f"{TELEGRAM_URL}{token}/setWebhook"
    requests.post(url, json={"url": webhook_url})
