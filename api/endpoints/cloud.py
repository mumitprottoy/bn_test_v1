from .libs import *
from cloud.engine import CloudEngine


def unpack(request: Request) -> tuple[str]:
    file_name = request.data.get('file_name').lower()
    bucket = request.data.get('bucket')
    return file_name, bucket


class FileUploadKeyRequestAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        file_name, bucket = unpack(request)
        engine = CloudEngine(bucket=bucket)
        key = engine.get_file_upload_key(file_name)
        if key is not None:
            return Response(dict(key=key))
        return Response(errors=engine.errors, 
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)


class MultipartUploadInitiationAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        file_name, bucket = unpack(request)
        engine = CloudEngine(bucket=bucket)
        key = engine.get_file_upload_key(file_name)
        if key is None: return Response(errors=engine.errors, 
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
        upload_id = engine.initiate_multipart_upload(key)
        if upload_id is None: return Response(
            dict(errors=engine.errors), status=status.HTTP_400_BAD_REQUEST)
        return Response(dict(key=key, upload_id=upload_id))


class PartUploadPresignedURLRequestAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        engine = CloudEngine(bucket=request.data.get('bucket'))
        presigned_url = engine.get_presigned_url_for_part_upload(
            **request.data.get('params'))
        if presigned_url is not None:
            return Response(dict(presigned_url=presigned_url))
        return Response(dict(errors=engine.errors), status=status.HTTP_400_BAD_REQUEST)
    

class MultipartUploadCompletionRequestAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        engine = CloudEngine(bucket=request.data.get('bucket'))
        completion = engine.complete_multipart_upload(
            **request.data.get('params'))
        if completion is not None:
            public_url = engine.__get_file_public_url(request.data.get('key'))
            return Response(dict(public_url=public_url))
        return Response(dict(errors=engine.errors), status=status.HTTP_400_BAD_REQUEST)
