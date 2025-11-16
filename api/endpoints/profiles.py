import json
from .libs import *
from profiles.models import Follow, CityAndCountry, UserInfo
from utils import subroutines as sr, constants as const
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
        profile['is_complete'] = profile['favorite_brands'].__len__() > 0
        return Response(profile, status=status.HTTP_200_OK)


class ProPlayersPublicProfileAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        users = [pro.user for pro in ProPlayer.objects.filter(is_public=True).all()]
        user_profiles = list()
        for user in users:
            profile = user.basic.copy()
            pro = ProPlayer.objects.filter(user=user).first()
            profile['is_pro'] = pro is not None
            if profile['is_pro']:
                profile['sponsors'] = pro.sponsors_list
                profile['socials'] = pro.social_links
            profile['follower_count'] = Follow.objects.filter(followed=user).count()
            profile['stats'] = sr.get_clean_dict(user.stats)
            profile['is_followed'] = Follow.objects.filter(
                followed=user, follower=request.user).exists()
            profile['favorite_brands'] = [fav.brand.details for fav in user.favbrands.all()]
            profile['is_complete'] = profile['favorite_brands'].__len__() > 0
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
                profile['sponsors'] = pro.sponsors_list
                profile['socials'] = pro.social_links
            profile['follower_count'] = Follow.objects.filter(followed=user).count()
            profile['stats'] = sr.get_clean_dict(user.stats)
            profile['engagement'] = EngagementStats.stats_of_user(user)
            profile['is_followed'] = Follow.objects.filter(
                followed=user, follower=request.user).exists()
            profile['favorite_brands'] = [fav.brand.details for fav in user.favbrands.all()]
            profile['is_complete'] = profile['favorite_brands'].__len__() > 0
            return Response(profile, status=status.HTTP_200_OK)
        return Response(dict(error='User not found'), status=status.HTTP_404_NOT_FOUND)


class UserProfileByUsername(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, username: str) -> Response:
        user = User.objects.filter(username=username).first()
        if user is not None:
            profile = user.basic.copy()
            pro = ProPlayer.objects.filter(user=user).first()
            profile['is_me'] = user.id == request.user.id
            profile['is_pro'] = pro is not None
            if profile['is_pro']:
                profile['sponsors'] = pro.sponsors_list
                profile['socials'] = pro.social_links
            else: 
                profile['favorite_brands'] = [fav.brand.details for fav in user.favbrands.all()]
                profile['is_complete'] = profile['favorite_brands'].__len__() > 0
            profile['follower_count'] = Follow.objects.filter(followed=user).count()
            profile['stats'] = sr.get_clean_dict(user.stats)
            profile['engagement'] = EngagementStats.stats_of_user(user)
            profile['is_followed'] = Follow.objects.filter(
                followed=user, follower=request.user).exists()
            
            return Response(profile, status=status.HTTP_200_OK)
        return Response(dict(error='User not found'), status=status.HTTP_404_NOT_FOUND)


class ProPlayerProfileByUsername(views.APIView):
    
    def get(self, request: Request, username: str) -> Response:
        user = User.objects.filter(username=username).first()
        pro = ProPlayer.objects.filter(user=user).first()
        if pro is not None:
            profile = user.basic.copy()
            profile['sponsors'] = pro.sponsors_list
            profile['socials'] = pro.social_links
            profile['follower_count'] = Follow.objects.filter(followed=user).count()
            profile['stats'] = sr.get_clean_dict(user.stats)
            profile['engagement'] = EngagementStats.stats_of_user(user)
            if request.user.is_authenticated:
                profile['is_followed'] = Follow.objects.filter(
                    followed=user, follower=request.user).exists()
            return Response(profile, status=status.HTTP_200_OK)
        return Response(dict(error='User not found'), status=status.HTTP_404_NOT_FOUND)


class UploadProfilePictureAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request: Request) -> Response:
        image = request.data.get('image')
        if image and image.name.lower().split('.')[1] in const.PROFILE_PIC_SUPPORTED_FILES:
            cloud_engine = CloudEngine(image, 'profiles')
            image_pub_url = cloud_engine.upload()
            if image_pub_url is not None:
                request.user.profile_picture_url = image_pub_url
                request.user.save()
            return Response(dict(
                message='Success', image_public_url=image_pub_url), status=status.HTTP_200_OK)
        else: return Response(
            dict(message=f'Unsupported file type. Supported file types: {", ".join(const.PROFILE_PIC_SUPPORTED_FILES)}'),
            status=status.HTTP_400_BAD_REQUEST
        )


class UploadCoverPhotoAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def post(self, request: Request) -> Response:
        # return Response(dict(method='POST'))
        image = request.data.get('image')
        if image and image.name.lower().split('.')[1] in const.COVER_PHOTO_SUPPORTED_FILES:
            cloud_engine = CloudEngine(image, 'profiles')
            image_pub_url = cloud_engine.upload()
            if image_pub_url is not None:
                request.user.cover_photo_url = image_pub_url
                request.user.save()
            return Response(dict(
                message='Success', image_public_url=image_pub_url), status=status.HTTP_200_OK)
        else: return Response(
            dict(message=f'Unsupported file type ({image.name.lower().split('.')[1]}). Supported file types: {', '.join(const.COVER_PHOTO_SUPPORTED_FILES)}'),
            status=status.HTTP_400_BAD_REQUEST
        )

class UploadIntroVideoAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request: Request) -> Response:
        video = request.data.get('video')
        if video and video.name.lower().split('.')[1] in const.INTRO_VIDEO_SUPPORTED_FILES:
            cloud_engine = CloudEngine(video, 'profiles')
            video_pub_url = cloud_engine.upload()
            if video_pub_url is not None:
                request.user.introvideo.url = video_pub_url
                request.user.introvideo.save()
            return Response(dict(
                message='Success', video_public_url=video_pub_url), status=status.HTTP_200_OK)
        else: return Response(
            dict(message=f'Unsupported file type ({video.name.lower().split('.')[1]}). Supported file types: {', '.join(const.INTRO_VIDEO_SUPPORTED_FILES)}'),
            status=status.HTTP_400_BAD_REQUEST
        )


class CountriesAPI(views.APIView):

    def get(self, request: Request) -> Response:
        return Response([cc.details for cc in CityAndCountry.objects.all()])
    

class SecretDeleteUserAPI(views.APIView):

    def post(self, request: Request) -> Response:
        if request.data.get('key') != 'zxcvbnm':
            return Response(dict(error='Invalid key'), status=status.HTTP_401_UNAUTHORIZED)
        username = request.data.get('username')
        User.objects.filter(username=username).delete()
        return Response(dict(message=f'User with username `{username}` is deleted.'))
    

class DeleteAccountAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        if request.user.check_password(request.data.get('password')):
            request.user.is_active = False
            request.user.save()
            return Response(dict(user_id=request.user.id, name=request.user.get_full_name(), status='Account Deleted.'))
        return Response(dict(error='Incorrect password'), status=status.HTTP_401_UNAUTHORIZED)


class UserInfoAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def initial(self, request: Request, *args, **kwargs) -> None:
        super().initial(request, *args, **kwargs)
        self.user_info, self.created = UserInfo.objects.get_or_create(user=request.user)

    def get(self, request: Request) -> Response:
        return Response(self.user_info.details)
    
    def post(self, request: Request) -> Response:
        self.user_info.info = json.dumps(request.data, indent=4, ensure_ascii=False)
        self.user_info.is_added = True
        self.user_info.save()
        return Response(self.user_info.details)


class ProfileStatusAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(dict(
            fav_brands=request.user.favbrands.exists(),
            game_stats=request.user.stats.is_added,
            user_info=UserInfo.objects.filter(user=request.user).exists()
        ))