from django.db import models
from django.contrib.auth import get_user_model
from brands.models import Brand

User = get_user_model()

class ProPlayer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.user.username} ({self.user.email})'


class Sponsors(models.Model):
    pro_player = models.ForeignKey(
        ProPlayer, on_delete=models.CASCADE, related_name='sponsors')
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='sponsoredplayers')
    
    def __str__(self) -> str:
        return f'{self.brand.__str__()} ➝ {self.pro_player.__str__()}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('pro_player', 'brand'),
                name='unique_sponsor_player_pair'
            )
        ]
