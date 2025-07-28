from django.apps import AppConfig


class EmailsystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'emailsystem'

    def ready(self):
        try:
            from .models import EmailConfig
            EmailConfig.get_default()
        except: pass

