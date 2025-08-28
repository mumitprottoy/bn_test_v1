from .libs import *
from posts import models
from interface.posts import Poster, PostViewer
from .. import messages as msg
from rest_framework.pagination import PageNumberPagination


class PostPaginator(PageNumberPagination):
    page_size = 50  
    page_size_query_param = 'size'  
    max_page_size = 100  

    def get_paginated_response(self, data: dict) -> Response:
        return Response(data)


class PostFeedAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request: Request) -> Response:
        user = request.user
        viewer = PostViewer(user)
        queryset = viewer.get_viewable_posts_queryset()
        paginator = PostPaginator()
        posts : list[models.PostMetaData] = paginator.paginate_queryset(
            queryset=queryset, request=request)
        return paginator.get_paginated_response(
            data=[p.details(user) for p in posts])
    

class UserPostAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser, parsers.JSONParser]
     
    def get(self, request: Request) -> Response:
        return Response(dict(
            posts = [p.details() for p in models.PostMetaData.objects.filter(
                user=request.user).order_by('-id')]
        ))
    
    def post(self, request: Request) -> Response:
        kwargs = dict()
        for k in request.data:
            kwargs[k] = request.data.get(k)
        if 'media' in request.FILES:
            kwargs['media'] = request.FILES.getlist('media')
        poster = Poster(user=request.user, **kwargs)
        metadata = poster.create_post()
        # return Response(metadata.details(), status=status.HTTP_200_OK)
        return Response(request.data)
        # except Exception as e: 
        #     # error in dev; MUST be changed in prod
        #     return Response(dict(errors=[str(e)]), status=status.HTTP_400_BAD_REQUEST)


class PostClickLikeAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request: Request, metadata_id: int) -> Response:
        metadata = models.PostMetaData.objects.filter(id=metadata_id).first()
        if metadata is not None:
            like, created = models.PostLike.objects.get_or_create(
                metadata=metadata, user=request.user)
            if created:
                # send notification
                pass
            else: like.delete()
            return Response(
                dict(message=msg.SUCCESS, likes=like.metadata.all_likes), status=status.HTTP_200_OK)
        return Response(dict(errors=[msg.INVALID_ID]), status=status.HTTP_404_NOT_FOUND)
    

class PostAddCommentAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request: Request, metadata_id: int) -> Response: 
        metadata = models.PostMetaData.objects.filter(id=metadata_id).first()
        if metadata is not None:
            content = request.data.get('text')
            comment = models.PostComment.objects.create(
                metadata=metadata, user=request.user, content=content)
            return Response(dict(comment=comment.details), status=status.HTTP_200_OK)
        return Response(dict(errors=[msg.INVALID_ID]), status=status.HTTP_404_NOT_FOUND)


class PostAddReplyAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request: Request, comment_id: int) -> Response: 
        comment = models.PostComment.objects.filter(id=comment_id).first()
        if comment is not None:
            content = request.data.get('text')
            reply = models.PostCommentReply.objects.create(
                comment=comment, user=request.user, content=content)
            return Response(dict(reply=reply.details), status=status.HTTP_200_OK)
        return Response(dict(errors=[msg.INVALID_ID]), status=status.HTTP_404_NOT_FOUND)
            

class PostLikesAPI(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request: Request, metadata_id: int) -> Response:
        metadata = models.PostMetaData.objects.filter(id=metadata_id).first()
        if metadata is not None:
            return Response(metadata.all_likes, status=status.HTTP_200_OK)  
        return Response(dict(errors=[msg.INVALID_ID]), status=status.HTTP_404_NOT_FOUND)


class PostCommentsAPI(views.APIView):
    # permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request: Request, metadata_id: int) -> Response:
        metadata = models.PostMetaData.objects.filter(id=metadata_id).first()
        if metadata is not None:
            return Response(metadata.all_comments, status=status.HTTP_200_OK)  
        return Response(dict(errors=[msg.INVALID_ID]), status=status.HTTP_404_NOT_FOUND)


class UserPostsByID(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, user_id: int) -> Response:
        user = User.objects.filter(id=user_id).first()
        if user is not None:
            return Response([post.details() for post in models.PostMetaData.objects.filter(
                user=user).order_by('-id')])
        return Response(dict(error='User not found'))
    

class PostsByID(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, post_id: int) -> Response:
        return Response(
            models.PostMetaData.objects.get(
                id=post_id).details(request.user))


class PostsByUID(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, uid: str) -> Response:
        return Response(
            models.PostMetaData.objects.get(
                uid=uid).details(request.user))


class PollVoteAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request, option_id: int) -> Response:
        opt = models.PollOption.objects.filter(id=option_id).first()
        if opt is not None:
            response = opt.poll.vote(voter=request.user, opt=opt)
            return Response(response, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)