from .libs import *
from rest_framework.request import QueryDict
from habijabi.models import (
    ProPlayer, Questionnaire, QuestionnaireAnswers, ProsOnboarding)


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


class SubmitSurveyAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        pro_onb = ProsOnboarding.objects.filter(
            email=request.user.email).first()
        if pro_onb is not None:
            pro_onb.has_answered = True
            pro_onb.save()
        return Response()


class SubmitAnswerByQuesIDAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request, ques_id: int) -> Response:
        q = Questionnaire.objects.get(id=ques_id)
        qa = QuestionnaireAnswers.objects.filter(
            pro=request.user.pro, questionnaire=q).first()
        if qa is None:
            qa = QuestionnaireAnswers(pro=request.user.pro, questionnaire=q)
        qa.answer = request.data.get('answer')
        qa.save()
        return Response(qa.details)


class ProInfoAPI(views.APIView):

    def get(self, request: Request) -> Response:
        return Response([po.details for po in ProsOnboarding.objects.all().order_by('-id')])
    
    def post(self, request: Request) -> Response:
        po = ProsOnboarding.objects.create(**request.data)
        return Response(po.details)


class ProsPrivateOnboardingAPI(views.APIView):

    def post(self, request: Request) -> Response:
        private_key = request.data.get('private_key')
        pro_onb = ProsOnboarding.objects.filter(private_key=private_key).first()
        if pro_onb is None: return Response(status=status.HTTP_401_UNAUTHORIZED)
        pro = pro_onb.setup_account(**request.data.get('data'))
        token = RefreshToken.for_user(pro.user)
        return Response(dict(tokan=token, user=pro.user.minimal))
    

class ProsPrivateAuthAPI(views.APIView):

    def post(self, request: Request) -> Response:
        private_key = request.data.get('private_key')
        pro_onb = ProsOnboarding.objects.filter(private_key=private_key).first()
        if pro_onb is None: return Response(status=status.HTTP_401_UNAUTHORIZED)
        token = None
        if pro_onb.is_onboard:
            user = User.objects.get(email=pro_onb.email)
            token = RefreshToken.for_user(user)
        return Response(dict(access_token=token))