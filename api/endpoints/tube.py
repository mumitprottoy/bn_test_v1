from .libs import *
from tube.models import LargeVideo, LargeVideoLike, LargeVideoComment
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
        return Response([v.details for v in request.user.large_videos.all().order_by('id')])

    def post(self, request: Request) -> Response:
        large_video = LargeVideo(**request.data)
        large_video.user = request.user
        large_video.save()
        return Response(large_video.details)


class LargeVideosFeedAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response([v.details_for_user(
            request.user) for v in LargeVideo.objects.all().order_by('-id')])


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


class LargeVideoDeleteAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request: Request, video_id: int) -> Response:
        large_video_set = LargeVideo.objects.filter(id=video_id)
        if not large_video_set.exists():
            return Response(status=status.HTTP_404_NOT_FOUND)
        if large_video_set.first().user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        large_video_set.delete()
        return Response()


class LargeVideoLikeAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, uid: str) -> Response:
        large_video = LargeVideo.objects.filter(uid=uid).first()
        if large_video is not None:
            like, created = LargeVideoLike.objects.get_or_create(
                user=request.user, large_video=large_video)
            if not created: like.delete()
            return Response(dict(
                is_liked=created, likes_count=large_video.likes_count))
        return Response(status=status.HTTP_404_NOT_FOUND)
    

class LargeVideoCommentAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, uid: str) -> Response:
        large_video = LargeVideo.objects.filter(uid=uid).first()
        if large_video is not None:
            comment = LargeVideoComment.objects.create(
                large_video=large_video,
                user=request.user,
                comment=request.data.get('comment')
            )
            return Response(comment.details)
        return Response(status=status.HTTP_404_NOT_FOUND)
        