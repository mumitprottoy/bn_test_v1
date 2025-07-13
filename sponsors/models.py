from django.db import models


class BusinessSponsor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    formal_name = models.CharField(max_length=100, unique=True)
    logo_url = models.URLField()

    def __str__(self) -> str:
        return self.name