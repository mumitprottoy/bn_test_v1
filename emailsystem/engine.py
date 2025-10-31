from django.core.mail import EmailMultiAlternatives, get_connection
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import EmailConfig, EmailCred

DEFAULT_CONFIG = 'google'
SYSTEM_CRED_KEY = 'system'
ATTACHMENT_MIME_TYPE = 'text/html'


class EmailEngine:
    
    def __init__(
            self, 
            recipient_list: list[str],
            subject: str,
            template: str,
            context: dict=dict(),
            display_name = 'BowlersNetwork',
            config_name: str=DEFAULT_CONFIG,
            cred_key: str=SYSTEM_CRED_KEY 
        ):
        self.config = EmailConfig.objects.get(name=config_name)
        self.cred = EmailCred.objects.get(key=cred_key)
        self.display_name=display_name
        self.recipient_list = recipient_list
        self.subject = subject
        self.template = template
        self.context = context
    
    def __get_sender_email(self) -> str:
        return f'{self.display_name} <{self.cred.email}>'

    def connect(self):
        connection_kwargs = self.config.connection_kwargs
        connection_kwargs.update(self.cred.connection_kwargs)
        return get_connection(**connection_kwargs)
    
    def setup_email(self) -> EmailMultiAlternatives:
        connection = self.connect()
        html_content = render_to_string(self.template, self.context)
        text_content = strip_tags(html_content)
        email = EmailMultiAlternatives(
            subject=self.subject,
            body=text_content,
            from_email=self.__get_sender_email(),
            to=self.recipient_list,
            connection=connection
        )
        email.attach_alternative(html_content, 'text/html')

        return email

    def send(self, fail_silently=True) -> int:
        email = self.setup_email()
        return email.send(fail_silently=fail_silently)