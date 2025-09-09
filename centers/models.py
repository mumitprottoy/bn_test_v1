from django.db import models
from player.models import User


class CenterAdmin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)


