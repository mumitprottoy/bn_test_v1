from django.test import TestCase
from pros.models import ProPlayer
from player.models import User
from posts.models import PostMetaData
from interface import stats

def test_engagement_stats():
    uri = User.objects.get(username='Uri')
    pro = ProPlayer.objects.get(user=uri)
    posts = PostMetaData.objects.filter(user=uri)
    engagement = stats.EngagementStats
    
    class A:
        def __init__(self):
            self.user = uri
            self.pro = pro
            self.posts = posts
            self.enagement = engagement
    
    return A()

if __name__ == '__main__':
    # test_scores()
    pass