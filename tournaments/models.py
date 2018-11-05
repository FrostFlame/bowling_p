import os
from datetime import datetime

from django.db import models
# Create your models here.
from django.db.models import Max, Min, Sum
from django.utils.crypto import get_random_string

from accounts.models import PlayerInfo, City


def filename(instance, filename):
    return os.path.join('tournaments', get_random_string(length=32) + '.' + filename.split('.')[-1])


class TournamentType(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class TournamentMembership(models.Model):
    player = models.ForeignKey(PlayerInfo, on_delete=models.CASCADE)
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE)


class Tournament(models.Model):
    class Meta:
        verbose_name_plural = 'Турниры'

    name = models.CharField(max_length=100)
    start = models.DateTimeField()
    end = models.DateTimeField()
    description = models.TextField(max_length=500, blank=True, default='')
    type = models.ForeignKey(TournamentType)
    team_type = models.ManyToManyField('TeamType')
    photo = models.ImageField(upload_to=filename, blank=True, default=os.path.join('default', 'tournament_avatar.png'))
    # Значение по умолчанию - Казань
    city = models.ForeignKey(City, default=5139)
    handicap = models.BooleanField(default=False)
    handicap_size = models.IntegerField(default=8)
    players = models.ManyToManyField(PlayerInfo, related_name='tournament_players', through=TournamentMembership)
    block_type = models.ForeignKey('BlockType', on_delete=models.CASCADE, related_name='block_type')

    def __str__(self):
        return self.name

    def get_player_points(self, player):
        """
        Возвращает сумму очков, набранную игроком за весь турнир.
        Если игр нет, возвращает 0.
        """
        blocks = self.blocks.all()
        if player.license != '':
            for block in blocks:
                pass
        else:
            for block in blocks:
                pass
        # info = GameInfo.objects.filter(game__in=games, player=player)

        # points = info.aggregate(Sum('points'))['result__sum']
        # return points if points else 0
        return 0

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

    # def get_sorted_rating(self):
    #     """
    #     Возвращает упорядоченный по количеству убывания очков словарь игроков с суммой очков
    #     """
    #     players = self.players.all()
    #     players_points = dict()
    #     for player in players:
    #         games = Game.objects.filter(tournament=self)
    #         info = GameInfo.objects.filter(game__in=games, player=player)
    #         points = info.aggregate(Sum('result'))['result__sum']
    #         points = 0 if points is None else points
    #         players_points.update({str(player): points})
    #     players_points = sorted(players_points.items(), key=operator.itemgetter(1), reverse=True)
    #     return players_points

    # def get_rating_points(self, player):
    #     """
    #     Переводим место в турнире в количество очков в рейтинге
    #     """
    #     rating = self.get_sorted_rating()
    #     for r in rating:
    #         if str(player) in r:
    #             position = rating.index(r) + 1
    #             return position_to_points(position)
    #     return 0

    @classmethod
    def get_by_type(clf, tournament_type):
        """
        Возвращает queryset с турнирами нужного типа
        """
        if tournament_type == 'sport':
            tournaments = Tournament.objects.filter(type__name='Спортивный')
        elif tournament_type == 'commercial':
            tournaments = Tournament.objects.filter(type__name='Коммерческий')
        elif tournament_type == 'both':
            tournaments = Tournament.objects.filter(type__name='Спортивный и коммерческий')
        else:
            tournaments = Tournament.objects.all()
        return tournaments

    @classmethod
    def ordered_by_creation(cls, amount=0, reversed=True, page=1):
        if amount == 0:
            amount = Tournament.objects.count()
        if not reversed:
            return Tournament.objects.order_by('start').values('id', 'name', 'photo', 'start')[
                   (page - 1) * amount:page * amount]
        else:
            return Tournament.objects.order_by('-start').values('id', 'name', 'photo', 'start')[
                   (page - 1) * amount:page * amount]


class Team(models.Model):
    number = models.IntegerField()
    count = models.IntegerField(default=1)
    type = models.ForeignKey('TeamType', on_delete=models.CASCADE)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='teams')
    players = models.ManyToManyField(PlayerInfo, related_name='team')

    def __str__(self):
        return ', '.join(str(player) for player in self.players.all())


class TeamType(models.Model):
    class Meta:
        verbose_name_plural = 'Типы команд'

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class BlockType(models.Model):
    class Meta:
        verbose_name_plural = 'Типы блоков'

    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Block(models.Model):
    name = models.CharField(max_length=200, blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    creation_date = models.DateTimeField(default=datetime.now)
    description = models.TextField(max_length=500, blank=True, default='')
    is_final = models.BooleanField(default=False)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='blocks')
    players = models.ManyToManyField(PlayerInfo, related_name='block')

    def get_player_points(self, player):
        """
        Возвращает сумму очков, набранную игроком за весь блок.
        Если игр нет, возвращает 0.
        """
        games = Game.objects.filter(block=self)
        info = GameInfo.objects.filter(game__in=games, team=player.get_team(tournament=self.tournament, count=1))

        points = info.aggregate(Sum('point'))['point__sum']
        if points and self.tournament.handicap and (
                player.sex == '0' or player.get_age() > 50):
            points += len(games) * self.tournament.handicap_size
        return points if points else 0

    def get_games_count(self):
        return self.games.count()

    def get_player_min_points(self, player):
        """
        Возвращает минимальное количество очков, которые игрок набрал в рамках игр данного блока.
        Если игр нет, возвращает 0.
        """
        games = Game.objects.filter(block=self)
        info = GameInfo.objects.filter(game__in=games, team=player.get_team(tournament=self.tournament, count=1))

        min_points = info.aggregate(Min('point'))['point__min']
        if min_points and self.tournament.handicap and (player.sex == '0' or player.get_age() > 50):
            min_points += self.tournament.handicap_size
        return min_points if min_points else 0

    def get_player_max_points(self, player):
        """
        Возвращает максимальное количество очков, которые игрок набрал в рамках игр данного блока.
        Если игр нет, возвращает 0.
        """
        games = Game.objects.filter(block=self)
        info = GameInfo.objects.filter(game__in=games, team=player.get_team(tournament=self.tournament, count=1))

        max_points = info.aggregate(Max('point'))['point__max']
        if max_points and self.tournament.handicap and (player.sex == '0' or player.get_age() > 50):
            max_points += self.tournament.handicap_size
        return max_points if max_points else 0


class Game(models.Model):
    class Meta:
        verbose_name_plural = 'Игры'

    date = models.DateField(default=datetime.today)
    time = models.TimeField(default=datetime.now)
    name = models.CharField(max_length=200, blank=False)
    block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='games')
    is_desperado = models.BooleanField(default=False)
    # info = models.ManyToManyField('GameInfo', related_name='game')

    def __str__(self):
        return self.name


class GameInfo(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='info')
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='info')
    point = models.IntegerField(default=0)
