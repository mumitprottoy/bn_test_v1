from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class ProPlayer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.username} ({self.user.email})'

