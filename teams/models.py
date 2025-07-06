from django.db import models
from player.models import User
from utils import constants as const


class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    logo_url = models.TextField(default='https://i.imgur.com/QMJ67hC.png')
    created_by = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_creator(self, user: User) -> bool:
        return user == self.created_by

    @property
    def member_count(self) -> int:
        return self.members.count()
    
    @property
    def member_list(self) -> list[dict]:
        return [dict(
            member_id=member.id,
            member=member.user.basic,
            is_creator=self.created_by == member.user
            ) for member in self.members.all()]
    
    @property
    def member_details(self) -> dict:
        return dict(
            member_count=self.member_count,
            members=self.member_list
        )
    
    @property
    def details(self) -> dict:
        return dict(
            team_id=self.id,
            name=self.name,
            logo_url=self.logo_url,
            created_by=self.created_by.basic,
            created_at=self.created_at.strftime(const.DATE_STR_FORMAT_1)
        )

    def __str__(self) -> str:
        return self.name


class TeamMember(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teams')

    def __str__(self) -> str:
        return f'{self.user.username} - {self.team.name}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('team', 'user'), name='unique_member')
        ]


class TeamInvitation(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invites')
    invited_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='myinvites')
    is_accepted = models.BooleanField(default=False)

    def accept(self) -> None:
        self.is_accepted = True
        TeamMember.objects.get_or_create(team=self.team, user=self.invited_user)
        self.save()
    
    @property
    def details(self) -> dict:
        return dict(
            invitation_id=self.id,
            team=self.team.details
        )
    
    def __str__(self) -> str:
        return f'{self.invited_user.username} - {self.team.name} | Accepted: [{self.is_accepted}]'
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=('team', 'invited_user'), name='unique_invites')
        ]  
