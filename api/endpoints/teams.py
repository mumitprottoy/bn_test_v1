from .libs import *
from teams import models


class TeamsAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(dict(my_teams=[
          member.team.details for member in models.TeamMember.objects.filter(
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
            dict(error='Team with name already exists'), 
            status=status.HTTP_400_BAD_REQUEST
        )


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
        return Response(dict(
            invitations=[invitation.details 
                for invitation in models.TeamInvitation.objects.filter(
                    invited_user=request.user, is_accepted=False          
                )]
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

  