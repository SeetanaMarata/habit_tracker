from datetime import timedelta

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from habits.models import Habit


@pytest.mark.django_db
class TestHabitAPI:
    def test_create_habit_authenticated(self):
        user = User.objects.create_user(username="testuser", password="12345")
        client = APIClient()
        client.force_authenticate(user=user)

        data = {
            "place": "Дом",
            "time": "12:00:00",
            "action": "Тестовая привычка",
            "duration": "00:01:00",
            "periodicity": 1,
        }

        response = client.post("/api/habits/", data, format="json")
        assert response.status_code == 201
        assert response.data["action"] == "Тестовая привычка"

    def test_create_habit_unauthenticated(self):
        client = APIClient()
        data = {
            "place": "Дом",
            "time": "12:00:00",
            "action": "Тестовая привычка",
            "duration": "00:01:00",
            "periodicity": 1,
        }
        response = client.post("/api/habits/", data, format="json")
        assert response.status_code == 401

    def test_list_own_habits(self):
        user = User.objects.create_user(username="testuser", password="12345")
        other_user = User.objects.create_user(username="other", password="12345")

        Habit.objects.create(
            user=user,
            place="Дом",
            time="12:00",
            action="Моя привычка",
            duration=timedelta(seconds=60),
            periodicity=1,
        )
        Habit.objects.create(
            user=other_user,
            place="Дом",
            time="12:00",
            action="Чужая привычка",
            duration=timedelta(seconds=60),
            periodicity=1,
        )

        client = APIClient()
        client.force_authenticate(user=user)
        response = client.get("/api/habits/")

        assert response.status_code == 200
        assert len(response.data["results"]) == 1
        assert response.data["results"][0]["action"] == "Моя привычка"

    def test_public_habits_anonymous(self):
        user = User.objects.create_user(username="testuser", password="12345")
        Habit.objects.create(
            user=user,
            place="Парк",
            time="09:00",
            action="Публичная привычка",
            duration=timedelta(seconds=60),
            periodicity=1,
            is_public=True,
        )

        client = APIClient()
        response = client.get("/api/habits/public/")

        assert response.status_code == 200
        assert len(response.data) == 1
        assert response.data[0]["action"] == "Публичная привычка"
