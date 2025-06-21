from .libs import *
from player.models import Statistics
from utils import subroutines as sr


class StatsAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        Statistics.objects.filter(
            user=request.user).update(**request.data)
        return Response(sr.get_clean_dict(request.user.stats), status=status.HTTP_200_OK)
    
    def get(self, request: Request) -> Response:
        return Response(sr.get_clean_dict(request.user.stats), status=status.HTTP_200_OK)