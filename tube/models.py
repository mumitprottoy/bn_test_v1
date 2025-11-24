from django.db import models
from player.models import User
from utils import keygen as kg, subroutines as sr


def generate_uid() -> str:
    return kg.KeyGen().timestamped_alphanumeric_id(head_len=30)


class LargeVideo(models.Model):
    uid = models.CharField(unique=True, max_length=150, default=generate_uid)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='large_videos')
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField(default='')
    url = models.CharField(unique=True, max_length=200)
    thumbnail_url = models.CharField(null=True, default=None, max_length=200)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_public = models.BooleanField(default=True)
    duration = models.FloatField(default=0.0)

    @classmethod
    def validate_video_metadata(cls: 'LargeVideo', **kwargs) -> bool:
        return not cls.objects.filter(**kwargs).exists()
    
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
            is_public=self.is_public
        )
    
    def __str__(self) -> str:
        return self.title
