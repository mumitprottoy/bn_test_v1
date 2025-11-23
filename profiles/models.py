import json
from datetime import datetime
from django.db import models
from player.models import User
from brands.models import Brand
from utils import constants as const, keygen
from emailsystem.engine import EmailEngine


class Nickname(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, default='')
    is_public = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.__str__()


class Bio(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='bio')    
    content = models.TextField(default='')

    def __str__(self) -> str:
        self.user.__str__()


class BirthDate(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='birth_date')
    date = models.DateField(null=True, blank=True, default=None)
    is_public = models.BooleanField(default=True)
    
    @property
    def date_str(self) -> str | None:
        if self.date is not None:
            return self.date.strftime(const.DATE_STR_FORMAT_1)
    
    @property
    def age(self) -> int | None:
        if self.date is not None:
            today = datetime.today()
            age = today.year - self.date.year
            if (today.month, today.day) < (self.date.month, self.date.day):
                age -= 1
            return age

    def __str__(self) -> str:
        return self.user.__str__()


class Address(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='address', 
        null=True, blank=True, default=None)
    zip_code = models.CharField(max_length=15, null=True, default=None)
    address_str = models.TextField(default='')
    lat = models.CharField(max_length=50, default='')
    long = models.CharField(max_length=50, default='')
    
    class Meta:
        verbose_name_plural = 'User Address'
    
    def __str__(self) -> str:
        return self.user.__str__()
    

class AuthCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='codes')
    otp = models.CharField(max_length=6, default='') 
    verification_code = models.CharField(max_length=6, default='')
    is_email_verified = models.BooleanField(default=False)
    
    def __generate_code(self):
        kg = keygen.KeyGen()
        return kg.num_key(key_len=6)
    
    def change_otp(self):
        self.otp = self.__generate_code()
        self.save()
    
    def change_verification_code(self):
        self.verification_code = self.__generate_code()
        self.save()
    
    def send_otp(self):
        try:
            self.change_otp()
            engine = EmailEngine(
                recipient_list=[self.user.email],
                subject=f'Your OTP for BowlersNetwork [{self.otp}]',
                template='emails/otp.html',
                context=dict(code=self.otp)
            )
            engine.send()
            return True
        except: return False
    
    def send_verification_code(self):
        try:
            self.change_verification_code()
            # self.send_code('verification code')
            return True
        except: return False
    
    def verify_auth_code(self, code_type: str, code: str) -> bool:
        print(f'verifying: {self.__dict__[code_type]} == {code}')
        return self.__dict__[code_type] == code
        
    def verify_email(self, code: str) -> bool:
        if self.verify_auth_code('verification_code', code):
            self.is_email_verified = True; self.save()
            return True
        return False
    
    def verify_otp(self, code: str) -> bool:
        return self.verify_auth_code('otp', code)
    
    @classmethod
    def verify_email_before_login(cls, email: str, code: str) -> bool:
        user = User.objects.filter(email=email).first()
        if user is not None:
            return user.codes.verify_email(code)
        return False
    
    @classmethod
    def verify_otp_before_login(cls, email: str, code: str) -> bool:
        user = User.objects.filter(email=email).first()
        if user is not None:
            return user.codes.verify_otp(code)
        return False

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = self.__generate_code()
        if not self.verification_code:
            self.verification_code = self.__generate_code()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return self.user.__str__()


class Follow(models.Model):
    followed = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='followers')
    follower = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='following')
    
    @classmethod
    def get_followers(cls, user: User) -> models.QuerySet:
        follower_ids = [follow.follower.id for follow in cls.objects.filter(followed=user)]
        return User.objects.filter(id__in=follower_ids)
    
    def save(self, *args, **kwargs) -> None:
        # A user can't follow itself
        if self.followed == self.follower:
            raise ValueError('A user cannot follow itself')
        
        # Avoid follow pair duplication
        if self.__class__.objects.filter(
            follower=self.follower, followed=self.followed).exists():
            raise ValueError('Follow duplication')
        
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.followed.username} followed by {self.follower.username}'


class IntroVideo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    url = models.URLField(max_length=500, null=True, default=None)

    def __str__(self) -> str:
        return self.user.__str__()


class FavoriteBrand(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='favbrands')
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='targets')
    
    def __str__(self) -> str:
        return f'{self.brand.__str__()} ➝ {self.user.__str__()}'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'brand'),
                name='unique_user_brand_pair'
            )
        ]
