from rest_framework import generics, permissions, pagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from player.models import User
from chat.models import Room, RoomMate, MessageTextContent
from chat.serializers import RoomSerializer, MessageTextContentSerializer


class LatestMessagesPagination(pagination.PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data,
        })


class RoomListCreateView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [permissions.IsAuthenticated]


class MessageListView(generics.ListAPIView):
    serializer_class = MessageTextContentSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = LatestMessagesPagination

    def get_queryset(self):
        room_name = self.kwargs['room_name']
        room = get_object_or_404(Room, name=room_name)
        return MessageTextContent.objects.filter(metadata__room=room).order_by('-metadata__sent_at')

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data['results'] = list(reversed(response.data['results']))
        return response


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def get_or_create_private_room(request):
    target_username = request.GET.get('username')
    if not target_username:
        return Response({"detail": "Username query param is required."}, status=400)

    if target_username == request.user.username:
        return Response({"detail": "Cannot chat with yourself."}, status=400)

    try:
        target_user = User.objects.get(username=target_username)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=404)

    existing_room = (
        Room.objects.filter(room_type=Room.PRIVATE)
        .filter(mates__user=request.user)
        .filter(mates__user=target_user)
        .distinct()
        .first()
    )

    if existing_room:
        serializer = RoomSerializer(existing_room)
        return Response(serializer.data)

    new_room = Room.objects.create(room_type=Room.PRIVATE)
    RoomMate.objects.bulk_create([
        RoomMate(room=new_room, user=request.user),
        RoomMate(room=new_room, user=target_user),
    ])

    serializer = RoomSerializer(new_room)
    return Response(serializer.data)
