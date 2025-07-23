from django.db.models import QuerySet
from posts import models
# from posts.models import User
from cloud.engine import CloudEngine


class Poster:
    
    def __init__(
        self, user: models.User, 
        caption: str | None=None,
        privacy: str='Public', # Only me, Followers
        poll: dict | None=None, 
        event: dict | None=None,
        media: list | None=None,
        tags: list=list()):
        
        self.user = user
        self.caption = caption
        self.poll = poll
        self.event = event
        self.privacy = privacy
        self.tags = tags
        self.media = media
        
    def create_metadata(self) -> models.PostMetaData:
        return models.PostMetaData.objects.create(user=self.user, privacy=self.privacy, tags=self.tags)
    
    def create_text(
        self, metadata: models.PostMetaData) -> models.PostText:
        if self.caption is not None:
            return models.PostText.objects.create(metadata=metadata, content=self.caption)
    
    def create_poll(self, metadata: models.PostMetaData) -> models.PostPoll:
        if self.poll is not None:
            poll = models.PostPoll.objects.create(
                metadata=metadata, title=self.poll['title'], poll_type=self.poll['poll_type'])

            for option in self.poll['options']:
                models.PollOption.objects.create(poll=poll, content=option)

            return poll
    
    def upload_media_content(
            self, metadata: models.PostMetaData) -> models.PostImageUrl:
        for file in self.media:
            engine = CloudEngine(file, 'media', 'mumit1')
            url = engine.upload()
            models.Pos
    
    def create_event(self, metadata: models.PostMetaData) -> models.PostEvent:
        if self.event is not None:
            return models.PostEvent.objects.create(metadata=metadata, **self.event)
    
    def create_post(self) -> models.PostMetaData:
        metadata = self.create_metadata()
        self.create_text(metadata)
        self.create_poll(metadata)
        self.create_event(metadata)
        return metadata


class PostViewer:
    
    def __init__(self, user: models.User) -> None:
        self.user = user
    
    def get_post_ids(self) -> list[int]:
        public_post_ids = [p.id for p in models.PostMetaData.objects.filter(
            privacy=models.PostMetaData.PUBLIC).order_by('-id')]
        followed = [f.followed for f in self.user.following.all()]
        followed_users_post_ids = [p.id for p in models.PostMetaData.objects.filter(
            user__in=followed).order_by('-id')]
        return list(set(public_post_ids + followed_users_post_ids))[::-1]
        
    
    def get_viewable_posts_queryset(self) -> QuerySet:
        return models.PostMetaData.objects.filter(
            id__in=self.get_post_ids()).order_by('-id')

