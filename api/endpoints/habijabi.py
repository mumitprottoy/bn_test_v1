from .libs import *
from rest_framework.request import QueryDict
from habijabi.models import Questionnaire

CODE = '0912'

def code_is_valid(code_container: QueryDict) -> bool:
    return code_container.get('securityCode') == CODE


class AddQuestionAPI(views.APIView):

    def post(self, request: Request) -> Response:
        if code_is_valid(request.data):
            q = Questionnaire.objects.create(
                question=request.data.get('question'),
                description=request.data.get('description')
            )
            return Response(q.details)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AllQuestionsAPI(views.APIView):

    def get(self, request: Request) -> Response:
        return Response(Questionnaire.all_questions())


class EditQuestionAPI(views.APIView):

    def post(self, request: Request, ques_id: int) -> Response:
        if code_is_valid(request.data):
            q = Questionnaire.objects.get(id=ques_id)
            q.question = request.data.get('question')
            q.description = request.data.get('description')
            q.save()
            return Response(q.details)
        return Response(status=status.HTTP_401_UNAUTHORIZED) 
    

class DeleteQuestionAPI(views.APIView):

    def delete(self, request: Request, ques_id: int) -> Response:
        if code_is_valid(request.data):
            Questionnaire.objects.get(id=ques_id).delete()
            return Response()
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class SerializeQuestionsAPI(views.APIView):

    def post(self, request: Request) -> Response:
        if code_is_valid(request.data):
            serials: dict = request.data.get('serials')
            for ques_id, serial in serials.items():
                Questionnaire.objects.filter(id=int(ques_id)).update(serial=serial)
            return Response(Questionnaire.all_questions())
        return Response(status=status.HTTP_401_UNAUTHORIZED)
