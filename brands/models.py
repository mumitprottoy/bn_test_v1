from django.db import models


class BrandType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


class Brand(models.Model):
    brand_type = models.ForeignKey(BrandType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True)
    formal_name = models.CharField(max_length=100, unique=True)
    logo_url = models.URLField()

    def __str__(self) -> str:
        return f'{self.formal_name} ({self.brand_type.name})'


