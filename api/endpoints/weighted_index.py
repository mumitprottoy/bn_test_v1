from .libs import *
from interface.weighted_index import WeightedIndex
from pros.models import ProPlayer


class WeightedIndexAPI(views.APIView):

    def get(self, request: Request) -> Response:
        query_set = ProPlayer.objects.all()
        index = WeightedIndex(query_set)
        return Response(dict(indices=index.ranked_score_map), status=status.HTTP_200_OK)
