from .libs import *
from rest_framework.request import QueryDict
from habijabi.models import Questionnaire
from onboarding.models import ProPlayer, ProsOnboarding, QuestionnaireAnswers

CODE = '0912'

def code_is_valid(code_container: QueryDict) -> bool:
    return code_container.get('securityCode') == CODE


class AddQuestionAPI(views.APIView):

    def post(self, request: Request) -> Response:
        if code_is_valid(request.data):
            q = Questionnaire.objects.create(**request.data.get('data'))
            return Response(q.details)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class AllQuestionsAPI(views.APIView):

    def get(self, request: Request) -> Response:
        return Response(Questionnaire.all_questions())


class EditQuestionAPI(views.APIView):

    def post(self, request: Request, ques_id: int) -> Response:
        if code_is_valid(request.data):
            q = Questionnaire.objects.filter(id=ques_id)
            if not q.exists(): return Response(status=status.HTTP_404_NOT_FOUND)
            q.update(**request.data.get('data'))
            return Response(q.first().details)
        return Response(status=status.HTTP_401_UNAUTHORIZED) 
    

class DeleteQuestionAPI(views.APIView):

    def delete(self, request: Request, ques_id: int) -> Response:
        if code_is_valid(request.data):
            q = Questionnaire.objects.filter(id=ques_id).first()
            if q is None: return Response(status=status.HTTP_404_NOT_FOUND)
            details = q.details
            serial = q.serial
            q.delete()
            Questionnaire.sync_serial(serial)
            return Response(dict(
                deleted_question=details, 
                updated_questions=Questionnaire.all_questions()
            ))
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class SerializeQuestionsAPI(views.APIView):

    def post(self, request: Request) -> Response:
        if code_is_valid(request.data):
            serials: dict = request.data.get('serials')
            for ques_id, serial in serials.items():
                Questionnaire.objects.filter(id=int(ques_id)).update(serial=serial)
            return Response(Questionnaire.all_questions())
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class ValidateSecurityCodeAPI(views.APIView):

    def post(self, request: Request) -> Response:
        if code_is_valid(request.data):
            return Response()
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class PrivateURLEmailAPI(views.APIView):

    def get(self, request: Request, pro_onb_id: int) -> Response:
        pro_onb = ProsOnboarding.objects.get(id=pro_onb_id)
        pro_onb.send_private_url()
        return Response()


class SubmitAnswersAPI(views.APIView):

    def post(self, request: Request) -> Response:
        user = User.objects.get(id=request.data.get('user_id'))
        pro = ProPlayer.objects.get(user=user)
        for ans in request.data.get('answers'):
            q = Questionnaire.objects.get(id=ans['ques_id'])
            QuestionnaireAnswers.objects.create(
                pro=pro,
                question=q.question,
                description=q.description,
                answer=ans['answer']
            )
        ProsOnboarding.objects.filter(email=pro.user.email).update(has_answered=True)
        return Response(QuestionnaireAnswers.all_answers_of_pro(pro))


class ProInfoAPI(views.APIView):

    def get(self, request: Request) -> Response:
        return Response([po.details for po in ProsOnboarding.objects.all().order_by('-id')])
    
    def post(self, request: Request) -> Response:
        po = ProsOnboarding.objects.create(**request.data)
        return Response(po.details)
    