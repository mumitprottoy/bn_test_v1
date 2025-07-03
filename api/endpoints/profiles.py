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


class ProPlayersPublicProfileAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        users = [pro.user for pro in ProPlayer.objects.all() if pro.user.id != request.user.id]
        user_profiles = list()
        for user in users:
            profile = user.basic.copy()
            profile['is_pro'] = ProPlayer.objects.filter(user=user).exists()
            profile['follower_count'] = Follow.objects.filter(followed=user).count()
            profile['stats'] = sr.get_clean_dict(user.stats)
            profile['is_followed'] = Follow.objects.filter(
                followed=user, follower=request.user).exists()
            user_profiles.append(profile)  
        import random
        random.shuffle(user_profiles)
        return Response(user_profiles, status=status.HTTP_200_OK)


class UserProfileByID(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, user_id: int) -> Response:
        user = User.objects.filter(id=user_id)
        if user is not None:
            profile = user.basic.copy()
            profile['is_pro'] = ProPlayer.objects.filter(user=user).exists()
            profile['follower_count'] = Follow.objects.filter(followed=user).count()
            profile['stats'] = sr.get_clean_dict(user.stats)
            profile['is_followed'] = Follow.objects.filter(
                followed=user, follower=request.user).exists()
            return Response(profile, status=status.HTTP_200_OK)
        return Response(dict(error='User not found'), status=status.HTTP_404_NOT_FOUND)



