from django.db import models
from django.contrib.auth import get_user_model
from sponsors.models import BusinessSponsor, Brand

User = get_user_model()

class ProPlayer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.username} ({self.user.email})'


class ProPlayerSponsor(models.Model):
    pro_player = models.ForeignKey(
        ProPlayer, on_delete=models.CASCADE, related_name='sponsors')
    sponsor = models.ForeignKey(
        BusinessSponsor, on_delete=models.CASCADE, related_name='proplayers')
    
    def __str__(self) -> str:
        return f'{self.sponsor.__str__()} ➝ {self.pro_player.__str__()}'
    
    class Meta:
        verbose_name_plural = 'Business sponsors'


class ProPlayerBrandSponsor(models.Model):
    pro_player = models.ForeignKey(
        ProPlayer, on_delete=models.CASCADE, related_name='brandsponsors')
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='proplayers')
    
    def __str__(self) -> str:
        return f'{self.brand.__str__()} ➝ {self.pro_player.__str__()}'
    
    class Meta:
        verbose_name_plural = 'Brand sponsors'