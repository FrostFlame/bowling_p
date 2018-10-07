from django.conf.urls import url

from tournaments.ajax_views import GameResultUpdate
from tournaments.views import *

urlpatterns = [
    url(r'^create$', TournamentCreate.as_view(), name='tournaments_create'),
    url(r'^delete/(?P<pk>\d+)$', TournamentDelete.as_view(), name='tournaments_delete'),
    url(r'^all/(?P<page>\d+)$', TournamentsListView.as_view(), name='tournaments_all'),
    url(r'^all/(?P<tournament_type>\w+)/(?P<page>\d+)$', TournamentsListView.as_view(), name='tournaments_all'),
    url(r'^(?P<pk>\d+)$', TournamentView.as_view(), name='tournament_page'),
    url(r'^(?P<pk>\d+)/(?P<block_pk>\d+)/game/create$', GameCreateView.as_view(), name='game_create'),
    url(r'^(?P<tournament_pk>\d+)/block/create$', BlockCreate.as_view(), name='block_create'),
    url(r'^(?P<pk>\d+)/(?P<block_pk>\d+)$', BlockView.as_view(), name='block_page'),
    url(r'^(?P<pk>\d+)/add_players$', AddPlayersView.as_view(), name='tournament_add_players'),
    url(r'^(?P<pk>\d+)/divide_players$', DividePlayersByTeams.as_view(), name='divide_players'),
    url(r'^(?P<pk>\d+)/edit$', TournamentUpdate.as_view(), name='tournament_update'),
    url(r'^(?P<tournament_pk>\d+)/(?P<pk>\d+)/edit$', BlockUpdate.as_view(), name='block_update'),
    url(r'^(?P<tournament_pk>\d+)/(?P<block_pk>\d+)/(?P<game_pk>\d+)$',
        TournamentGameInfo.as_view(), name='tournament_game_info'),
    url(r'^(?P<tournament_pk>\d+)/(?P<block_pk>\d+)/(?P<game_pk>\d+)/edit$',
        GameUpdateView.as_view(), name='game_update'),

    # Ajax
    url(r'^ajax/update_results', GameResultUpdate.as_view(), name='update_game_result'),
]
