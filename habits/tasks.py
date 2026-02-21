from celery import shared_task
from django.utils import timezone

from tg.models import TgUser
from tg.services import send_telegram_message

from .models import Habit


@shared_task
def send_habit_reminders():
    """Отправка напоминаний о привычках"""
    now = timezone.now()
    current_time = now.time()

    # Ищем привычки, которые нужно выполнить сейчас
    habits = Habit.objects.filter(
        time__hour=current_time.hour, time__minute=current_time.minute
    )

    sent_count = 0
    for habit in habits:
        user = habit.user
        # Ищем подтвержденные Telegram аккаунты пользователя
        tg_users = TgUser.objects.filter(user=user, verified=True)

        message = f"🔔 Напоминание!\nМесто: {habit.place}\nДействие: {habit.action}"

        for tg_user in tg_users:
            result = send_telegram_message(tg_user.chat_id, message)
            if result and result.get("ok"):
                sent_count += 1

    return f"Отправлено напоминаний: {sent_count} для {habits.count()} привычек"
