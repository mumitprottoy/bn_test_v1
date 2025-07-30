from django.db import models
from django.contrib.auth import get_user_model
from pros.models import ProPlayer, ProRotator

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
    

class PreRegistration(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    onboarded_by = models.ForeignKey(ProPlayer, on_delete=models.DO_NOTHING, null=True, default=None)

    def save(self, *args, **kwargs) -> None:
        if self._state.adding:
            last_pre = self.__class__.objects.last()
            last_pro = last_pre.onboarded_by if last_pre is not None else None
            rotator = ProRotator(last_pro)
            self.onboarded_by = rotator.get_current_pro()
        else:
            pre_registration = self.__class__.objects.get(id=self.id)
            if self.onboarded_by != pre_registration.onboarded_by:
                raise ValueError('Cannot change pro player')
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} onboarded by {self.onboarded_by.user.get_full_name()}'
