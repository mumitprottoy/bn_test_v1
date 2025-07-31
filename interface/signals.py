from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from player.models import User
from profiles import models as profile_models
from teams.models import Team, TeamMember
from chat.models import Room, RoomMate
from entrance.models import PreRegistration
from emailsystem.engine import EmailEngine


@receiver(post_save, sender=User)
def add_birth_date(instance: User, created: bool, *args, **kwargs) -> None:
    user = instance
    if created:
        profile_models.BirthDate.objects.create(user=user)


@receiver(post_save, sender=Team)
def add_team_creator_as_member(instance: Team, created: bool, *args, **kwargs) -> None:
    team = instance
    if created:
        TeamMember.objects.create(team=team, user=team.created_by)


@receiver(post_delete, sender=Team)
def delete_chat_room(instance: Team, *args, **kwargs) -> None:
    name = instance.name
    room = Room.objects.filter(name=name, room_type=Room.GROUP)
    if room.exists(): room.delete()


@receiver(post_save, sender=Team)
def create_group_room(instance: Team, created: bool, *args, **kwargs) -> None:
    team = instance
    if created:
        Room.objects.get_or_create(name=team.name, room_type=Room.GROUP)


@receiver(post_save, sender=TeamMember)
def create_group_room_mates(instance: TeamMember, created: bool, *args, **kwargs) -> None:
    member = instance
    if created:
        room, _ = Room.objects.get_or_create(name=member.team.name, room_type=Room.GROUP)
        room.mates.get_or_create(user=member.user)

@receiver(post_save, sender=User)
def add_intro_video(instance: User, created: bool, *args, **kwargs) -> None:
    user = instance
    if created:
        profile_models.IntroVideo.objects.create(
            user=user, url='https://i.imgur.com/BnDntB8.mp4')


@receiver(post_save, sender=User)
def add_address(instance: User, created: bool, *args, **kwargs) -> None:
    user = instance
    if created:
        profile_models.Address.objects.create(user=user)


@receiver(post_save, sender=User)
def add_auth_code(instance: User, created: bool, *args, **kwargs) -> None:
    user = instance
    if created:
        profile_models.AuthCode.objects.create(user=user)


@receiver(post_save, sender=User)
def add_nickname(instance: User, created: bool, *args, **kwargs) -> None:
    user = instance
    if created:
        profile_models.Nickname.objects.create(user=user)


@receiver(post_save, sender=User)
def add_bio(instance: User, created: bool, *args, **kwargs) -> None:
    user = instance
    if created:
        profile_models.Bio.objects.create(user=user, content=f'Hi! I am {user.get_full_name()}.')


@receiver(post_save, sender=PreRegistration)
def send_pre_registration_conformation_email(instance: PreRegistration, created: bool, *args, **kwargs) -> None:
    pre = instance
    if created:
        engine = EmailEngine(
            recipient_list=[pre.email],
            subject='Pre-Registration Confirmed — Let’s Roll!',
            template='emails/pre_resgiter.html',
            context=dict(full_name=f'{pre.first_name} {pre.last_name}')
        )        
        engine.send()
