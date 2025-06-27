from .libs import *
from profiles.models import Follow
from utils import subroutines as sr
from pros.models import ProPlayer


class PlayerProfileAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        profile = request.user.basic.copy()
        profile['is_pro'] = ProPlayer.objects.filter(user=request.user).exists()
        # followers = [f.follower.details for f in Follow.objects.filter(
        #     followed=request.user)]
        profile['follower_count'] = Follow.objects.filter(followed=request.user).count()
        # profile['followers'] = followers
        profile['stats'] = sr.get_clean_dict(request.user.stats)
        return Response(profile, status=status.HTTP_200_OK)
    