from .libs import *
from chat.models import Room


class RoomsAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        pass