from datetime import timedelta

from rest_framework.serializers import ValidationError


def validate_reward_and_linked_habit(reward, linked_habit):
    """Нельзя заполнять одновременно reward и linked_habit"""
    if reward and linked_habit:
        raise ValidationError(
            "Нельзя указать одновременно вознаграждение и связанную привычку"
        )


def validate_duration(duration):
    """Время выполнения должно быть не больше 120 секунд"""
    if duration > timedelta(seconds=120):
        raise ValidationError("Время выполнения не может превышать 120 секунд")


def validate_linked_habit(linked_habit, is_pleasant):
    """В связанные привычки могут попадать только привычки с признаком приятной привычки"""
    if linked_habit and not linked_habit.is_pleasant:
        raise ValidationError(
            "В связанные привычки можно добавлять только приятные привычки"
        )


def validate_pleasant_habit(is_pleasant, reward, linked_habit):
    """У приятной привычки не может быть вознаграждения или связанной привычки"""
    if is_pleasant and (reward or linked_habit):
        raise ValidationError(
            "У приятной привычки не может быть вознаграждения или связанной привычки"
        )


def validate_periodicity(periodicity):
    """Нельзя выполнять привычку реже, чем 1 раз в 7 дней"""
    if periodicity < 1 or periodicity > 7:
        raise ValidationError("Периодичность должна быть от 1 до 7 дней")
