from django.db import models
from player.models import User
from utils.subroutines import get_clean_dict
from utils import constants as const


class Center(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address_str = models.CharField(max_length=200, unique=True)
    lat = models.CharField(max_length=30)
    long = models.CharField(max_length=30)
    logo = models.URLField(max_length=500, default=const.DEFAULT_CENTER_LOGO)

    @property
    def details(self) -> dict:
        return get_clean_dict(self)
    
    def __str__(self) -> str:
        return self.name


class CenterAdmin(models.Model):
    center = models.OneToOneField(Center, on_delete=models.CASCADE, related_name='admin', null=True, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='centermanager')

    def __str__(self) -> str:
        return f'{self.center.name} : {self.user.get_full_name()}'