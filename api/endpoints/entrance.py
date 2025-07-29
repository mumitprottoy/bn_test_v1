import io, csv
from .libs import *


class SendInvitesWithCSVFileAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [parsers.FormParser, parsers.MultiPartParser]

    def post(self, request: Request) -> Response:
        csv_file = request.FILES.get('csv_file')
        decoded_file = csv_file.read().decode('utf-8')
        io_string = io.StringIO(decoded_file)
        reader = csv.DictReader(io_string)
        data = list(reader)
        return Response(data)

