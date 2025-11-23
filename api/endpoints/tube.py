from .libs import *
from tube.models import LargeVideo


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
        return Response()


class LargeVideosFeedAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response([v.details for v in LargeVideo.objects.all()])


class LargeVideoDetailsAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, uid: str) -> Response:
        return Response(LargeVideo.objects.get(uid=uid).details)