from .libs import *
from centers.models import Center, CenterAdmin
from utils import error_messages, constants as const
from cloud.engine import CloudEngine


class CenterCreationAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        if Center.objects.filter(name=request.data.get('name')).exists():
            return Response(
                dict(error=error_messages.NAME_ALREADY_EXISTS), status=status.HTTP_400_BAD_REQUEST)
        
        if Center.objects.filter(
            lat=request.data.get('lat'), long=request.data.get('long')).exists():
            return Response(
                dict(error=error_messages.GEO_COORDINATE_EXISTS), status=status.HTTP_400_BAD_REQUEST)

        if CenterAdmin.objects.filter(user=request.user).exists():
            return Response(
                dict(error=error_messages.ALREADY_ADMIN), status=status.HTTP_400_BAD_REQUEST)
        
        center = Center.objects.create(**request.data)
        CenterAdmin.objects.create(user=request.user, center=center)

        return Response(center.details)


class GetCenterDataByCurrentUserAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        center_admin = CenterAdmin.objects.filter(user=request.user).first()
        center_details = center_admin.center.details if center_admin is not None else None
        return Response(dict(center=center_details))
    

class UploadCenterLogoAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request: Request) -> Response:
        center = CenterAdmin.objects.get(user=request.user).center
        image = request.data.get('image')
        if image and image.name.lower().split('.')[1] in const.PROFILE_PIC_SUPPORTED_FILES:
            cloud_engine = CloudEngine(image, 'profiles')
            image_pub_url = cloud_engine.upload()
            if image_pub_url is not None:
                center.logo = image_pub_url
                center.save()
            return Response(dict(
                message='Success', image_public_url=image_pub_url), status=status.HTTP_200_OK)
        else: return Response(
            dict(message=f'Unsupported file type. Supported file types: {", ".join(const.PROFILE_PIC_SUPPORTED_FILES)}'),
            status=status.HTTP_400_BAD_REQUEST
        )
        