from rest_framework import serializers

from .models import TgUser


class TgUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TgUser
        fields = ["id", "chat_id", "verified"]
        read_only_fields = ["verified"]
