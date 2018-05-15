from django.db import models

from tournaments.models import Tournament


class Rating(models.Model):
    name = models.CharField(max_length=240, unique=True)
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
