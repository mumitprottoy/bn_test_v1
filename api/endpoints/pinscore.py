import json
from .libs import *
from pinscore.models import Game


class GamesAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(Game.get_all_games(request.user))

    def post(self, request: Request) -> Response:
        game = Game.objects.create(
            user=request.user, data=json.dumps(
                request.data, indent=4, ensure_ascii=False))
        return Response(game.details)


class DeleteGameAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request: Request, game_id: int) -> Response:
        Game.objects.get(id=game_id).delete()
        return Response() 
