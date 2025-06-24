from django.db import models
from player.models import User


class Premium(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} ({self.user.email})' 
