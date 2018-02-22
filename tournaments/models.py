import os
from datetime import datetime

from django.db import models
# Create your models here.
from django.db.models import Sum
from django.utils.crypto import get_random_string
from djchoices import DjangoChoices, ChoiceItem

from accounts.models import PlayerInfo


# todo enum
class TournamentType(DjangoChoices):
    # choices
    CLUB_LICENSE = ChoiceItem('C', 'Только для обладателей клубной лицензии')
    GAME_LICENSE = ChoiceItem('G', 'Только для обладателей игровой лицензии')
    ANY_LICENSE = ChoiceItem('L', 'Для обладателей любой лицензии')
    PUBLIC = ChoiceItem('P', "Публичный")


def filename(instance, filename):
    return os.path.join('tournaments', get_random_string(length=32) + '.' + filename.split('.')[-1])


class Tournament(models.Model):
    name = models.CharField(max_length=40)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField(max_length=500, blank=True, default='')
    type = models.CharField(max_length=1, choices=TournamentType.choices)
    team_type = models.ForeignKey('TeamType')
    games = models.IntegerField('amount of games in the tournament', default=1)
    photo = models.ImageField(upload_to=filename, blank=True)
    players = models.ManyToManyField(PlayerInfo, through='TournamentMembership')

    def __str__(self):
        return self.name

    def get_player_points(self, player):
        games = Game.objects.filter(tournament=self)
        info = GameInfo.objects.filter(game__in=games, player=player)
        return info.aggregate(Sum('result'))['result__sum']


class TournamentMembership(models.Model):
    player = models.ForeignKey(PlayerInfo, on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)


class TeamType(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Game(models.Model):
    start = models.DateTimeField(default=datetime.now)
    name = models.CharField(max_length=200, blank=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='tournament_games')
    players = models.ManyToManyField(PlayerInfo, through='GameInfo')

    def __str__(self):
        return self.name


class GameInfo(models.Model):
    player = models.ForeignKey(PlayerInfo, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    result = models.IntegerField(default=0)
