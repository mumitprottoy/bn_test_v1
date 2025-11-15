import json
from django.db import models
from player.models import User


class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    data = models.TextField()

    @property
    def details(self) -> dict:
        return dict(game_id=self.id, game_data=json.loads(self.data))
    
    @classmethod
    def get_all_games(cls: 'Game', user: User) -> list[dict]:
        return [g.details for g in cls.objects.filter(user=user).order_by('-id')]


