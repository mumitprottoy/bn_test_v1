import random
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings
from django.core import validators
from utils import subroutines as sr


class LevelXPMapping(models.Model):
    max_xp = models.IntegerField(unique=True)
    level = models.IntegerField(unique=True)
    card_theme_color = models.CharField(
        max_length=20, default='#8db85a', 
        help_text='put in color name in lowercase e.g. blue. \
            Also takes hex e.g #8db85a or rgb e.g rgb(120, 200, 50)'
        )

    class Meta:
        verbose_name_plural = 'Level-XP Mapping'

    def __str__(self):
        return f"Level {self.level} (≤ {self.max_xp} XP)"


def forbidden_word_validator(value):
    forbidden_words = ['organic']
    if value.lower() in forbidden_words:
        raise ValidationError(f"Using '{value}' is not allowed.")


class User(AbstractUser):
    email = models.EmailField(unique=True)
    profile_picture_url = models.URLField(
        max_length=500, default='https://profiles.bowlersnetwork.com/default-profile-pic.png')
    cover_photo_url = models.URLField(
        max_length=500, default='https://profiles.bowlersnetwork.com/default-cover.png')
    xp = models.IntegerField(default=0)

    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    username = models.CharField(
        max_length=20,
        unique=True,
        validators=[forbidden_word_validator],
    )

    @property
    def minimal(self) -> dict:
        return dict(
            user_id=self.id,
            username=self.username,
            name=self.get_full_name(),
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            profile_picture_url=self.profile_picture_url,
        )
    
    @property
    def basic(self) -> dict:
        basic_info = self.minimal.copy()
        basic_info.update(dict(
            intro_video_url=self.introvideo.url,
            cover_photo_url=self.cover_photo_url,
            xp=self.xp,
            level=self.level,
            card_theme = self.card_theme
        ))
        return basic_info

    def get_current_mapping(self) -> LevelXPMapping:
        mapping = LevelXPMapping.objects.filter(max_xp__lte=self.xp).order_by('-max_xp').first()
        if mapping is not None: 
            return mapping
        return LevelXPMapping.objects.first()
            
    @property
    def level(self) -> int:
        return self.get_current_mapping().level
    
    @property
    def card_theme(self):
        return self.get_current_mapping().card_theme_color
    
    @property
    def details(self) -> dict:
        return sr.get_clean_dict(self)
        
    def __str__(self):
        return f"{self.username} ({self.email})"


# class Team(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     created_by = models.ForeignKey('User', on_delete=models.CASCADE, related_name='created_teams', default=1)
#     members = models.ManyToManyField('User', related_name='teams', blank=True)

#     def __str__(self):
#         return f"{self.name} (created by {self.created_by.username})"


# class TeamInvitation(models.Model):
#     team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invitations')
#     invited_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='invitations')
#     status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted')], default='pending')

#     def __str__(self):
#         return f"{self.invited_user.username} → {self.team.name} [{self.status}]"


class Statistics(models.Model):
    is_added = models.BooleanField(default=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='stats')
    average_score = models.FloatField(default=0.0)
    high_game = models.IntegerField(default=0)
    high_series = models.IntegerField(default=0)
    experience = models.IntegerField(default=0, help_text='Years (at least 0)', validators=[validators.MinValueValidator(0)])

    def __str__(self):
        return f"{self.user.username}'s Stats"


class XPMap(models.Model):
    trigger_codename = models.CharField(max_length=20, unique=True, help_text='e.g. onboarding', default='')
    trigger_detail = models.CharField(max_length=200, help_text='e.g.on boarding a user', default='')
    xp_worth = models.IntegerField(default=1, 
        help_text='Must be greater than zero!', validators=[validators.MinValueValidator(1)])
    
    def __str__(self):
        return f'{self.trigger_codename} : {self.xp_worth} XP'
    
    
class XPLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='xplogs')
    xp_map = models.ForeignKey(XPMap, on_delete=models.CASCADE)
    gained_xp = models.IntegerField(default=0)
    gained_at = models.DateTimeField(auto_now_add=True)
    
    def title_str(self):
        return f'{self.user.username} gained +{self.gained_xp} for {self.xp_map.trigger_detail}'
         
    def title_html(self):
        return f'<span>Gained <span style="color:green">+{self.gained_xp}</span> for <b>{self.xp_map.trigger_detail}.</b>'
    
    def __str__(self):
        return self.title_str()