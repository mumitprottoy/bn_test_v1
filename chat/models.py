from django.db import models
from player.models import User
from utils import exceptions, error_messages
from teams.models import Team


class Room(models.Model):
    PRIVATE = 'Private'; GROUP = 'Group'
    ROOM_TYPE_CHOICES = ((PRIVATE, PRIVATE), (GROUP, GROUP))

    name = models.CharField(max_length=50, unique=True, default='')
    room_type = models.CharField(max_length=10, choices=ROOM_TYPE_CHOICES, default=PRIVATE)

    def display_info(self, for_user: User) -> dict | None:
        if self.mates.filter(user=for_user).exists():
            if self.room_type == self.GROUP:
                team = Team.objects.filter(name=self.name).first()
                return dict(
                    display_name=team.name, 
                    display_image_url=team.logo_url)
            for mate in self.mates.all():
                if mate.user != for_user:
                    return dict(
                        display_name=mate.user.username, 
                        display_image_url=mate.user.profile_picture_url)  
          
    def save(self, *args, **kwargs) -> None:
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

    def save(self, *args, **kwargs) -> None:
        if not RoomMate.objects.filter(
            room=self.room, user=self.sender).exists():
            raise exceptions.NotRoomMate(error_messages.NOT_ROOM_MATE)
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['sent_at']
    

class MessageTextContent(models.Model):
    metadata = models.ForeignKey(MessageMetaData, on_delete=models.CASCADE)
    text = models.TextField()


class MessageMediaContent(models.Model):
    metadata = models.ForeignKey(MessageMetaData, on_delete=models.CASCADE)
    url = models.URLField()
