from profiles.models import Follow
from posts import models as post_models
from player.models import User
from pros.models import ProPlayer
from entrance.models import OnBoarding
from django.db.models import QuerySet
from utils import subroutines as sr


class Engagement:
    # weights
    FOLLOWERS = 0.50
    LIKE = 0.25
    COMMENT = 0.75
    SHARE = 1.5
    ONBOARDING = 3
    PREMIUM_CONVERSION = 5
    
    def __init__(self, pro: ProPlayer) -> None:
        self.pro = pro
        self.user = pro.user

    @property
    def follower_count(self) -> int:
        return Follow.objects.filter(
            followed=self.user).count() 
    
    @property
    def likes(self) -> int:
        post_models.PostMetaData.objects.filter(user=self.user)

    @property
    def score(self) -> int:
        like_score = comment_score = 0
        for post in post_models.PostMetaData.objects.filter(user=self.user):
            like_score += (post.total_likes * self.LIKE)
            comment_score += (post.total_comments * self.COMMENT)
        follower_score = self.follower_count * self.FOLLOWERS
        onboarding_score = OnBoarding.objects.filter(
            channel=self.user).count() * self.ONBOARDING

        return sum([
            like_score,
            comment_score,
            follower_score,
            onboarding_score
        ])
    

class WeightedIndex:

    def __init__(self, pro_players: QuerySet) -> None:
        self.pro_players = pro_players
    
    @property
    def scores(self) -> list[dict]:
        score_list = list()
        for pro in self.pro_players:
            engagement = Engagement(pro)
            score_list.append(dict(
                user=sr.get_clean_dict(pro.user),
                score=engagement.score
            ))
        return score_list

    
