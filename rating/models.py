from django.db import models

from tournaments.models import Tournament, TournamentType


class Rating(models.Model):
    class Meta:
        verbose_name_plural = 'Рейтинги'
    name = models.CharField(max_length=240, unique=True)
    type = models.ForeignKey(TournamentType)
    tournaments = models.ManyToManyField(Tournament)

    def get_unique_players(self):
        """
        Возвращает список всех игроков в турнирах рейтинга
        """
        players = []
        for tournament in self.tournaments.all():
            for player in tournament.players.all():
                players.append(str(player))
        return sorted(set(players))

    def __str__(self):
        return "%s (%s)" % (self.name, self.type)