from celery import shared_task
from django.utils import timezone  # оставить только этот

from config.celery import app
from tg.models import TgUser
from tg.services import send_telegram_message

from .models import Habit


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Проверяем каждую минуту
    sender.add_periodic_task(
        60.0, send_habit_reminders.s(), name="check habits every minute"
    )


@shared_task
def send_habit_reminders():
    """Отправка напоминаний о привычках"""
    now = timezone.now()
    current_time = now.time()

    # Ищем привычки, которые нужно выполнить сейчас
    habits = Habit.objects.filter(
        time__hour=current_time.hour, time__minute=current_time.minute
    )

    for habit in habits:
        user = habit.user
        # Ищем подтвержденные Telegram аккаунты пользователя
        tg_users = TgUser.objects.filter(user=user, verified=True)

        message = f"🔔 Напоминание!\nМесто: {habit.place}\nДействие: {habit.action}"

        for tg_user in tg_users:
            send_telegram_message(tg_user.chat_id, message)

    return f"Отправлено напоминаний: {habits.count()}"
