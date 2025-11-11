from django.db import models
from utils.keygen import KeyGen
from pros.models import User, ProPlayer
from emailsystem.engine import EmailEngine


def get_key() -> str:
    return KeyGen().timestamped_alphanumeric_id()


class ProsOnboarding(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_onboard = models.BooleanField(default=False)
    private_key = models.CharField(
        max_length=100, default=get_key, unique=True)

    def onboard(self) -> None:
        self.is_onboard = True
        self.save()
    
    def setup_account(self, username: str, password: str) -> ProPlayer:
        user = User.objects.create(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            username=username,
        )
        user.set_password(password)
        return ProPlayer.objects.create(user=user)
    
    @property
    def __private_url(self) -> str:
        return f'https://onboarding.bowlersnetwork.com/pros/onboarding/{self.private_key}'
    
    def send_private_url(self) -> None:
        engine = EmailEngine(
            [self.email],
            'Setup Your BowlersNetwork Pro Account',
            'email/pros_onboarding.html',
            {'full_name': f'{self.__str__()}',}
        )
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
