from django.db import models


class League(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.CharField(max_length=100)
    entry_fee = models.IntegerField(default=0, help_text='In dollars ($)')
    