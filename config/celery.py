import os

from celery import Celery
from celery.schedules import crontab

# Устанавливаем переменную окружения для настроек Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

# Загружаем конфигурацию из настроек Django
app.config_from_object("django.conf:settings", namespace="CELERY")

# Настраиваем периодические задачи
app.conf.beat_schedule = {
    "send-habit-reminders-every-minute": {
        "task": "habits.tasks.send_habit_reminders",
        "schedule": crontab(minute="*/1"),  # каждую минуту
    },
}

# Автоматически находим задачи в приложениях
app.autodiscover_tasks()
