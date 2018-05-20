from django.contrib import admin

# Register your models here.
from tournaments.models import Tournament, TeamType, Game

admin.site.register(Tournament)
admin.site.register(TeamType)
admin.site.register(Game)