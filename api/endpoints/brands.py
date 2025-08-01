from .libs import *
from brands.models import Brand
from profiles.models import FavoriteBrand


class BrandsAPI(views.APIView):

    def get(self, request: Request) -> Response:
        return Response(Brand.all_details(), status=status.HTTP_200_OK)
    

class FavoriteBrandAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(
            [fav.brand.details for fav in request.user.favbrands.all()], status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        brand_id = request.data.get('brand_id')
        brand = Brand.objects.get(id=brand_id)
        fav_brand, created = FavoriteBrand.objects.get_or_create(
            user=request.user, brand=brand)
        if not created:
            fav_brand.delete()
        action = 'Added' if created else 'Removed'
        return Response(
            dict(message=f'{action}: {brand.name} as favorite brand'), status=status.HTTP_200_OK)
    
    def patch(self, request: Request) -> Response:
        brand_ids = request.data.get('brandIDs')
        brands = Brand.objects.filter(id__in=brand_ids)
        for brand in brands:
            FavoriteBrand.objects.get_or_create(user=request.user, brand=brand)
        
        return Response(dict(message='Added favorite brands'))