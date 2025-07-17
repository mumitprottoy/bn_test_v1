from .libs import *
from feedback.models import FeedbackType, Feedback


class FeedbackTypesAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(dict(
            feedback_types=[dict(
            feedback_type_id=ft.id,
            name=ft.name
        ) for ft in FeedbackType.objects.all()]))


class FeedbacksAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(Feedback.feedback_by_type())
    
    def post(self, request: Request) -> Response:
        kwargs = dict(
            user=request.user,
            feedback_type=FeedbackType.objects.get(
                request.data.get('feedback_type_id')),
            title=request.data.get('title'),
            details=request.data.get('details')
        )
        feedback = Feedback.objects.create(**kwargs)
        return Response(feedback.feedback_details)