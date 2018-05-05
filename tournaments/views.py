from collections import defaultdict

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
# Create your views here.
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, UpdateView, ListView, DeleteView
from django.views.generic import FormView

from accounts.models import PlayerInfo
from tournaments.forms import TournamentCreationForm, GameCreationForm, TournamentSearchForm
from tournaments.models import Tournament, TournamentMembership, Game, GameInfo, TournamentRequest


@method_decorator(staff_member_required(), name='dispatch')
class TournamentCreate(CreateView):
    """
    class-based view для создания турнира
    перенаправляет на страницу добавления игроков созданного турнира
    """

    def get_success_url(self):
        return reverse('tournaments:tournament_add_players', args=(self.object.id,))

    model = Tournament
    template_name = 'tournaments/tournament_form.html'
    success_url = get_success_url
    form_class = TournamentCreationForm


@method_decorator(staff_member_required(), name='dispatch')
class TournamentDelete(DeleteView):
    """
    class-based view для удаления турнира
    """

    def get_success_url(self):
        return reverse('tournaments:tournaments_all')

    model = Tournament
    success_url = get_success_url


class TournamentsListView(ListView,FormView):
    """
    class-based view для отображения спискка турниров
    """

    def get_queryset(self):
        tournament_type = 'all'
        form = self.form_class(self.request.GET)
        if 'tournament_type' in self.kwargs:
            tournament_type = self.kwargs['tournament_type']
        tournaments = Tournament.get_by_type(tournament_type)
        if form.is_valid():
            return tournaments.filter(Q(name__icontains=form.cleaned_data['search_field']) | Q(city__name__icontains=form.cleaned_data['search_field']) )
        else:
            return tournaments

    queryset = Tournament.objects.all()
    context_object_name = 'tournaments'
    template_name = 'tournaments/tournaments_list.html'
    form_class = TournamentSearchForm


class TournamentView(View):
    """
    class-based view для страницы турнира
    """

    def get(self, request, pk):
        tournament = Tournament.objects.get(id=pk)
        games = tournament.tournament_games.all().order_by('start')
        # Сортируем игроков по сумме очков, набранных за турнир
        players = tournament.players.all()
        players = sorted(players, key=tournament.get_player_points, reverse=True)

        player_games_dict = defaultdict(list)
        # Для каждой игры  турнира создаем словарь с информацией о статистике игрока
        for game in games:
            for player in players:
                try:
                    player_games_dict[player.id].append(player.player_games.get(game=game))
                except GameInfo.DoesNotExist:
                    # Если игрок не участвовал в данной игре, его результат равен 0.
                    gi = GameInfo(result=0)
                    player_games_dict[player.id].append(gi)

        tournament_request = False
        if not request.user.is_staff:
            tournament_request = TournamentRequest.objects.filter(user=request.user, tournament=tournament).exists()

        return render(request, 'tournaments/tournament_page.html',
                      {'tournament': tournament,
                       'games': games,
                       'players': players,
                       'games_dict': player_games_dict,
                       'tournament_request': tournament_request
                       })


class AddPlayersView(View):
    """
    class-based view для страницы добавления игроков к турниру
    """

    def get(self, request, pk):
        tournament = Tournament.objects.get(id=pk)
        already_selected = tournament.players.all()
        players = PlayerInfo.objects.get_players_by_license_type(tournament.type).exclude(pk__in=already_selected)

        return render(request, 'tournaments/add_players.html',
                      {'tournament': tournament, 'players': players, 'already_selected': already_selected})

    def post(self, request, pk):
        tournament = Tournament.objects.get(id=pk)
        # Обновленный список игроков, который пришел от пользователя
        players_pks = request.POST.getlist('select')

        # Список первичных ключей игроков, которые находятся в бд
        tournament_players_pks = list(tournament.players.values_list('id', flat=True))

        # tournament.players.clear()

        # Удаление игроков
        for tournament_players_pk in tournament_players_pks:
            if tournament_players_pk not in players_pks:
                player = get_object_or_404(PlayerInfo, pk=tournament_players_pk)
                TournamentMembership.objects.get(player=player,
                                                 tournament=tournament).delete()
        # Добавление новых игроков
        for player_pk in players_pks:
            if player_pk not in tournament_players_pks:
                player = get_object_or_404(PlayerInfo, pk=player_pk)
                TournamentMembership.objects.get_or_create(player=player,
                                                           tournament=tournament)

        return redirect(reverse('tournaments:tournament_page', kwargs={'pk': pk}))


@method_decorator(staff_member_required(), name='dispatch')
class TournamentUpdate(UpdateView):
    """
    class-based view для редактирования информации о турнире
    """

    def get_success_url(self):
        return reverse('tournaments:tournament_add_players', args=(self.object.id,))

    model = Tournament
    template_name = 'tournaments/tournament_form.html'
    success_url = get_success_url
    form_class = TournamentCreationForm


class TournamentGameInfo(View):
    """
    class-based view для отображения информации о конкретной игре турнира
    """

    def get(self, request, tournament_pk, game_pk):
        game = get_object_or_404(Game, pk=game_pk)
        gameInfo = GameInfo.objects.filter(game=game)
        return render(request, 'tournaments/tournament_game_info.html', {'game': game, 'gameInfo': gameInfo})


class GameCreateView(View):
    """
    class-based view для создания игры турнира
    после создаия перенаправляет на страницу турнира
    """

    def get(self, request, pk):
        tournament = Tournament.objects.get(pk=pk)
        selected = tournament.players.all()
        game_form = GameCreationForm()
        return render(request, 'tournaments/game_create.html', {
            'tournament': tournament,
            'form': game_form,
            'selected': selected,
        })

    def post(self, request, pk):
        tournament = Tournament.objects.get(pk=pk)

        game_form = GameCreationForm(request.POST, tournament=tournament)
        if game_form.is_valid():
            game = game_form.save()
            players = request.POST.getlist('select')
            for player in players:
                GameInfo(player=PlayerInfo.objects.get(id=player),
                         game=game).save()
            return redirect(reverse('tournaments:tournament_page', kwargs={'pk': tournament.id}))
        else:
            selected = tournament.players.all()
            return render(request, 'tournaments/game_create.html', {
                'form': game_form,
                'selected': selected
            })


class GameUpdateView(View):
    """
    class-based view для редактирования информации о конкретной игре турнира
    """

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(GameUpdateView, self).dispatch(request, *args, **kwargs)

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


def send_participation_request(request, pk):
    user = request.user
    tournament = Tournament.objects.get(id=pk)
    if TournamentRequest.objects.filter(user=user, tournament=tournament).exists():
        TournamentRequest.objects.get(user=user, tournament=tournament).delete()
    else:
        TournamentRequest.objects.create_request(user=user, tournament=tournament)
    return redirect(reverse('tournaments:tournament_page', kwargs={'pk': tournament.id}))