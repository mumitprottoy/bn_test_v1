class EmailID:

    def __init__(self, address: str, password: str) -> str:
        self.address = address
        self.password = password



EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SMTP_SERVER = 'smtp.hostinger.com'
EMAIL_PORT = 465
EMAILS = {
    'system' : {
        'address': 'system@bowlersnetwork.com',
        'password': '$y$temEm@i1bwlrntk'
    }
}

