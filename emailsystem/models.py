from django.db import models


class EmailConfig(models.Model):
    name = models.CharField(max_length=20, unique=True, default='default', editable=False)
    backend = models.CharField(
        max_length=100, default='django.core.mail.backends.smtp.EmailBackend', editable=False)
    host = models.CharField(max_length=100, default='smtp.hostinger.com', editable=False)
    port = models.IntegerField(default=587, editable=False)
    use_tls = models.BooleanField(default=True, editable=False)

    @classmethod
    def get_default(cls) -> 'EmailConfig':
        return cls.objects.get_or_create(
            name='default',
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='smtp.hostinger.com',
            port=587,
            use_tls=True
        )[0]
    
    def __str__(self) -> str:
        return self.name


class EmailCred(models.Model):
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name_plural = 'Email Credentials'