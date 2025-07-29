import io, csv
from .libs import *
from emailsystem.engine import EmailEngine


class SendInvitesWithCSVFileAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def post(self, request: Request) -> Response:
        csv_file = request.FILES.get('csv_file')
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        data = list(reader)
        invite_link = 'https://youtube.com'
        sent_count = 0
        for _ in data:
            engine = EmailEngine(
                recipient_list=[_['email']], 
                subject='Where Bowlers Belong — Your Invite to BowlersNetwork',
                template='emails/invite.html',
                context=dict(full_name=f'{_['first_name']} {_['last_name']}', invite_link=invite_link)
                )
            sent_count += engine.send()
        return Response(dict(sent_to=f'{sent_count} people', csv_file_data=data))

