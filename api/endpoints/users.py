from .libs import *


class UserDataAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response([user.minimal for user in User.objects.all().exclude(id=request.user.id)])
    