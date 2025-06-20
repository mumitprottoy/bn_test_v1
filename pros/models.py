from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProPlayer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username
