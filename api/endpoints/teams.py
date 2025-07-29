from .libs import *
from teams import models
from cloud.engine import CloudEngine
from chat.models import Room


def get_team_details(team: models.Team) -> dict:
    team_details = team.details.copy()
    room = Room.objects.get(name=team.name, room_type=Room.GROUP)
    team_details['team_chat_room_id'] = room.id
    return team_details


class TeamsAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(dict(my_teams=[
          get_team_details(member.team) for member in models.TeamMember.objects.filter(
                user=request.user
            )
        ]), status=status.HTTP_200_OK)
    
    def post(self, request: Request) -> Response:
        team = models.Team.objects.filter(**request.data).first()

        if team is None:
            team = models.Team.objects.create(
                created_by=request.user, **request.data)
            return Response(team.details, status=status.HTTP_200_OK)
        
        return Response(
            dict(error='Team with same name already exists'), 
            status=status.HTTP_400_BAD_REQUEST
        )


class TeamMembersAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def initial(self, request: Request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        team_id = kwargs.get('team_id')
        self.team = models.Team.objects.filter(id=team_id).first()
        if not self.team:
            raise exceptions.NotFound(detail="Team not found")
        if not self.team.members.filter(user=request.user).exists():
            raise exceptions.PermissionDenied(detail='Members only')

    def get(self, request: Request, team_id: int) -> Response:
        team_details = get_team_details(self.team)
        team_details.update(dict(members=self.team.member_details))
        return Response(team_details, status=status.HTTP_200_OK)
    
    # leave group
    def post(self, request: Request, team_id: int) -> Response:
        self.team.members.filter(user=request.user).delete()
        return Response(dict(message='Left group successfully'), status=status.HTTP_200_OK)

    # remove a member
    def delete(self, request: Request, team_id: int) -> Response:
        member = self.team.members.filter(id=int(request.data['member_id'])).first()

        if member is not None and self.team.is_creator(request.user):
            member.delete()
            return Response(dict(message=f'Removed member successfully'), status=status.HTTP_200_OK)
        
        return Response(dict(error='Member not found'), status=status.HTTP_404_NOT_FOUND)


class TeamDeletionAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request: Request, team_id: int) -> Response:
        team = models.Team.objects.filter(
            id=team_id, created_by=request.user).first()
        
        if team is not None:
            team.delete()
            return Response(dict(message='Team successfully deleted'), status=status.HTTP_200_OK)
        
        return Response(dict(error='Not authorized'), status=status.HTTP_401_UNAUTHORIZED)


class TeamInviteSendingAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        team = models.Team.objects.filter(
            id=int(request.data['team_id'])).first()
        invited_user = models.User.objects.filter(
            id=int(request.data['invited_user_id'])).first()
        
        if team is None:
            return Response(
                dict(error='Invalid team ID'), status=status.HTTP_400_BAD_REQUEST)
        if invited_user is None:
            return Response(
                dict(error='Invalid user ID'), status=status.HTTP_400_BAD_REQUEST)
        if models.TeamInvitation.objects.filter(
            team=team, invited_user=invited_user, is_accepted=False).exists():
            return Response(
                dict(error='Already invited'), status=status.HTTP_400_BAD_REQUEST)
        if models.TeamMember.objects.filter(team=team, user=invited_user).exists():
            return Response(
                dict(error='Already a team member'), status=status.HTTP_400_BAD_REQUEST)
        
        models.TeamInvitation.objects.create(team=team, invited_user=invited_user)
        return Response(dict(message='Invitation sent'), status=status.HTTP_200_OK)


class UserTeamInvitationsAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        sent_invitations = list()

        for team in models.Team.objects.filter(created_by=request.user):
            for invitation in models.TeamInvitation.objects.filter(
                team=team, is_accepted=False):
                sent_invitations.append(invitation.details)

        return Response(dict(
            received=[invitation.details 
                for invitation in models.TeamInvitation.objects.filter(
                    invited_user=request.user, is_accepted=False          
                )],
            sent=sent_invitations
        ), status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        invitation = models.TeamInvitation.objects.filter(
            id=int(request.data['invitation_id']), invited_user=request.user, is_accepted=False).first()
        
        if invitation is not None:
            if request.data['is_accepted']:
                invitation.accept()
                return Response(dict(message='Invitation accepted'), status=status.HTTP_200_OK)
            else:
                invitation.delete()
                return Response(dict(message='Invitation declined'), status=status.HTTP_200_OK)
        
        return Response(dict(error='Invalid invitation'), status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request: Request) -> Response:
        invitation = models.TeamInvitation.objects.filter(
            id=int(request.data['invitation_id']), is_accepted=False).first()
        
        if invitation is not None and invitation.team.is_creator(request.user):
            invitation.delete()
            return Response(dict(message='Invitation deleted'))
        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class UploadTeamLogoAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def post(self, request: Request, team_name: str) -> Response:
        team = models.Team.objects.filter(name=team_name).first()
        if team is not None:
            if team.is_member(request.user):
                image = request.FILES.get('image')
                engine = CloudEngine(image, 'profiles')
                pub_url = engine.upload()
                if pub_url is not None:
                    team.logo_url = pub_url
                    team.save()
                return Response(team.details)
            return Response(dict(error='Unauthorised: not a member'), status=status.HTTP_401_UNAUTHORIZED)
        return Response(dict(error='Not found'), status=status.HTTP_404_NOT_FOUND)