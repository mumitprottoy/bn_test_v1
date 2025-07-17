from django.db import models
from player.models import User
from utils.constants import DATETIME_STR_FORMAT_1


class FeedbackType(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self) -> str:
        return self.name


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feedback_type = models.ForeignKey(
        FeedbackType, on_delete=models.CASCADE, related_name='feedbacks')
    title = models.CharField(max_length=100, unique=True)
    details = models.TextField()
    dealt_with = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def feedback_details(self) -> dict:
        return dict(
            feedback_id = self.id,
            posted_by=self.user.minimal,
            feedback_type=self.feedback_type.name,
            title=self.title,
            details=self.details,
            dealt_with=self.dealt_with,
            posted_at=self.created_at.strftime(DATETIME_STR_FORMAT_1)
        )
    
    @classmethod
    def feedback_by_type(cls) -> list[dict]:
        feedbacks = dict()
        for ft in FeedbackType.objects.all():
            feedbacks[ft.name] = [
                f.feedback_details for f in cls.objects.filter(
                    feedback_type=ft)]
        
        return feedbacks

    def __str__(self) -> str:
        return f'[{self.feedback_type.name}] {self.user.username} : {self.title}'
