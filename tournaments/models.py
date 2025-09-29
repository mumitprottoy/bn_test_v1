from django.db import models
from player.models import User


class Tournamant(models.Model):
    INVITATIONAL = 'Invitational'; OPEN = 'Open'
    ACCESS_CHOICES = ((INVITATIONAL, INVITATIONAL), (OPEN, OPEN))
    HANDICAP = 'Handicap'; SCRATCH = 'Scratch'
    TYPE_CHOICES = ((HANDICAP, HANDICAP), (SCRATCH, SCRATCH))

    name = models.CharField(max_length=200, unique=True, default='')
    start_date = models.DateTimeField()
    reg_deadline = models.DateTimeField()
    reg_fee = models.FloatField()
    participants_count = models.IntegerField(default=1)
    lat = models.CharField(max_length=50, default='')
    long = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=300, default='')
    access_type = models.CharField(max_length=20, choices=ACCESS_CHOICES)
    tournament_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default=SCRATCH)
    average = models.IntegerField(default=200)
    percentage = models.IntegerField(default=100)

    @property
    def format(self) -> str:
        if self.participants_count == 1:
            return 'Singles'
        if self.participants_count == 2:
            return 'Doubles'
        return 'Teams'
    
    @property
    def details(self) -> dict:
        return dict(
            id=self.id,
            name=self.name,
            start_date=self.start_date,
            reg_deadline=self.reg_deadline,
            address=self.address,
            reg_fee=self.reg_fee,
            access_type=self.access_type,
            format=self.format,
            already_enrolled=self.participants.count()
        )
    
    @property
    def all_teams(self) -> list[dict]:
        return [p.details for p in self.participants.all()]
    
    def save(self, *args, **kwargs) -> None:
        if self.participants_count not in range(1,6):
            raise ValueError('Invalid participant count. Max: 5; Min: 1.')
        super().save(*args, **kwargs)


class ParticipantSet(models.Model):
    tournament = models.ForeignKey(
        Tournamant, on_delete=models.CASCADE, related_name='participants')
    name = models.CharField(max_length=200, default='')
    profile_picture = models.URLField(max_length=200, default='')

    @property
    def details(self) -> list:
        return dict(
            display_name=self.name,
            profile_picture=self.profile_picture,
            players = [m.user.basic for m in self.members.all()]
        )
        
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['tournament', 'name'],
                name='unique_name_in_tournament'
            )
        ]


class ParticipantMember(models.Model):
    participant_set = models.ForeignKey(
        ParticipantSet, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self._state.adding:
            tournament = self.participant_set.tournament
            for participant in tournament.participants.all():
                if participant.members.filter(user=self.user).exists():
                    raise ValueError('User already exists in this tournament')
        super().save(*args, **kwargs)


class ScratchTournament(models.Model):
    tournament = models.OneToOneField(
        Tournamant, on_delete=models.CASCADE, related_name='scratch')
    average = models.IntegerField(default=200)


class HandicapTournament(models.Model):
    tournament = models.OneToOneField(
        Tournamant, on_delete=models.CASCADE, related_name='handicap'
    )
    percentage = models.IntegerField(default=90)
    average = models.IntegerField(default=200)
