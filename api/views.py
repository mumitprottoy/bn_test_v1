from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import views, status
from rest_framework_simplejwt.tokens import RefreshToken
from entrance.operations import AuthHandler
from entrance.models import EmailVerification
from profiles.models import FavoriteBrand
from pros.models import ProPlayer
from brands.models import Brand
from .endpoints.posts import *
from .endpoints.stats import *
from .endpoints.profiles import *
from .endpoints.teams import *
from .endpoints.users import *
from .endpoints.test import *
from .endpoints.chat import *
from .endpoints.brands import *
from .endpoints.feedbacks import *
from .endpoints.entrance import *
from .endpoints.tournaments import *
from .endpoints.centers import *
from .endpoints.habijabi import *
from .endpoints.pinscore import *
from .endpoints.beta import *
from .endpoints.lanes import *
from .endpoints.cloud import *
from .endpoints.tube import *
from . import serializers


class ProLoginAPI(views.APIView):

    def post(self, request: Request) -> Response:
        handler = AuthHandler(**request.data)
        user = handler.authenticate()

        if user is not None:
            if ProPlayer.objects.filter(user=user).exists():
                refresh_token = RefreshToken.for_user(user)
                return Response({
                    'access_token': str(refresh_token.access_token)
                }, status=status.HTTP_200_OK)
            else: return Response({
                'errors': ['pro player only']
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({
            'errors': handler.errors
        }, status=status.HTTP_401_UNAUTHORIZED)


class AmateurLoginAPI(views.APIView):

    def post(self, request: Request) -> Response:
        handler = AuthHandler(**request.data)
        user = handler.authenticate()

        if user is not None:
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh_token.access_token)
            }, status=status.HTTP_200_OK)       
        return Response({
            'errors': handler.errors
        }, status=status.HTTP_401_UNAUTHORIZED)


class UserRegisterAPI(views.APIView):

    def post(self, request):
        serializer = serializers.UserCreateSerializer(data=request.data.get('basicInfo'))
        email = request.data.get('basicInfo')['email'].lower()
        email_verification = EmailVerification.objects.filter(email=email, is_verified=True).first()
        if email_verification is None:
            return Response(dict(error='Email is not verified'), status=status.HTTP_400_BAD_REQUEST)
        if serializer.is_valid():
            user = serializer.save()
            if 'brandIDs' in request.data:
                brand_ids = request.data.get('brandIDs')
                for brand in Brand.objects.filter(id__in=brand_ids):
                    FavoriteBrand.objects.create(user=user, brand=brand)
            return Response({'message': 'User created successfully!'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TestPayloadAPI(views.APIView):
    def post(self, request: Request) -> Response:
        import json
        from entrance.models import TestPayload
        data = json.dumps(request.data, ensure_ascii=False, indent=4)
        payload = TestPayload.objects.create(data=data)
        payload_dict = json.loads(payload.data)
        return Response(payload_dict)