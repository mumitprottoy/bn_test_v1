import time
from django.db import models
from player.models import User
from utils.keygen import KeyGen
from emailsystem.engine import EmailEngine


def get_key() -> str: return KeyGen().timestamped_alphanumeric_id(20)

class BetaTester(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    private_key=models.CharField(max_length=100, default=get_key)

    @property
    def access_url(self) -> str:
        return f'https://beta.bowlersnetwork.com/private-access/{self.private_key}'

    @classmethod
    def create(
        cls: 'BetaTester', first_name: str, last_name: str, email: str) -> 'BetaTester':
        created = False
        user = User.objects.filter(email=email)
        if user.exists():
            user.update(first_name=first_name, last_name=last_name)
            user=user.first()
        else:
            user = User.objects.create(
                first_name=first_name,
                last_name=last_name,
                username=KeyGen().alphanumeric_key(20),
                email=email
            )
            created = True

        tester, _ = cls.objects.get_or_create(user=user)
        if created:
            user.username = f'beta_tester_{tester.id}'
            user.save()
        
        return tester
    
    @classmethod
    def send_emails_to_all(
        cls: 'BetaTester', subject: str, template: str, context: dict=dict(), test: bool=False) -> None:
        _context = context.copy()
        connection = EmailEngine([], subject, template).get_connection_only()
        connection.open()
        batch_size = 50
        testers = list(cls.objects.all())
        
        if test:
            user = User.objects.get(email='mumitprottoy@gmail.com')
            tester, _ = cls.objects.get_or_create(user=user)
            testers = [tester]

        for i, tester in enumerate(testers):
            _context.update(dict(
                full_name=tester.user.get_full_name(),
                access_url=tester.access_url
            ))
            
            engine = EmailEngine(
                recipient_list=[tester.user.email],
                subject=subject,
                template=template,
                context=_context,
            )
            email_obj = engine.setup_email(connection)
            email_obj.send()

            if (i + 1) % batch_size == 0:
                connection.close()
                time.sleep(1)
                connection.open()

            print(f'{i + 1} / {testers.__len__()} Sent to: {tester.user.email}')

    def __str__(self) -> str:
        return self.user.get_full_name()
