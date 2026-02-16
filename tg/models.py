from django.contrib.auth.models import User
from django.db import models


class TgUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tg_ids")
    chat_id = models.CharField(max_length=100, unique=True)
    verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.chat_id}"
