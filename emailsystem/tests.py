import random
from .engine import EmailEngine


def test_email(email='mumitprottoy@gmail.com', full_name='Mumit Prottoy') -> None:
    verification_code = random.randint(176524, 984561)
    context = dict(code=verification_code, full_name=full_name)
    subject = f'Your Email Verification Code [{verification_code}]'
    engine = EmailEngine(
        recipient_list=[email],
        subject=subject,
        template='emails/verification_code.html',
        context=context
    )
    _count = engine.send(fail_silently=False)
    print(_count)


def test_invite_email(first_name, last_name, email):
    pass


