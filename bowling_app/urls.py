from django.conf.urls import url

from bowling_app.ajax_views import CityAutocomplete
from bowling_app.views import RequestsView, RegistrationRequestHandlingView, PlayerCreate, HomePage, PlayersUnionView, \
    PlayersListView, PlayerProfileView, PlayerBlockUnblock, TournamentRequestHandlingView

urlpatterns = [
    # todo переименовать url name в нормальный вид
    url(r'manage/registration$', RequestsView.as_view(), name="bowling_manage_registration"),
    url(r'manage/registration/(?P<id>\d+)/', RegistrationRequestHandlingView.as_view(), name="handling_registration"),
    url(r'manage/tournament/(?P<id>\d+)/', TournamentRequestHandlingView.as_view(), name="handling_tournament_request"),
    url(r'manage/player/register$', PlayerCreate.as_view(), name="player_create"),
    url(r'manage/player/union$', PlayersUnionView.as_view(), name="players_union"),
    url(r'manage/players$', PlayersListView.as_view(), name="players_list"),
    url(r'manage/player/(?P<pk>\d+)$', PlayerProfileView.as_view(), name="player"),
    url(r'manage/player/(?P<id>\d+)/activity$', PlayerBlockUnblock.as_view(), name="player_activity"),
    url(r'^$', HomePage.as_view(), name='home'),
    # Ajax
    url(r'^ajax/city-autocomplete', CityAutocomplete.as_view(), name='city-autocomplete')
]
