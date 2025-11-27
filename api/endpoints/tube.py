from .libs import *
from tube.models import LargeVideo
from cloud.engine import CloudEngine


class LargeVideoMetaDataValidationAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        metadata_is_valid = LargeVideo.validate_video_metadata(**request.data)
        if metadata_is_valid: return Response()
        return Response(status=status.HTTP_400_BAD_REQUEST)


class LargeVideosAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response([v.details for v in request.user.large_videos.all()])

    def post(self, request: Request) -> Response:
        large_video = LargeVideo(**request.data)
        large_video.user = request.user
        large_video.save()
        return Response(large_video.details)


class LargeVideosFeedAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response([v.details for v in LargeVideo.objects.all()])


class LargeVideoDetailsAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, uid: str) -> Response:
        return Response(LargeVideo.objects.get(uid=uid).details)
    

class SmallVideoUploadAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def post(self, request: Request) -> Response:
        video = request.data.get('video')
        cloud_engine = CloudEngine(video, 'cdn')
        public_url = cloud_engine.upload()
        return Response(dict(
            public_url=public_url), status=status.HTTP_200_OK)
    

class LargeVideoEditAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, video_id: str) -> Response:
        large_video_set = LargeVideo.objects.filter(id=video_id)
        if not large_video_set.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        if large_video_set.first().user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        large_video_set.update(**request.data)
        return Response(large_video_set.first().details)
