from django.db import models
from player.models import User
from utils import keygen as kg, subroutines as sr, constants as const


def generate_uid() -> str:
    return kg.KeyGen().timestamped_alphanumeric_id(head_len=30)


class LargeVideo(models.Model):
    uid = models.CharField(unique=True, max_length=150, default=generate_uid)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='large_videos')
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(default='')
    url = models.CharField(unique=True, max_length=200)
    thumbnail_url = models.CharField(null=True, default=const.DEFAULT_THUMBNAIL, max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    duration = models.FloatField(default=0.0)

    @classmethod
    def validate_video_metadata(cls: 'LargeVideo', **kwargs) -> bool:
        return not cls.objects.filter(**kwargs).exists()
    
    @property
    def likes_count(self) -> int:
        return self.likes.count()
    
    @property
    def all_comments(self) -> list[dict]:
        return [c.details for c in self.comments.all().order_by('-id')]
    
    def toggle_privacy(self) -> dict:
        self.is_public = not self.is_public
        self.save()
        return dict(is_public=self.is_public)
    
    @property
    def duration_str(self) -> str:
        t = self.duration
        h=int(t//3600);m=int(t%3600//60);s=int(t%60)
        return f'{h:02d}:{m:02d}:{s:02d}' if h else f'{m:02d}:{s:02d}'

    @property
    def details(self) -> dict:
        return dict(
            id=self.id,
            uid=self.uid,
            title=self.title,
            description=self.description,
            url=self.url,
            thumbnail_url=self.thumbnail_url,
            duration_str=self.duration_str,
            uploaded=sr.pretty_timesince(self.uploaded_at),
            is_public=self.is_public,
            likes_count=self.likes_count,
            comments=self.all_comments
        )
    
    def details_for_user(self, user: User) -> dict:
        details = self.details
        details.update(dict(
            viewer_liked=self.likes.filter(user=user).exists()))
        return details
    
    def __str__(self) -> str:
        return self.title


class LargeVideoLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    large_video = models.ForeignKey(
        LargeVideo, on_delete=models.CASCADE, related_name='likes')


class LargeVideoComment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    large_video = models.ForeignKey(
        LargeVideo, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def details(self) -> dict:
        return dict(
            large_video_id=self.large_video.id,
            comment_id=self.id,
            comment=self.comment,
            user=self.user.minimal,
            created=sr.pretty_timesince(self.created_at)
        )
