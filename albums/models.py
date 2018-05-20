from django.db import models

# Create your models here.


from _datetime import datetime

import os
from django.db import models
from django.utils.crypto import get_random_string

from tournaments.models import Tournament


def album_cover_path(instance, filename):
    return os.path.join('albums', instance.name, get_random_string(length=32) + '.' + filename.split('.')[-1])


def album_image_path(instance, filename):
    return os.path.join('albums', instance.album.name, get_random_string(length=32) + '.' + filename.split('.')[-1])


class Album(models.Model):
    class Meta:
        verbose_name_plural = 'Альбомы'

    name = models.CharField(max_length=200, blank=False, unique=False)
    created_at = models.DateTimeField(default=datetime.now)
    cover = models.ImageField(upload_to=album_cover_path, default=os.path.join('default', 'album_avatar.jpg'))
    tournament = models.OneToOneField(Tournament, null=True, default=None, related_name="tournament_album")

    def __str__(self):
        return self.name


class Photo(models.Model):
    class Meta:
        verbose_name_plural = 'Фотографии'

    created_at = models.DateTimeField(default=datetime.now)
    image = models.ImageField(upload_to=album_image_path)
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
