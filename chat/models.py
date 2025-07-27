from django.db import models
from player.models import User
from utils import exceptions, error_messages, subroutines as sr, constants as const
from teams.models import Team


class Room(models.Model):
    PRIVATE = 'Private'; GROUP = 'Group'
    ROOM_TYPE_CHOICES = ((PRIVATE, PRIVATE), (GROUP, GROUP))

    name = models.CharField(max_length=50, unique=True, default='')
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, default=PRIVATE)

    def last_message_for_user(self, for_user: User) -> dict | None:
        last_message = self.messages.last()
        if last_message is not None:
            return last_message.details_for_user(for_user)

    def messages_for_user(self, for_user: User) -> list[dict]:
        return [msg.details_for_user(for_user) for msg in self.messages.all()]

    def display_info_for_user(self, for_user: User) -> dict | None:
        last_message = self.last_message_for_user(for_user)
        if self.mates.filter(user=for_user).exists():
            if self.room_type == self.GROUP:
                team = Team.objects.filter(name=self.name).first()
                return dict(
                    room_id=self.id,
                    name=self.name,
                    display_name=team.name, 
                    display_image_url=team.logo_url,
                    last_message=last_message
                )
            for mate in self.mates.all():
                if mate.user != for_user:
                    return dict(
                        room_id=self.id,
                        name=self.name,
                        display_name=mate.user.username, 
                        display_image_url=mate.user.profile_picture_url,
                        last_message=last_message
                    )
            return dict(
                    room_id=self.id,
                    name=self.name,
                    display_name=for_user.username, 
                    display_image_url=for_user.profile_picture_url,
                    last_message=last_message
                )
          
    def save(self, *args, **kwargs) -> None:
        if not self._state.adding:
            original_room_type = Room.objects.get(id=self.id).room_type
            if self.room_type != original_room_type:
                raise ValueError("Cannot change room type")
            
        if not self.name:
            from utils.keygen import KeyGen
            self.name = KeyGen().alphanumeric_key(50)
        
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class RoomMate(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='mates')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rooms')

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('room', 'user'),
                name='unique_room_mates'
            )
        ]
        indexes = [
            models.Index(fields=('room', 'user')),
            models.Index(fields=('user',))
        ]


class MessageMetaData(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='mymessages')
    sent_at = models.DateTimeField(auto_now_add=True)

    @property
    def time_datails(self) -> dict:
        return dict(
            sent_at=const.DATETIME_STR_FORMAT_1,
            timesince=sr.pretty_timesince(self.sent_at)
        )

    def details_for_user(self, for_user: User) -> dict:
        has_text_content = hasattr(self, 'textcontent')
        return dict(
            sentByMe=self.sender.id == for_user.id,
            roomID=self.room_id,
            sender=self.sender.minimal,
            timeDetails=self.time_datails,
            message=dict(
                textContent=self.textcontent.text if has_text_content else None),
                mediaContent=[content.url for content in self.mediacontents.all()]
        )

    def save(self, *args, **kwargs) -> None:
        if not RoomMate.objects.filter(
            room=self.room, user=self.sender).exists():
            raise exceptions.NotRoomMate(error_messages.NOT_ROOM_MATE)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['sent_at']
    

class MessageTextContent(models.Model):
    metadata = models.OneToOneField(
        MessageMetaData, on_delete=models.CASCADE, related_name='textcontent')
    text = models.TextField()


class MessageMediaContent(models.Model):
    metadata = models.ForeignKey(
        MessageMetaData, on_delete=models.CASCADE, related_name='mediacontents')
    url = models.URLField()
