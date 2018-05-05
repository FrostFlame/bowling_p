from django.conf.urls import url

from tournaments.ajax_views import GameResultUpdate
from tournaments.views import *

urlpatterns = [
    url(r'^create$', TournamentCreate.as_view(), name='tournaments_create'),
    url(r'^delete/(?P<pk>\d+)$', TournamentDelete.as_view(), name='tournaments_delete'),
    url(r'^all/(?P<page>\d+)$', TournamentsListView.as_view(), name='tournaments_all'),
    url(r'^all/(?P<tournament_type>\w+)/(?P<page>\d+)$', TournamentsListView.as_view(), name='tournaments_all'),
    url(r'^(?P<pk>\d+)$', TournamentView.as_view(), name='tournament_page'),
    url(r'^(?P<pk>\d+)/game/create$', GameCreateView.as_view(), name='game_create'),
    url(r'^(?P<pk>\d+)/add_players$', AddPlayersView.as_view(), name='tournament_add_players'),
    url(r'^(?P<pk>\d+)/edit$', TournamentUpdate.as_view(), name='tournament_update'),
    url(r'^(?P<tournament_pk>\d+)/game/(?P<game_pk>\d+)$',
        TournamentGameInfo.as_view(), name='tournament_game_info'),
    url(r'^(?P<tournament_pk>\d+)/game/(?P<game_pk>\d+)/edit$',
        GameUpdateView.as_view(), name='game_update'),
    url(r'^(?P<pk>\d+)/request$', send_participation_request, name='send_request'),

    # Ajax
    url(r'^ajax/update_results', GameResultUpdate.as_view(), name='update_game_result'),
]
