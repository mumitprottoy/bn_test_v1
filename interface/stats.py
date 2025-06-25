from django.db.models import QuerySet
from player.models import User
from premium.models import Premium
from posts.models import PostMetaData
from pros.models import ProPlayer
from entrance.models import OnBoarding
from utils import subroutines as sr
from profiles.models import Follow


class EngagementStats:

    def __init__(self, posts: QuerySet) -> None:
        self.posts = posts

    @property
    def stats(self) -> dict:
        likes = comments = shares = views = 0

        for post in self.posts:
            likes += post.total_likes
            comments += post.total_comments
            # video views and shares will be added later

        return dict(
            likes=likes,
            comments=comments,
            shares=shares,
            views=views
        )
    
    @classmethod
    def stats_of_user(cls, user: User) -> dict:
        posts = PostMetaData.objects.filter(user=user)
        return cls(posts).stats
    
    @property
    def value(self) -> int:
        return sum(list(self.stats.values()))
    
    @classmethod
    def value_of_user(cls, user: User) -> int:
        posts = PostMetaData.objects.filter(user=user)
        return cls(posts).value


class OnboardingStats:

    def __init__(self, pro: ProPlayer) -> None:
        self.pro = pro
        self.user_set = [ob.user for ob in OnBoarding.objects.filter(
            channel=self.pro.user)]
        self.user_count = self.user_set.__len__()
        self.premium_users = Premium.objects.filter(
            user__in=self.user_set)
        self.premium_user_count = self.premium_users.count()
    
    @property
    def conversion_rate(self) -> float:
        return round((
            self.premium_user_count / self.user_count) * 100, 2) if self.user_count > 0 else 0.0

    @property
    def numeric_stats(self) -> dict:
        return dict(
            onboarded_user_count=self.user_count,
            free_users=self.user_count - self.premium_user_count,
            premium_user_count=self.premium_user_count,
            conversion_rate=self.conversion_rate
        )
    
    @property
    def users(self) -> dict:
        return dict(
            onboarded_users = [sr.get_clean_dict(user) for user in self.user_set],
            premium_users = [
                sr.get_clean_dict(premium.user) for premium in self.premium_users]
        )
    

class ProPlayerWeightedIndex:

    def __init__(self) -> None:
        self.pro_players = ProPlayer.objects.all()
        self.pro_players_user_set = User.objects.filter(username__in=[
            [pro.user.username for pro in self.pro_players]])
        self.pro_players_user_list = list(self.pro_players_user_set)
        self.total_free_user_count = sum([
            OnboardingStats(pro).user_count for pro in self.pro_players])
        self.total_premium_user_count = sum([
            OnboardingStats(pro).premium_user_count for pro in self.pro_players])
        self.all_pro_players_engagement_value = self.count_all_pro_players_engagement_value()
        self.free_user_wight = 0.3
        self.premium_user_weight = 0.4
        self.enagament_weight = 0.3
    
    def get_engagement_value(self, users: QuerySet) -> int:
        posts = PostMetaData.objects.filter(user__in=users)
        return EngagementStats(posts).value
    
    def count_pro_player_engagement_value(self, pro: ProPlayer) -> int:
        return self.get_engagement_value(
            self.pro_players_user_set.filter(
                username=pro.user.username))
    
    def count_all_pro_players_engagement_value(self) -> int:
        return self.get_engagement_value(self.pro_players_user_set)
    
    def free_user_index(self, pro: ProPlayer) -> float:
        free_user_count = OnboardingStats(pro).user_count
        return round((
            free_user_count / self.total_free_user_count)
              * self.free_user_wight * 100, 2) if self.total_free_user_count > 0 else 0.0
    
    def premium_user_index(self, pro: ProPlayer) -> float:
        premium_user_count = OnboardingStats(pro).premium_user_count
        return round((
            premium_user_count / self.total_premium_user_count)
              * self.premium_user_weight * 100, 2) if self.total_premium_user_count > 0 else 0.0

    def engagement_index(self, pro: ProPlayer) -> float:
        engagement_value = self.count_pro_player_engagement_value(pro)
        return round(
            (engagement_value / self.all_pro_players_engagement_value)
              * self.engagement_index * 100, 2) if self.all_pro_players_engagement_value > 0 else 0.0
    
    def compute_weighted_index(self, pro: ProPlayer) -> float:
        return round(sum((self.free_user_index(pro),
                   self.premium_user_index(pro),
                   self.engagement_index(pro))
                ), 2)
    
    def get_weighted_index_map(self, pro: ProPlayer) -> dict:
        return dict(
            user=pro.user.basic,
            index=self.compute_weighted_index(pro)
        )

    def get_all_weighted_indices_map(self) -> list[dict]:
        return sorted([self.get_weighted_index_map(pro)
            for pro in self.pro_players], 
            key=lambda _:_['index'], 
            reverse=True
        )


class FollowerStat:

    def __init__(self, pro_player: ProPlayer) -> None:
        self.pro_player = pro_player

    @property
    def follower_count(self) -> int:
        return Follow.get_followers(user=self.pro_player.user).count()
    
    @property
    def followers(self) -> dict:
        return dict(
            follower_count=self.follower_count,
            followers=[
                follower.basic for follower in Follow.get_followers(
                    user=self.pro_player.user)]
        )
    

def get_dashboard_data(pro_player: ProPlayer) -> dict:
    data = dict(user_id=pro_player.user.id)
    data.update(EngagementStats.stats_of_user(pro_player.user))
    data.update(dict(
        follower_count=FollowerStat(pro_player).follower_count))
    data.update(OnboardingStats(pro_player).numeric_stats)
    data.update(dict(weighted_index=ProPlayerWeightedIndex().compute_weighted_index(pro_player)))
    return data