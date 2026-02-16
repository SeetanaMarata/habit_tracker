from rest_framework import serializers

from .models import Habit
from .validators import (
    validate_duration,
    validate_linked_habit,
    validate_periodicity,
    validate_pleasant_habit,
    validate_reward_and_linked_habit,
)


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = "__all__"
        read_only_fields = ("user",)

    def validate(self, attrs):
        """Применяем все валидаторы"""
        reward = attrs.get("reward")
        linked_habit = attrs.get("linked_habit")
        # duration = attrs.get("duration")
        is_pleasant = attrs.get("is_pleasant")
        periodicity = attrs.get("periodicity")

        if linked_habit:
            # Чтобы проверить is_pleasant у связанной привычки, нужно получить объект из БД
            if isinstance(linked_habit, Habit):
                linked_habit_obj = linked_habit
            else:
                linked_habit_obj = Habit.objects.get(pk=linked_habit)
            validate_linked_habit(linked_habit_obj, is_pleasant)

        validate_reward_and_linked_habit(reward, linked_habit)
        validate_pleasant_habit(is_pleasant, reward, linked_habit)
        validate_periodicity(periodicity)

        return attrs

    def validate_duration(self, value):
        """Отдельная валидация для duration"""
        validate_duration(value)
        return value


class PublicHabitSerializer(serializers.ModelSerializer):
    """Сериализатор только для публичных привычек (без проверки user)"""

    class Meta:
        model = Habit
        fields = [
            "id",
            "place",
            "time",
            "action",
            "is_pleasant",
            "periodicity",
            "duration",
            "linked_habit",
            "reward",
        ]
