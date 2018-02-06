import os
from django.db import models

# Create your models here.
from django.utils.crypto import get_random_string

from accounts.models import PlayerInfo

TYPE = (
    ('1', 'Только для обладателей клубной лицензии'),
    ('2', 'Только для обладателей игровой лицензии'),
    ('3', 'Для обладателей любой лицензии'),
    ('4', "Публичный")
)

# todo make fixtures, export to db
# TEAM_TYPE = (
#     ('1', 'Один игрок'),
#     ('2', 'Два игрока')
# )


def filename(instance, filename):
    return os.path.join('tournaments', get_random_string(length=32) + '.' + filename.split('.')[-1])


class Tournament(models.Model):
    name = models.CharField(max_length=40)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField(max_length=500, blank=True, default='')
    type = models.CharField(max_length=1, choices=TYPE)
    team_type = models.ForeignKey('TeamType')
    games = models.IntegerField('amount of games in the tournament', default=1)
    photo = models.ImageField(upload_to=filename, blank=True)
    players = models.ManyToManyField(PlayerInfo, through='TournamentMembership')


class TournamentMembership(models.Model):
    player = models.ForeignKey(PlayerInfo, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)


class TeamType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name