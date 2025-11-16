from django.db import models
from player.models import User
from utils.keygen import KeyGen

def get_key() -> str: return KeyGen().timestamped_alphanumeric_id(20)

class BetaTester(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    private_key=models.CharField(max_length=100, default=get_key)

    @classmethod
    def create(
        cls: 'BetaTester', first_name: str, last_name: str, email: str) -> 'BetaTester':
        created = False
        user = User.objects.filter(email=email)
        if user.exists():
            user.update(first_name=first_name, last_name=last_name)
            user=user.first()
        else:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=KeyGen().alphanumeric_key(20),
                email=email
            )
            created = True
            
        tester = cls.objects.create(user=user)
        if created:
            user.username = f'beta_tester_{tester.id}'
            user.save()
        
        return tester


