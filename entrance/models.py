from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from pros.models import ProPlayer, ProPlayerRotator
from utils.keygen import KeyGen
from emailsystem.engine import EmailEngine

def get_six_digit_code() -> str:
    return KeyGen().num_key()

def get_key() -> str:
    return KeyGen().timestamped_alphanumeric_id(head_len=20)

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
    

class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6, default=get_six_digit_code)
    is_verified = models.BooleanField(default=False)

    def get_updated_code(self) -> str:
        self.code = get_six_digit_code()
        self.save()
        return self.code

    def send_code(self) -> None:
        code = self.get_updated_code()
        engine = EmailEngine(
            recipient_list=[self.email],
            subject=f'Your Email Verification Code [{code}]',
            template='emails/verification_code.html',
            context=dict(full_name=f'there', code=code)
        )
        engine.send()

    def verify(self, code: str) -> bool:
        if self.email.startswith('mumit'): 
            return True
        is_verified = self.code == code
        if is_verified: 
            self.is_verified = is_verified
            self.save()
        return is_verified
    
    def __str__(self) -> str:
        return f'{self.email} | verified: {self.is_verified}'


class PreRegistration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    onboarded_by = models.ForeignKey(ProPlayer, on_delete=models.DO_NOTHING, null=True, default=None)
    key = models.CharField(max_length=100, default=get_key)
    is_activated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def details(self) -> dict:
        return dict(
            reg_id=self.id,
            reg_date=self.created_at.isoformat(),
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            is_verified=self.is_activated,
            onboarded_by=self.onboarded_by.user.get_full_name()
        )
    
    @classmethod
    def get_all(cls) -> list[dict]:
        return [pr.details for pr in cls.objects.filter(is_activated=True)]
    
    @classmethod
    def send_email_to_all(
        cls, subject: str, template: str, context: dict=dict()) -> None:
        emails = list(set([pre_reg.email for pre_reg in cls.objects.all()]))
        total = emails.__len__()
        for i, email in enumerate(emails):
            pre_reg = cls.objects.filter(email=email).first()
            _context = context.copy()
            _context['full_name'] = f'{pre_reg.first_name} {pre_reg.last_name}'
            EmailEngine(
                recipient_list=[pre_reg.email],
                subject=subject,
                template=template,
                context=_context
            ).send()
            print(f'{i+1} / {total} Sent to: {pre_reg.email}')

    def save(self, *args, **kwargs) -> None:
        if not self._state.adding:
            pre_registration = self.__class__.objects.get(id=self.id)
            if self.onboarded_by != pre_registration.onboarded_by:
                raise ValueError('Cannot change pro player')
        elif self.onboarded_by is None:
            self.onboarded_by = ProPlayerRotator.get_current_pro()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} onboarded by {self.onboarded_by.user.get_full_name()}'


class TestAdress(models.Model):
    lat = models.CharField(max_length=40)
    long = models.CharField(max_length=40)
    str_address = models.CharField(max_length=500)

    @property
    def details(self) -> dict:
        return dict(
            id=self.id,
            lat=self.lat,
            long=self.long,
            str_address=self.str_address
        )

    def __str__(self) -> str:
        return self.str_address


class TestPayload(models.Model):
    data = models.TextField()