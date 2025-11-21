from .libs import *
from lanes.models import DiscussionTopic, Discussion, DiscussionOpinion


class DiscussionTopicAPI(views.APIView):

    def get(self, request: Request) -> Response:
        return Response(DiscussionTopic.all_topics())
    

class DiscussionAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response([d.details for d in Discussion.objects.filter(user=request.user)])

    def post(self, request: Request) -> Response:
        topic = DiscussionTopic.objects.get(
            id=request.data.get('topic_id'))
        discussion = Discussion(**request.data)
        discussion.topic = topic
        discussion.user = request.user
        discussion.save()
        return Response(discussion.details)


class DiscussionOpinionAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, discussion_id: int) -> Response:
        discussion = Discussion.objects.get(id=discussion_id)
        DiscussionOpinion.objects.create(
            discussion=discussion,
            user=request.user,
            opinion=request.data.get('opinion')
        )
        return Response(discussion.details_for_user(request.user))


class DiscussionFeedAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response([d.details_for_user(
            user=request.user) for d in Discussion.objects.all()])


class DiscussionVoteAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        node_type = request.data.get('node_type')
        node_id = request.data.get('node_id')

        if node_type == 'discussion':
            node = Discussion.objects.get(id=node_id)
        else: node = DiscussionOpinion.objects.get(id=node_id)

        response = node.vote(
            voter=request.user, is_upvote=request.data.get('is_upvote'))
        
        response.update(request.data)
        return Response(response)