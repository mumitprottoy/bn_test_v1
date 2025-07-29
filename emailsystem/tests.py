import random
from .engine import EmailEngine


def test_email() -> None:
    verification_code = random.randint(176524, 984561)
    context = dict(code=verification_code)
    subject = f'Your Email Verification Code [{verification_code}]'
    engine = EmailEngine(
        recipient_list=['mumitprottoy@gmail.com'],
        subject=subject,
        template='emails/base.html',
        context=context
    )
    engine.send()


if __name__ == '__main__':
    test_email()
