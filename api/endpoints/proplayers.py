from libs import *
from pros.models import Social, SocialLink, ProPlayer
from utils import subroutines as sr


class SocialsAPI(views.APIView):

    def get(self, request: Request) -> Response:
        return Response(
            [sr.get_clean_dict(social) for social in Social.objects.all()])
