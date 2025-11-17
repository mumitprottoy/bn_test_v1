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
    def survey_completion(self) -> int:
        completion = 0
        user = User.objects.filter(email=self.email).first()
        if user is not None and hasattr(user, 'pro'):
            q_count = Questionnaire.objects.count()
            a_count = 0
            for ans in QuestionnaireAnswers.objects.filter(pro=user.pro):
                if ans.answer: a_count += 1
            completion = int((a_count / q_count) * 100) if q_count > 0 else 0
        return completion

    @property
    def details(self) -> dict:
        d = get_clean_dict(self)
        d['survey_completion'] = self.survey_completion
        return d

    def onboard(self) -> None:
        self.is_onboard = True
        self.save()
    
    def setup_account(self, username: str, password: str) -> ProPlayer:
        user_set = User.objects.filter(email=self.email)
        if user_set.exists():
            user_set.update(
            first_name=self.first_name,
            last_name=self.last_name,
            username=username    
            )
            user = user_set.first()
        else:
            user = User.objects.create(
                first_name=self.first_name,
                last_name=self.last_name,
                username=username,
                email=self.email,
            )
        user.set_password(password)
        self.onboard()
        return ProPlayer.objects.create(user=user)
    # please launch for me. I am sleepy and tired.
    
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

        engine.subject = 'Getting Started with Your BowlersNetwork Partner Access'
        engine.template = 'emails/pro_player_instructions.html'
        engine.context = {'full_name': f'{self.__str__()}'}
        engine.send()
    
    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'



class Questionnaire(models.Model):
    question = models.TextField()
    description = models.TextField()
    serial = models.IntegerField(default=-1)

    @property
    def details(self) -> dict:
        return dict(
                ques_id=self.id,
                serial=self.serial,
                question=self.question,
                description=self.description
            )

    @classmethod
    def sync_serial(cls: 'Questionnaire', serial: int) -> None:
        for q in cls.objects.filter(serial__gt=serial):
            q.serial = q.serial - 1
            q.save()    

    @classmethod
    def all_questions(cls: 'Questionnaire') -> list[dict]:
        return [q.details for q in cls.objects.all().order_by('serial')]

    def __str__(self) -> str:
        return self.question
    
    def save(self, *args, **kwargs) -> None:
        if self._state.adding and self.serial == -1:
            self.serial = self.__class__.objects.count() + 1
        super().save(*args, **kwargs)


class QuestionnaireAnswers(models.Model):
    pro = models.ForeignKey(ProPlayer, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    answer = models.TextField(default='')

    @property
    def details(self) -> dict:
        return dict(
            ans_id=self.id,
            question=self.questionnaire.question,
            description=self.questionnaire.description,
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
                fields=('pro', 'questionnaire'),
                name='unique_pro_questionnaire_pair'
            )
        ]
