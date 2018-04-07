import os
from datetime import datetime

from django.db import models
# Create your models here.
from django.db.models import Sum, Max, Min
from django.utils.crypto import get_random_string

from accounts.models import PlayerInfo, City


def filename(instance, filename):
    return os.path.join('tournaments', get_random_string(length=32) + '.' + filename.split('.')[-1])


class TournamentType(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Tournament(models.Model):
    name = models.CharField(max_length=40)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField(max_length=500, blank=True, default='')
    type = models.ForeignKey(TournamentType)
    team_type = models.ForeignKey('TeamType')
    photo = models.ImageField(upload_to=filename, blank=True, default=os.path.join('default', 'tournament_avatar.png'))
    players = models.ManyToManyField(PlayerInfo, through='TournamentMembership')
    # Значение по умолчанию - Казань
    city = models.ForeignKey(City, default=5139)

    def __str__(self):
        return self.name

    def get_player_points(self, player):
        """
        Возвращает сумму очков, набранную игроком за весь турнир.
        Если игр нет, возвращает 0.
        """
        games = Game.objects.filter(tournament=self)
        info = GameInfo.objects.filter(game__in=games, player=player)

        points = info.aggregate(Sum('result'))['result__sum']
        return points if points else 0

    def get_player_max_points(self, player):
        """
        Возвращает максимальное количество очков, которые игрок набрал в рамках игр данного турнира.
        Если игр нет, возвращает 0.
        """
        games = Game.objects.filter(tournament=self)
        info = GameInfo.objects.filter(game__in=games, player=player)

        max_points = info.aggregate(Max('result'))['result__max']
        return max_points if max_points else 0

    def get_player_min_points(self, player):
        """
        Возвращает минимальное количество очков, которые игрок набрал в рамках игр данного турнира.
        Если игр нет, возвращает 0.
        """
        games = Game.objects.filter(tournament=self)
        # todo add get_min_result method
        info = GameInfo.objects.filter(game__in=games, player=player)
        min_points = info.aggregate(Min('result'))['result__min']
        return min_points if min_points else 0

    @classmethod
    def get_by_type(clf, tournament_type):
        """
        Возвращает queryset с турнирами нужного типа
        """
        if tournament_type == 'sport':
            tournaments = Tournament.objects.filter(type__name='Спортивный')
        elif tournament_type == 'commercial':
            tournaments = Tournament.objects.filter(type__name='Коммерческий')
        elif tournament_type == 'public':
            tournaments = Tournament.objects.filter(type__name='Публичный')
        else:
            tournaments = Tournament.objects.all()
        return tournaments

    def get_games_count(self):
        return self.tournament_games.count()


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
    player = models.ForeignKey(PlayerInfo, on_delete=models.CASCADE, related_name='player_games')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='game_players')
    result = models.IntegerField(default=0)
