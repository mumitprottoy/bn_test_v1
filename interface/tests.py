from django.test import TestCase

from .weighted_index import WeightedIndex
from .posts import PostStats
from pros.models import ProPlayer
from player.models import User
from posts.models import PostMetaData

def test_scores():
    query_set = ProPlayer.objects.all()

    index = WeightedIndex(query_set)
    print(index.scores)


def test_stats():
    user = User.objects.filter(username='Uri').first()
    query_set = PostMetaData.objects.filter(user=user)
    stats = PostStats(query_set).stats
    print(stats)

if __name__ == '__main__':
    # test_scores()
    test_stats()