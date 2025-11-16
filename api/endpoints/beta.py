from .libs import *
from beta.models import BetaTester


class BetaPrivateAccessAPI(views.APIView):

    def get(self, request: Request, private_key: str) -> Response:
        tester = BetaTester.objects.filter(
            private_key=private_key).first()
        if tester is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(dict(access_key=str(RefreshToken.for_user(tester.user).access_token)))