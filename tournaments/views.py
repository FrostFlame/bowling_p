from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView

from accounts.models import PlayerInfo
from tournaments.forms import TournamentCreationForm, GameCreationForm
from tournaments.models import Tournament, TournamentMembership, Game, GameInfo


@method_decorator(staff_member_required(), name='dispatch')
class TournamentCreate(CreateView):
    def get_success_url(self):
        return reverse('tournaments:tournament_add_players', args=(self.object.id,))

    model = Tournament
    template_name = 'tournaments/tournament_form.html'
    success_url = get_success_url
    form_class = TournamentCreationForm


class TournamentsListView(ListView):
    queryset = Tournament.objects.all()
    context_object_name = 'tournaments'
    template_name = 'tournaments/tournaments_list.html'


class TournamentView(View):
    def get(self, request, id):
        tournament = Tournament.objects.get(id=id)
        games = tournament.tournament_games.all()
        return render(request, 'tournaments/tournament_page.html',
                      {'request': tournament,
                       'games': games})


class AddPlayersView(View):
    def get(self, request, id):
        tournament = Tournament.objects.get(id=id)
        if tournament.type == '1':
            players = PlayerInfo.objects.filter(license__iregex='\\d+№0')
        elif tournament.type == '2':
            players = PlayerInfo.objects.filter(license__iregex='\\d+№1')
        elif tournament.type == '3':
            players = PlayerInfo.objects.filter(license__iregex='\\d+')
        else:
            players = PlayerInfo.objects.all()
        already_selected = tournament.players.all()
        return render(request, 'tournaments/add_players.html',
                      {'tournament': tournament, 'players': players, 'already_selected': already_selected})

    def post(self, request, id):
        players = request.POST.getlist('select')
        for player in players:
            TournamentMembership(player=PlayerInfo.objects.get(id=player),
                                 tournament=Tournament.objects.get(id=id)).save()
        return redirect('tournaments:tournaments_all')


@method_decorator(staff_member_required(), name='dispatch')
class TournamentUpdate(UpdateView):
    def get_success_url(self):
        return reverse('tournaments:tournament_page', args=(self.object.id,))

    model = Tournament
    template_name = 'tournaments/tournament_form.html'
    success_url = get_success_url
    form_class = TournamentCreationForm


class TournamentGameInfo(View):
    def get(self, request, tournament_pk, game_pk):
        game = get_object_or_404(Game, pk=game_pk)
        gameInfo = GameInfo.objects.filter(game=game)
        return render(request, 'tournaments/tournament_game_info.html', {'game': game, 'gameInfo': gameInfo})


class GameCreateView(View):
    def get(self, request, id):
        selected = Tournament.objects.get(pk=id).players.all()
        game_form = GameCreationForm()
        return render(request, 'tournaments/game_create.html', {
            'form': game_form,
            'selected': selected,
        })

    def post(self, request, id):
        tournament = Tournament.objects.get(pk=id)

        game_form = GameCreationForm(request.POST, tournament=tournament)
        if game_form.is_valid():
            game = game_form.save()
            players = request.POST.getlist('select')
            for player in players:
                GameInfo(player=PlayerInfo.objects.get(id=player),
                         game=game).save()
            return redirect(reverse('tournaments:tournament_page', kwargs={'id': tournament.id}))
        else:
            selected = Tournament.objects.get(pk=id).players.all()
            return render(request, 'tournaments/game_create.html', {
                'form': game_form,
                'selected': selected
            })


class GameUpdateView(View):
    def get(self, request, tournament_pk, game_pk):
        game = Game.objects.get(pk=game_pk)
        form = GameCreationForm(instance=game)
        # Игроки, которые уже добавлены к игре
        selected_players = game.players.all()
        # Остальные игроки, которые могут быть добавлены
        players = Tournament.objects.get(pk=tournament_pk).players.exclude(pk__in=selected_players)

        ctx = {
            'form': form,
            'players': players,
            'selected': selected_players,
        }
        return render(request, 'tournaments/game_update.html', ctx)

    def post(self, request, tournament_pk, game_pk):
        tournament = Tournament.objects.get(pk=tournament_pk)
        game = Game.objects.get(pk=game_pk)
        form = GameCreationForm(request.POST, instance=game, tournament=tournament)

        if form.is_valid():
            game = form.save()
            # Обновление игрок, участвующих в турнире
            game.players.clear()
            players_pk = request.POST.getlist('select')
            players = PlayerInfo.objects.filter(id__in=players_pk)
            for player in players:
                GameInfo.objects.create(player=player, game=game)

            return redirect('tournaments:tournaments_all')
