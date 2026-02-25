import random
import string

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import TgUser
from .serializers import TgUserSerializer
from .services import send_telegram_message


class TgUserViewSet(viewsets.ModelViewSet):
    serializer_class = TgUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TgUser.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Генерируем код подтверждения
        code = "".join(random.choices(string.digits, k=6))
        serializer.save(user=self.request.user, verification_code=code)

    @action(detail=True, methods=["post"])
    def verify(self, request, pk=None):
        """Подтверждение Telegram по коду"""
        tg_user = self.get_object()
        code = request.data.get("code")

        if tg_user.verification_code == code:
            tg_user.verified = True
            tg_user.verification_code = None
            tg_user.save()
            send_telegram_message(
                tg_user.chat_id,
                "✅ Ваш Telegram подтвержден! Теперь вы будете получать напоминания о привычках.",
            )
            return Response({"status": "verified"})
        return Response({"error": "Неверный код"}, status=status.HTTP_400_BAD_REQUEST)
