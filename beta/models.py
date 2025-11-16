from django.db import models
from player.models import User


class Tester(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    has_added_creds = models.BooleanField(default=False)
    private_key=models

