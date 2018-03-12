from django.conf.urls import url

from bowling_app.ajax_views import CityAutocomplete
from bowling_app.views import RegistrationRequestsView, RequestHandlingView, PlayerCreate, HomePage, PlayersUnionView, \
    PlayersListView, PlayerProfileView, PlayerBlockUnblock

urlpatterns = [
    # todo переименовать url name в нормальный вид
    url(r'manage/registration$', RegistrationRequestsView.as_view(), name="bowling_manage_registration"),
    url(r'manage/registration/(?P<id>\d+)/', RequestHandlingView.as_view(), name="handling_registration"),
    url(r'manage/player/register$', PlayerCreate.as_view(), name="player_create"),
    url(r'manage/player/union$', PlayersUnionView.as_view(), name="players_union"),
    url(r'manage/players$', PlayersListView.as_view(), name="players_list"),
    url(r'manage/player/(?P<id>\d+)$', PlayerProfileView.as_view(), name="player"),
    url(r'manage/player/(?P<id>\d+)/activity$', PlayerBlockUnblock.as_view(), name="player_activity"),
    url(r'^$', HomePage.as_view(), name='home'),

    # Ajax
    url(r'^ajax/city-autocomplete', CityAutocomplete.as_view(), name='city-autocomplete')
]
