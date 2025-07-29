from django.db.models import Prefetch, OuterRef, Subquery
from django.core.files.uploadedfile import UploadedFile
from chat.models import Room, RoomMate, MessageMetaData, MessageTextContent, MessageMediaContent
from teams.models import Team
from cloud.engine import CloudEngine
from player.models import User


class ChatEngine:
    
    def __init__(self, user: User):
        self.user = user
        self.rooms = None
        self.message_map = {}
    
    def get_or_create_private_room(self, other_user: User) -> dict:
        common_room = (Room.objects.filter(room_type=Room.PRIVATE, mates__user=self.user)
                       & Room.objects.filter(room_type=Room.PRIVATE, mates__user=other_user))
        if common_room.exists():
            return common_room.first().display_info_for_user(self.user)
        else:
            room = Room.objects.create(room_type=Room.PRIVATE)
            for user in (self.user, other_user):
                RoomMate.objects.create(room=room, user=user)
            return room.display_info_for_user(self.user)


    def get_all_rooms(self) -> dict[str, list]:
        rooms = Room.objects.filter(mates__user=self.user)
        private = [room.display_info_for_user(self.user) for room in rooms.filter(
                room_type=Room.PRIVATE)]
        group = [room.display_info_for_user(self.user) for room in rooms.filter(
                room_type=Room.GROUP)]
        return dict(
            private=sorted(private, key=lambda x: x['__last_activity']) if private.__len__() > 0 else private,
            group=sorted(group, key=lambda x: x['__last_activity']) if group.__len__() > 0 else group
        )

    def get_room_messages(self, room: Room) -> list[dict]:
        messages = MessageMetaData.objects.filter(room=room).prefetch_related(
            'mediacontents'
        ).select_related('sender', 'textcontent')
        return [msg.details_for_user(self.user) for msg in messages]
    
    def create_message(
            self, room: Room, text: str | None=None, media: list[UploadedFile] | None=None) -> dict | None:
        if text or media:
            metadata = MessageMetaData.objects.create(room=room, sender=self.user)
            
            if text is not None:
                MessageTextContent.objects.create(metadata=metadata, text=text)
            
            if media is not None:
                for file in media:
                    cloud_engine = CloudEngine(file, 'chat')
                    pub_url = cloud_engine.upload()
                    
                    if pub_url is not None:
                        MessageMediaContent.objects.create(metadata=metadata, url=pub_url)
            
            return metadata.details_for_user(self.user)

