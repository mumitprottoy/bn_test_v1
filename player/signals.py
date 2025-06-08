from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, Statistics, XPMap, XPLog
from entrance.models import OnBoarding


@receiver(post_save, sender=User)
def create_statistics(sender, instance, created, **kwargs):
    if created:
        Statistics.objects.create(user=instance)


@receiver(post_save, sender=OnBoarding)
def add_referral_xp(instance, created, **kwargs):
    if created and (instance.channel is not None):
        xp_type, created = XPMap.objects.get_or_create(
            trigger_codename='onboarding', trigger_detail='on boarding a user')
        if created:
            xp_type.xp_worth = 100
            xp_type.save()
        instance.channel.xp += xp_type.xp_worth
        XPLog.objects.create(
            user=instance.channel, xp_map=xp_type, gained_xp=xp_type.xp_worth)
        instance.channel.save()