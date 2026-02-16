from datetime import timedelta

import pytest
from django.contrib.auth.models import User

from habits.models import Habit


@pytest.mark.django_db
class TestHabitModel:
    def test_create_habit(self):
        user = User.objects.create_user(username="testuser", password="12345")
        habit = Habit.objects.create(
            user=user,
            place="Дом",
            time="12:00:00",
            action="Тестовая привычка",
            duration=timedelta(seconds=60),
            periodicity=1,
        )
        assert habit.id is not None
        assert str(habit) == "Тестовая привычка в 12:00:00"
