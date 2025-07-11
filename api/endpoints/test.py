from .libs import *
from cloud.engine import CloudEngine


class TestImageUploadAPI(views.APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    def post(self, request: Request) -> Response:
        print(request.data)
        print('*filename:', request.data.get('file_name'))
        image = request.data.get('image')
        engine = CloudEngine(image)
        cloud_image_url = engine.upload()
        if cloud_image_url is not None:
            return Response(dict(
                message='Received',
                cloudImageURL=cloud_image_url,
                imageName=image.name,
                imageFileType=image.name.split('.')[-1].lower(),
                imageSize=f'{round(image.size / (1024 ** 2), 2)} MB'
            ))
        return Response(dict(errors=engine.errors), status=status.HTTP_400_BAD_REQUEST)