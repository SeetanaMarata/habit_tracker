from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Habit
from .paginators import HabitPaginator
from .serializers import HabitSerializer, PublicHabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    pagination_class = HabitPaginator

    def get_queryset(self):
        """Пользователь видит только свои привычки"""
        if self.action == "public":
            return Habit.objects.all()  # для public метода queryset не используется
        return Habit.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """При создании привычки автоматически проставляем пользователя"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def public(self, request):
        """Список публичных привычек (доступно всем)"""
        habits = Habit.objects.filter(is_public=True)
        serializer = PublicHabitSerializer(habits, many=True)
        return Response(serializer.data)
