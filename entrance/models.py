from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class OnBoarding(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='myonboarding')
    channel = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pulls', null=True, default=None)
    
    @property
    def is_organic(self) -> bool:
        return self.channel is None
    
    def __str__(self):
        c = self.channel.username if not self.is_organic else 'organic'
        return f'{self.user.username} | Channel: {c}'
    
