from django.db import models
from django.utils import timezone as tz
from player.models import User
from utils import keygen as kg, subroutines as sr


def generate_uid() -> str:
    return kg.KeyGen().timestamped_alphanumeric_id()


class PointWeight(models.Model):
    name = models.CharField(max_length=7, default='default')
    amateur_weight = models.IntegerField(default=1)
    pro_weight = models.IntegerField(default=5)

    @classmethod
    def default(cls: 'PointWeight') -> 'PointWeight':
        return cls.objects.first() if cls.objects.exists() else None

    def save(self, *args, **kwargs) -> None:
        if self._state.adding and self.__class__.objects.exists():
            raise PermissionError()
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name 


class DiscussionTopic(models.Model):
    topic = models.CharField(max_length=20, unique=True)
    description = models.TextField()

    @property
    def details(self) -> str:
        return sr.get_clean_dict(self)
    
    @classmethod
    def all_topics(cls: 'DiscussionTopic') -> list[dict]:
        return [t.details for t in cls.objects.all()]

    def __str__(self) -> str:
        return self.topic


class Discussion(models.Model):
    topic = models.ForeignKey(
        DiscussionTopic, on_delete=models.CASCADE, related_name='discussions')
    uid = models.CharField(max_length=50, unique=True, default=generate_uid)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='discussions')
    title = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    def vote(self, voter: User, is_upvote: bool) -> dict:
        v, _ = self.votes.get_or_create(voter=voter)
        v.is_upvote = is_upvote
        v.save()
        return dict(
            point_str=self.__class__.point_str(self.point)
        )
    
    @property
    def is_upvoted_by_the_pros(self) -> bool:
        for vote in self.votes.all():
            if hasattr(vote.voter, 'pro'):
                return True
        return False

    @property
    def point(self) -> int:
        return sum([v.point for v in self.votes.all()])
    
    @classmethod
    def point_str(cls: 'Discussion', point: int) -> str:
        if point > 0: return f'+ {point}'
        return f'{point}'

    @property
    def details(self) -> dict:
        point = self.point
        return dict(
            discussion_id=self.id,
            uid=self.uid,
            title=self.title,
            description=self.description,
            created=sr.pretty_timesince(self.created_at),
            edited=sr.pretty_timesince(self.last_edited),
            is_edited=self.is_edited,
            is_upvoted_by_the_pros=self.is_upvoted_by_the_pros,
            point=point,
            point_str=self.__class__.point_str(point),
            author=self.user.minimal,
            opinions=[o.details for o in self.opinions.all()]
        )

    def details_for_user(self, user: User) -> dict:
        details = self.details.copy()
        vote = self.votes.filter(voter=user).first()
        if vote is not None: vote = vote.is_upvote
        details.update(dict(
            viewer_is_author=self.user.id == user.id,
            viewer_vote=vote,
            opinions=[o.details_for_user(user) for o in self.opinions.all()]
        ))
        return details

    def save(self, *args, **kwargs) -> None:
        if not self._state.adding:
            self.is_edited = True
        super().save(*args, **kwargs)
    

class DiscussionVote(models.Model):
    UP_VOTE = 1; DOWN_VOTE = -1

    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='votes')
    is_upvote = models.BooleanField(default=True)

    @property
    def point(self) -> int:
        factor = 1
        if hasattr(self.voter, 'pro'):
            weight = PointWeight.default()
            factor = weight.pro_weight if weight is not None else factor
        value = self.UP_VOTE if self.is_upvote else self.DOWN_VOTE
        return value * factor
    

class DiscussionOpinion(models.Model):
    discussion = models.ForeignKey(
        Discussion, on_delete=models.CASCADE, related_name='opinions')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    opinion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_edited = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    def vote(self, voter: User, is_upvote: bool) -> dict:
        v, _ = self.votes.get_or_create(voter=voter)
        v.is_upvote = is_upvote
        v.save()
        return dict(
            point_str=Discussion.point_str(self.point)
        )
    
    @property
    def is_upvoted_by_the_pros(self) -> bool:
        for vote in self.votes.all():
            if hasattr(vote.voter, 'pro'):
                return True
        return False
    

    @property
    def point(self) -> int:
        return sum([v.point for v in self.votes.all()])

    @property
    def details(self) -> dict:
        point = self.point
        return dict(
            opinion_id=self.id,
            opinion=self.opinion,
            created=sr.pretty_timesince(self.created_at),
            edited=sr.pretty_timesince(self.last_edited),
            is_edited=self.is_edited,
            is_upvoted_by_the_pros=self.is_upvoted_by_the_pros,
            point=point,
            point_str=Discussion.point_str(point),
            author=self.user.minimal 
        )
    
    def details_for_user(self, user: User) -> dict:
        details = self.details.copy()
        vote = self.votes.filter(voter=user).first()
        if vote is not None: vote = vote.is_upvote
        details.update(dict(
            viewer_is_author=self.user.id == user.id,
            viewer_vote=vote,
        ))
        return details


class DiscussionOpinionVote(models.Model):
    UP_VOTE = 1; DOWN_VOTE = -1

    opinion = models.ForeignKey(
        DiscussionOpinion, on_delete=models.CASCADE, related_name='votes')
    voter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='opinion_votes')
    is_upvote = models.BooleanField(default=True)

    @property
    def point(self) -> int:
        factor = 1
        if hasattr(self.voter, 'pro'):
            weight = PointWeight.default()
            factor = weight.pro_weight if weight is not None else factor
        value = self.UP_VOTE if self.is_upvote else self.DOWN_VOTE
        return value * factor    
