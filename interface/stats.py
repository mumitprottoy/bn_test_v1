from django.db.models import QuerySet
from player.models import User
from premium.models import Premium
from posts.models import PostMetaData


class PostStats:

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
