from django.db.models import Prefetch, OuterRef, Subquery
from chat.models import Room, RoomMate, MessageMetaData
from teams.models import Team


class ChatService:
    def __init__(self, user):
        self.user = user
        self.rooms = None
        self.message_map = {}

    def get_all_rooms(self):
        latest_msg_subquery = MessageMetaData.objects.filter(
            room=OuterRef('pk')
        ).order_by('-sent_at').values('id')[:1]

        self.rooms = Room.objects.prefetch_related(
            Prefetch('mates', queryset=RoomMate.objects.select_related('user'))
        ).annotate(
            last_msg_id=Subquery(latest_msg_subquery)
        ).filter(
            mates__user=self.user
        ).distinct()

        last_msg_ids = [room.last_msg_id for room in self.rooms if room.last_msg_id]
        messages = MessageMetaData.objects.filter(id__in=last_msg_ids).prefetch_related(
            'mediacontents'
        ).select_related('sender', 'textcontent', 'room')
        self.message_map = {msg.id: msg for msg in messages}

        team_names = [room.name for room in self.rooms if room.room_type == Room.GROUP]
        teams = {t.name: t for t in Team.objects.filter(name__in=team_names)}

        result = {"private": [], "group": []}
        for room in self.rooms:
            last_message = self.message_map.get(room.last_msg_id)
            if room.room_type == Room.GROUP and room.name in teams:
                team = teams[room.name]
                info = dict(
                    display_name=team.name,
                    display_image_url=team.logo_url,
                    last_message=last_message.details_for_user(self.user) if last_message else None
                )
                result["group"].append(info)
            else:
                for mate in room.mates.all():
                    if mate.user != self.user:
                        info = dict(
                            display_name=mate.user.username,
                            display_image_url=mate.user.profile_picture_url,
                            last_message=last_message.details_for_user(self.user) if last_message else None
                        )
                        result["private"].append(info)
                        break
        return result

    def get_room_messages(self, room):
        messages = MessageMetaData.objects.filter(room=room).prefetch_related(
            'mediacontents'
        ).select_related('sender', 'textcontent')
        return [msg.details_for_user(self.user) for msg in messages]
