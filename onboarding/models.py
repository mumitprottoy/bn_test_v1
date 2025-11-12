from django.db import models
from utils.keygen import KeyGen
from pros.models import User, ProPlayer
from emailsystem.engine import EmailEngine
from utils.subroutines import get_clean_dict


def get_key() -> str:
    return KeyGen().timestamped_alphanumeric_id()


class ProsOnboarding(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_onboard = models.BooleanField(default=False)
    private_key = models.CharField(
        max_length=100, default=get_key, unique=True)
    is_notified = models.BooleanField(default=False)
    has_answered = models.BooleanField(default=False)

    @property
    def details(self) -> dict:
        return get_clean_dict(self)

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
        self.onboard()
        return ProPlayer.objects.create(user=user)
    
    @property
    def __private_url(self) -> str:
        return f'https://pros.bowlersnetwork.com/pros/onboarding/{self.private_key}'
    
    def send_private_url(self) -> None:
        engine = EmailEngine(
            [self.email],
            'Setup Your BowlersNetwork Pro Account',
            'emails/pros_onboarding.html',
            {'full_name': f'{self.__str__()}', 'private_url': self.__private_url}
        )
        engine.send()
        self.is_notified = True
        self.save()
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class QuestionnaireAnswers(models.Model):
    pro = models.ForeignKey(ProPlayer, on_delete=models.CASCADE)
    ques_id = models.IntegerField(default=-1)
    answer = models.TextField()

    @property
    def details(self) -> dict:
        return dict(
            question=self.question,
            description=self.description,
            answer=self.answer
        )
    
    @classmethod
    def all_answers_of_pro(
        cls: 'QuestionnaireAnswers', pro: ProPlayer) -> list[dict]:
        answers = [qa.details 
                for qa in QuestionnaireAnswers.objects.filter(pro=pro)]
        return dict(
            pro=cls.objects.filter(pro=pro).first().pro.user.minimal,
            answers=answers
        )
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('pro', 'ques_id'),
                name='unique_pro_ques_id_pair'
            )
        ]
