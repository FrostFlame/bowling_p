from django.conf.urls import url

from tournaments.views import TournamentCreate, TournamentsListView

urlpatterns = [
    url(r'create$', TournamentCreate.as_view(), name='tournaments_create'),
    url(r'list/', TournamentsListView.as_view(), name='tournaments_list'),
]