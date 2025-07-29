import random
from .engine import EmailEngine


def test_email() -> None:
    verification_code = random.randint(176524, 984561)
    context = dict(code=verification_code, full_name='Mumit Prottoy')
    subject = f'Your Email Verification Code [{verification_code}]'
    engine = EmailEngine(
        recipient_list=['mumitprottoy@gmail.com'],
        subject=subject,
        template='emails/verification_code.html',
        context=context
    )
    _count = engine.send(fail_silently=False)
    print(_count)


if __name__ == '__main__':
    test_email()
