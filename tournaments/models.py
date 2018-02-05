import os
from django.db import models

# Create your models here.
from django.utils.crypto import get_random_string

from accounts.models import PlayerInfo

TYPE = (
    ('0', "Публичный"),
    ('1', 'Только для обладателей клубной лицензии'),
    ('2', 'Только для обладателей игровой лицензии'),
    ('3', 'Для обладателей любой лицензии')
)

# todo start with 1
# todo make fixtures, export to db
TEAM_TYPE = (
    ('0', 'Один игрок'),
    ('1', 'Два игрока')
)


def filename(instance, filename):
    return os.path.join('tournaments', get_random_string(length=32) + '.' + filename.split('.')[-1])


class Tournament(models.Model):
    name = models.CharField(max_length=40)
    start = models.DateTimeField()
    end = models.DateTimeField()
    # todo add default
    description = models.TextField(max_length=500, null=True)
    type = models.CharField(max_length=1, choices=TYPE)
    team_type = models.CharField(max_length=1, choices=TEAM_TYPE)
    # todo add verbose
    games = models.IntegerField(default=1)
    photo = models.ImageField(upload_to=filename, blank=True)
    # todo make without manytomany
    players = models.ManyToManyField(PlayerInfo)