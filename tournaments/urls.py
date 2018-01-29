from django.conf.urls import url

from tournaments.views import TournamentCreate

urlpatterns = [
    url(r'create$', TournamentCreate.as_view(), name='tournaments_create')
]