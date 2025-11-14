from .libs import *
from tournaments.models import Tournamant, TournamentV0, ParticipantSet, ParticipantMember
from teams.models import Team
from django.utils.dateparse import parse_datetime
from centers.models import CenterAdmin


class TournamentsAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        center_admin = CenterAdmin.objects.get(user=request.user)
        tournaments = [t.details for t in Tournamant.objects.filter(host=center_admin.center)]
        return Response(tournaments)

    def post(self, request: Request) -> Response:
        tournament = Tournamant(**request.data)
        tournament.start_date = parse_datetime(tournament.start_date)
        tournament.reg_deadline = parse_datetime(tournament.reg_deadline)
        center_admin = CenterAdmin.objects.get(user=request.user)
        tournament.host = center_admin.center
        tournament.save()
        return Response(tournament.details)


class UploadTournamentBannerByIDAPI(views.APIView):
    pass 


class AllTournamentsAPI(views.APIView):

    def get(self, request: Request) -> Response:
        tournaments = [t.details for t in Tournamant.objects.all()]
        return Response(tournaments)


class AddSinglesMemberAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, tournament_id: int, user_id: int) -> Response:
        tournament = Tournamant.objects.filter(id=tournament_id).first()
        if tournament is not None:
            user = User.objects.filter(id=user_id).first()
            if user is not None:
                if tournament.format == 'Singles':
                    part_set = ParticipantSet.objects.create(
                        tournament=tournament, name=user.get_full_name(), profile_picture=user.profile_picture_url)
                    ParticipantMember.objects.create(participant_set=part_set, user=user)
                    return Response(part_set.details)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class AddTeamsMemberAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, tournament_id: int, team_id: int) -> Response:
        tournament = Tournamant.objects.filter(id=tournament_id).first()
        if tournament is not None:
            team = Team.objects.filter(id=team_id).first()
            if team is not None:
                if tournament.format != 'Singles':
                    part_set = ParticipantSet.objects.create(
                        tournament=tournament,
                        name=team.name,
                        profile_picture=team.logo_url
                    )
                    for member in team.members.all():
                        ParticipantMember.objects.create(
                            participant_set=part_set,
                            user=member.user
                        )
                    return Response(part_set.details)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TournamentAllTeamsAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, tournament_id: int) -> Response:
        tournament = Tournamant.objects.filter(id=tournament_id).first()
        if tournament is not None:
            return Response(tournament.all_teams)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TournamentsV0API(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response([t.details for t in TournamentV0.objects.filter(
            director_user_id=request.user.id).order_by('-id')])

    def post(self, request: Request) -> Response:
        import json
        from tournaments.models import TournamentV0
        data = json.dumps(
            dict(request.data), indent=4, ensure_ascii=False)
        tournament = TournamentV0.objects.create(
            director_name=request.user.get_full_name(),
            director_user_id=request.user.id,
            data=data
        )
        return Response(tournament.details)


class TournamentV0FlyerUploadAPI(views.APIView):
    pass 


class TournamentsV0DeleteAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request: Request, tournament_id: int) -> Response:
        TournamentV0.objects.get(id=tournament_id).delete()
        return Response()
        