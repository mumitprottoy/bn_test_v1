from .libs import *
from chat import models, engine
from utils import error_messages


class RoomsAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def initial(self, request: Request, *args, **kwargs) -> None:
        super().initial(request, *args, **kwargs)
        self.engine = engine.ChatEngine(request.user)

    def get(self, request: Request) -> Response:
        return Response(self.engine.get_all_rooms())
    
    def post(self, request: Request) -> Response:
        other_user = User.objects.filter(username=request.data.get('other_username')).first()
        if other_user is None:
            return Response(dict(error='User does not exist'), status=status.HTTP_404_NOT_FOUND)
        room_info = self.engine.get_or_create_private_room(other_user)
        return Response(room_info)


class ChatMessagesAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def initial(self, request: Request, *args, **kwargs) -> None:
        super().initial(request, *args, **kwargs)
        room_id = kwargs['room_id']
        self.room = models.Room.objects.filter(id=room_id).first()
        self.engine = engine.ChatEngine(request.user)

        if self.room is None:
            raise exceptions.NotFound('Room not found')

        if not self.room.mates.filter(user=request.user).exists():
            raise exceptions.PermissionDenied(error_messages.NOT_ROOM_MATE)

    def get(self, request: Request, room_id: int) -> Response:
        messages = self.engine.get_room_messages(self.room)
        return Response(messages)
    
    def post(self, request: Request, room_id: int) -> Response:
        kwargs = dict()
        for k in request.data:
            kwargs[k] = request.data.get(k)
        if 'media_files' in kwargs:
            kwargs['media_files'] = request.FILES.getlist('media_files')
        message = self.engine.create_message(**kwargs)
        return Response(message)

