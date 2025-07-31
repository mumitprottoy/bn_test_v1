import io, csv
from .libs import *
from emailsystem.engine import EmailEngine
from entrance.models import EmailVerification, PreRegistration


class SendInvitesWithCSVFileAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def post(self, request: Request) -> Response:
        csv_file = request.FILES.get('csv_file')
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        data = list(reader)
        invite_link = 'https://youtube.com'
        sent_count = 0
        for _ in data:
            engine = EmailEngine(
                recipient_list=[_['email']], 
                subject='Where Bowlers Belong — Your Invite to BowlersNetwork',
                template='emails/invite.html',
                context=dict(full_name=f'{_['first_name']} {_['last_name']}', invite_link=invite_link)
                )
            sent_count += engine.send()
        return Response(dict(sent_to=f'{sent_count} people', csv_file_data=data))


class PreRegistrationAPI(views.APIView):
    
    def post(self, request: Request) -> Response:
        email = request.data.get('email')
        email_verifiaction = EmailVerification.objects.filter(
            email=email, is_verified=True).first()
    
        if email_verifiaction is None:
            return Response(
                dict(error='Email is not verified'), status=status.HTTP_401_UNAUTHORIZED)
        
        PreRegistration.objects.create(**request.data)
        return Response(dict(message='Pre-registration completed'))


class SendEmailVerificationCode(views.APIView):

    def post(self, request: Request) -> Response:
        email = request.data.get('email')
        email_verifiaction, _ = EmailVerification.objects.get_or_create(
            email=email)
        if email_verifiaction.is_verified:
            return Response(
                dict(error='Email is already verified'), status=status.HTTP_400_BAD_REQUEST)
        email_verifiaction.send_code()
        return Response(dict(message='Email verification code sent'))


class VerifyEmailAPI(views.APIView):

    def post(self, request: Request) -> Response:
        email = request.data.get('email')
        code = request.data.get('code')
        email_verification = EmailVerification.objects.filter(
            email=email, code=code).first()
        if email_verification is None:
            return Response(
                dict(error='No verification code was sent to this email'), status=status.HTTP_400_BAD_REQUEST)
        if email_verification.is_verified:
            return Response(dict(error='Email already verified'), status=status.HTTP_409_CONFLICT)
        verified = email_verification.verify(code)
        if verified:
            return Response(dict(message='Email verified'))
        else:
            return Response(dict(error='Wrong verification code'), status=status.HTTP_401_UNAUTHORIZED)
