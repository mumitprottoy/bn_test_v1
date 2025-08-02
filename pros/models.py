from django.db import models
from django.contrib.auth import get_user_model
from brands.models import Brand

User = get_user_model()

class ProPlayer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    @property
    def sponsors_list(self) -> list[dict]:
        return [sponsor.brand.details for sponsor in self.sponsors.all()]
    
    @property
    def social_links(self) -> list[dict]:
        return [social.details for social in self.socials.all()]
    
    def __str__(self) -> str:
        return f'{self.user.username} ({self.user.email})'


class Sponsors(models.Model):
    pro_player = models.ForeignKey(
        ProPlayer, on_delete=models.CASCADE, related_name='sponsors')
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='sponsoredplayers')
    
    def __str__(self) -> str:
        return f'{self.brand.__str__()} ➝ {self.pro_player.__str__()}'
    
    class Meta:
        verbose_name_plural = 'Sponsors'
        constraints = [
            models.UniqueConstraint(
                fields=('pro_player', 'brand'),
                name='unique_sponsor_player_pair'
            )
        ]


class Social(models.Model):
    name = models.CharField(max_length=30, unique=True)
    logo = models.URLField(max_length=500)

    def __str__(self) -> str:
        return self.name


class SocialLink(models.Model):
    pro = models.ForeignKey(
        ProPlayer, on_delete=models.CASCADE, related_name='socials')
    social = models.ForeignKey(Social, on_delete=models.CASCADE)
    url = models.URLField(max_length=500)

    @property
    def details(self) -> dict:
        return dict(
            pro_player_id=self.pro.id,
            social_link_id=self.id,
            social_id=self.social.id,
            social=self.social.name,
            logo=self.social.logo,
            url=self.url
        )

    def __str__(self) -> str:
        return f'{self.pro.__str__()} [{self.social.name}]'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('pro', 'social', 'url'),
                name='unique_social'
            )
        ]

class ProPlayerRotator(models.Model):
    last_pro = models.ForeignKey(ProPlayer, on_delete=models.CASCADE)

    @classmethod
    def get_default(cls) -> 'ProPlayerRotator':
        if cls.objects.count() > 0:
            return cls.objects.first()
        return cls.objects.create(last_pro=ProPlayer.objects.first())
    
    @classmethod
    def get_current_pro(cls) -> ProPlayer:
        pros = list(ProPlayer.objects.all())
        rotator = cls.get_default()
        index_of_last = pros.index(rotator.last_pro)
        current_pro = pros[(index_of_last + 1) % pros.__len__()]
        rotator.last_pro = current_pro; rotator.save()
        return current_pro
