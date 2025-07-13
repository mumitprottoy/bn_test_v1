from rest_framework import generics, permissions
from chat.models import Room, MessageMetaData, MessageTextContent
from chat.serializers import RoomSerializer, MessageTextContentSerializer

class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]

class MessageListView(generics.ListAPIView):
    serializer_class = MessageTextContentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        room_id = self.kwargs['room_id']
        return MessageTextContent.objects.filter(metadata__room_id=room_id)
