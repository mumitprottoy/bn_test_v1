from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import views, status
from rest_framework_simplejwt.tokens import RefreshToken
from pros.operations import AuthHandler
from pros.models import ProPlayer


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
