from .libs import *
from profiles.models import Follow, FavoriteBrand
from utils import subroutines as sr
from pros.models import ProPlayer, Sponsors
from interface.stats import EngagementStats
from cloud.engine import CloudEngine


class PlayerProfileAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        profile = request.user.basic.copy()
        pro = ProPlayer.objects.filter(user=request.user).first()
        profile['is_pro'] = pro is not None
        if profile['is_pro']:
            profile['sponsors'] = [sponsor.brand.details for sponsor in pro.sponsors.all()]
        # followers = [f.follower.details for f in Follow.objects.filter(
        #     followed=request.user)]
        profile['follower_count'] = Follow.objects.filter(followed=request.user).count()
        # profile['followers'] = followers
        profile['stats'] = sr.get_clean_dict(request.user.stats)
        profile['favorite_brands'] = [fav.brand.details for fav in request.user.favbrands.all()]
        return Response(profile, status=status.HTTP_200_OK)


class ProPlayersPublicProfileAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        users = [pro.user for pro in ProPlayer.objects.all()]
        user_profiles = list()
        for user in users:
            profile = user.basic.copy()
            pro = ProPlayer.objects.filter(user=user).first()
            profile['is_pro'] = pro is not None
            if profile['is_pro']:
                profile['sponsors'] = [sponsor.brand.details for sponsor in pro.sponsors.all()]
            profile['follower_count'] = Follow.objects.filter(followed=user).count()
            profile['stats'] = sr.get_clean_dict(user.stats)
            profile['is_followed'] = Follow.objects.filter(
                followed=user, follower=request.user).exists()
            profile['favorite_brands'] = [fav.brand.details for fav in user.favbrands.all()]
            user_profiles.append(profile)  
        import random
        random.shuffle(user_profiles)
        return Response(user_profiles, status=status.HTTP_200_OK)


class UserProfileByID(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, user_id: int) -> Response:
        user = User.objects.filter(id=user_id).first()
        if user is not None:
            profile = user.basic.copy()
            pro = ProPlayer.objects.filter(user=user).first()
            profile['is_pro'] = pro is not None
            if profile['is_pro']:
                profile['sponsors'] = [sponsor.brand.details for sponsor in pro.sponsors.all()]
            profile['follower_count'] = Follow.objects.filter(followed=user).count()
            profile['stats'] = sr.get_clean_dict(user.stats)
            profile['engagement'] = EngagementStats.stats_of_user(user)
            profile['is_followed'] = Follow.objects.filter(
                followed=user, follower=request.user).exists()
            profile['favorite_brands'] = [fav.brand.details for fav in user.favbrands.all()]
            return Response(profile, status=status.HTTP_200_OK)
        return Response(dict(error='User not found'), status=status.HTTP_404_NOT_FOUND)


class UploadProfilePicture(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request: Request) -> Response:
        image = request.data.get('image')
        cloud_engine = CloudEngine(image)
        image_pub_url = cloud_engine.upload()
        if image_pub_url is not None:
            request.user.profile_picture_url = image_pub_url
            request.user.save()
        return Response(dict(
            message='Success', image_public_url=image_pub_url), status=status.HTTP_200_OK)
