from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views.generic import CreateView

from tournaments.forms import TournamentCreationForm
from tournaments.models import Tournament

@method_decorator(staff_member_required(), name='dispatch')
class TournamentCreate(CreateView):
    model = Tournament
    template_name = 'tournaments/tournament_form.html'
    success_url = '/'
    form_class = TournamentCreationForm