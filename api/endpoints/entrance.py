import io, csv
from .libs import *
from emailsystem.engine import EmailEngine
from entrance.models import EmailVerification, PreRegistration
from pros.models import ProPlayer
from habijabi.models import ProsOnboarding


class SendInvitesWithCSVFileAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def post(self, request: Request) -> Response:
        csv_file = request.FILES.get('csv_file')
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        data = list(reader)
        invite_link = 'https://bowlersnetwork.com'
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
        email_verification = EmailVerification.objects.filter(email=email).first()
        if email_verification is not None and email_verification.is_verified:
            if PreRegistration.objects.filter(email=email).exists():
                return Response(dict(error='Already pre-registered'), status=status.HTTP_400_BAD_REQUEST)
            onborded_by = ProPlayer.objects.filter(
                user__username=request.data.get('channel')).first()
            PreRegistration.objects.create(onboarded_by=onborded_by, **request.data)
            return Response(dict(message='Pre-registration completed'))
        return Response(dict(error='Email not verified'), status=status.HTTP_400_BAD_REQUEST)


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
            email=email).first()
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


class SignupDataValidationAPI(views.APIView):

    def post(self, request: Request) -> Response:
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
        errors = list()
        if not first_name.replace(' ', '').isalpha():
            errors.append('First name must only contain letters.')
        if not last_name.replace(' ', '').isalpha():
            errors.append('Last name must only contain letters.')
        if User.objects.filter(username=username).exists():
            errors.append('Username already exists.')
        if User.objects.filter(email=email).exists():
            errors.append('Email already exists.')
        # if not EmailVerification.objects.filter(email=email, is_verified=True).exists():
        #     errors.append('Email is not verified.')
        if password.__len__() < 8:
            errors.append('Password must be of at least 8 characters.')
        
        is_valid = errors.__len__() == 0
        if is_valid:
            return Response(dict(isValid=True))
        else:
            return Response(dict(isValid=False, errors=errors))


class UsernameValidationAPI(views.APIView):

    def post(self, request: Request) -> Response:
        if User.objects.filter(
            username=request.data.get('username')).exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        return Response()
    

class TestAdressAPI(views.APIView):

    def post(self, request: Request) -> Response:
        from entrance.models import TestAdress
        addr = TestAdress.objects.create(**request.data)
        return Response(addr.details)


class ApologiesCredsUpdateAPI(views.APIView):
    
    def post(self, request: Request, private_key: str) -> Response:
        pro_onb = ProsOnboarding.objects.filter(
            private_key=private_key).first()
        if pro_onb is None:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.get(email=pro_onb.email)
        user.username = request.data.get('username')
        user.save()
        user.set_password(request.data.get('password'))
        access_token = str(RefreshToken.for_user(user).access_token)
        return Response(access_token=access_token)


class OTPSendingAPI(views.APIView):

    def post(self, request: Request) -> Response:
        user = User.objects.filter(
            email=request.data.get('email')).first()
        if user is None: return Response(status=status.HTTP_404_NOT_FOUND)
        user.codes.send_otp()
        return Response()


class PasswordResetAPI(views.APIView):

    def post(self, request: Request) -> Response:
        user = User.objects.get(email=request.data.get('email'))
        if user.codes.otp == request.data.get('otp'):
            user.set_password(request.data.get('password'))
            user.save()
            user.codes.change_otp()
            return Response(dict(username=user.username, message='Login with the new password to continue.'))
        return Response(status=status.HTTP_401_UNAUTHORIZED)