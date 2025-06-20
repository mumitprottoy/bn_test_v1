from .libs import *
from profiles.models import Follow

class PlayerProfileAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        profile = request.user.details
        profile.pop('password')
        profile['name'] = request.user.get_full_name()
        followers = [f.follower.details for f in Follow.objects.filter(followed=request.user)]
        profile['follower_count'] = followers.__len__()
        profile['followers'] = followers
        return Response(profile, status=status.HTTP_200_OK)
    # def post(self, request: Request) -> Response:
    #     User.objects.filter(username=request.user.username)
    