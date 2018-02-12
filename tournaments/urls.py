from django.conf.urls import url

from tournaments.views import *

urlpatterns = [
    url(r'^create$', TournamentCreate.as_view(), name='tournaments_create'),
    url(r'^all/', TournamentsListView.as_view(), name='tournaments_all'),
    url(r'^(?P<id>\d+)$', TournamentView.as_view(), name='tournament_page'),
    url(r'^(?P<id>\d+)/add_players$', AddPlayersView.as_view(), name='tournament_add_players'),
    url(r'^(?P<pk>\d+)/edit$', TournamentUpdate.as_view(), name='tournament_update'),
    url(r'^(?P<tournament_pk>\d+)/game/(?P<game_pk>\d+)$', TournamentGameInfo.as_view(), name='tournament_game_info'),
]