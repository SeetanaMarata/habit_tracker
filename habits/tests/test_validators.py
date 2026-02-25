from datetime import timedelta

import pytest
from rest_framework.serializers import ValidationError

from habits.validators import (validate_duration, validate_periodicity,
                               validate_pleasant_habit,
                               validate_reward_and_linked_habit)


class TestValidators:
    def test_duration_valid(self):
        # 60 секунд - ок
        validate_duration(timedelta(seconds=60))

    def test_duration_invalid(self):
        # 121 секунда - не ок
        with pytest.raises(ValidationError):
            validate_duration(timedelta(seconds=121))

    def test_periodicity_valid(self):
        validate_periodicity(1)
        validate_periodicity(7)

    def test_periodicity_invalid(self):
        with pytest.raises(ValidationError):
            validate_periodicity(0)
        with pytest.raises(ValidationError):
            validate_periodicity(8)

    def test_reward_and_linked_habit(self):
        # Нельзя заполнить оба поля
        with pytest.raises(ValidationError):
            validate_reward_and_linked_habit("шоколадка", "связанная")

    def test_pleasant_habit_no_reward(self):
        # У приятной привычки не может быть награды
        with pytest.raises(ValidationError):
            validate_pleasant_habit(True, "шоколадка", None)
