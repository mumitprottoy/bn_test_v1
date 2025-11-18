import time
from beta.models import BetaTester
from habijabi.models import ProsOnboarding
from emailsystem.engine import EmailEngine

emails = [bt.user.email for bt in BetaTester.objects.all()] + [po.email for po in ProsOnboarding.objects.all()]
emails = list(set(emails))

subject = "Temporary Service Disruption Due to Cloudflare Outage"
template = 'emails/service_outage.html'

def send():
    connection = EmailEngine([], subject, template).get_connection_only()
    for i, email in enumerate(emails):
        engine = EmailEngine(
            recipient_list=emails,
            subject=subject,
            template=template
        )
        engine.setup_email(connection)
        engine.send()

        print(f'{i} / {emails.__len__()} Sent to: {email}')

        if (i + 1) % 50 == 0:
            connection.close()
            time.sleep(1)
            connection.open()
        
    