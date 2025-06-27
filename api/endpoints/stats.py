from .libs import *
from player.models import Statistics
from utils import subroutines as sr
from interface import stats
from posts.models import PostMetaData
from profiles.models import Follow


class GameStatsAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        Statistics.objects.filter(
            user=request.user).update(**request.data)
        return Response(sr.get_clean_dict(request.user.stats), status=status.HTTP_200_OK)
    
    def get(self, request: Request) -> Response:
        return Response(sr.get_clean_dict(request.user.stats), status=status.HTTP_200_OK)
    

class EngagementStatsAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        query_set = PostMetaData.objects.filter(user=request.user)
        return Response(stats.EngagementStats(query_set).stats, status=status.HTTP_200_OK)


class FollowAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request: Request) -> Response:
        followed = User.objects.get(id=int(request.data['user_id']))
        follow, created = Follow.objects.get_or_create(
            followed=followed, follower=request.user)
        if not created: follow.delete()
        return Response(dict(message={
            True: f'Followed this user with id: {request.data['user_id']}',
            False: f'Unfollowed this user with id: {request.data['user_id']}',
        }[created]), status=status.HTTP_200_OK)


class FollowerCountAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(
            dict(
            follower_count=Follow.objects.filter(followed=request.user).count()),
            status=status.HTTP_200_OK
        )


class FollowersAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        followers = Follow.get_followers(request.user)
        return Response(dict(
            follower_count=followers.count(),
            followers=[sr.get_clean_dict(f.follower) for f in followers] 
        ), status=status.HTTP_200_OK)


class SelfWeightedIndexAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        pro_player = stats.ProPlayer.objects.get(user=request.user)
        index = stats.ProPlayerWeightedIndex().compute_weighted_index(pro_player)
        return Response(dict(weighted_index=index), status=status.HTTP_200_OK)


class WeightedIndexLeaderBoard(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        return Response(
            dict(
                leaderboard=stats.ProPlayerWeightedIndex().get_all_weighted_indices_map()),
            status=status.HTTP_200_OK
            )

class ProDashboardAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        pro_player = stats.ProPlayer.objects.get(user=request.user)
        return Response(stats.get_dashboard_data(pro_player), status=status.HTTP_200_OK)
