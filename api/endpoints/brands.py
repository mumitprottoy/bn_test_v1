from .libs import *
from brands.models import Brand


class BrandsAPI(views.APIView):

    def get(self, request: Request) -> Response:
        return Response(Brand.all_details(), status=status.HTTP_200_OK)