from .libs import *
from tournaments.models import Tournamant
from django.utils.dateparse import parse_datetime


class TournamentsAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        tournaments = [t.details for t in Tournamant.objects.all()]
        return Response(tournaments)

    def post(self, request: Request) -> Response:
        tournament = Tournamant(**request.data)
        tournament.start_date = parse_datetime(tournament.start_date)
        tournament.reg_deadline = parse_datetime(tournament.reg_deadline)
        tournament.save()
        return Response(tournament.details)
    