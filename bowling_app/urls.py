from django.conf.urls import url

from bowling_app.views import RegistrationRequestsView, RequestHandlingView, PlayerCreate, HomePage, PlayersUnionView

urlpatterns = [
    url(r'manage/registration$', RegistrationRequestsView.as_view(), name="bowling_manage_registration"),
    url(r'manage/registration/(?P<id>\d+)/', RequestHandlingView.as_view(), name="handling_registration"),
    url(r'manage/player/register$', PlayerCreate.as_view(), name="player_create"),
    url(r'manage/player/union$', PlayersUnionView.as_view(), name="players_union"),
    url(r'^$', HomePage.as_view(), name='home'),
]
