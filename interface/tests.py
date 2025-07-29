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


def create_team_rooms() -> None:
    from teams.models import Team
    from chat.models import Room, RoomMate

    for team in Team.objects.all():
        room, _ = Room.objects.get_or_create(name=team.name, room_type=Room.GROUP)
        for member in team.members.all():
            RoomMate.objects.get_or_create(room=room, user=member.user)


if __name__ == '__main__':
    # test_scores()
    pass