from django.conf.urls import url

from bowling_app.views import RegistrationRequestsView, RequestHandlingView, PlayerCreate, HomePage

urlpatterns = [
    url(r'manage/registration$', RegistrationRequestsView.as_view(), name="bowling_manage_registration"),
    url(r'manage/registration/(?P<id>\d+)/', RequestHandlingView.as_view(), name="handling_registration"),
    url(r'manage/player/register$', PlayerCreate.as_view(), name="player_create"),
    url(r'^$',HomePage.as_view(),name='home'),
]
