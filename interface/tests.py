from django.test import TestCase

from .weighted_index import WeightedIndex
from pros.models import ProPlayer


def test_scores():
    query_set = ProPlayer.objects.all()

    index = WeightedIndex(query_set)
    print(index.scores)


if __name__ == '__main__':
    test_scores()