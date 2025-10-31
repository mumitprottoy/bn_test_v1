from django.db import models


class EmailConfig(models.Model):
    name = models.CharField(max_length=20, unique=True, default='default')
    backend = models.CharField(
        max_length=100, default='django.core.mail.backends.smtp.EmailBackend')
    host = models.CharField(max_length=100, default='smtp.hostinger.com')
    port = models.IntegerField(default=587)
    use_tls = models.BooleanField(default=True)

    @classmethod
    def get_default(cls) -> 'EmailConfig':
        return cls.objects.get_or_create(
            name='google',
            backend='django.core.mail.backends.smtp.EmailBackend',
            host='smtp.gmail.com',
            port=587,
            use_tls=True
        )[0]
    
    @property
    def connection_kwargs(self) -> dict:
        return dict(backend=self.backend, host=self.host, port=self.port, use_tls=self.use_tls)
    
    def __str__(self) -> str:
        return self.name


class EmailCred(models.Model):
    key = models.CharField(max_length=20, unique=True, default='system')
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    @property
    def connection_kwargs(self) -> dict:
        return dict(username=self.email, password=self.password)

    def __str__(self) -> str:
        return self.email

    class Meta:
        verbose_name_plural = 'Email Credentials'