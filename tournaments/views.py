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
from tournaments.forms import TournamentCreationForm, GameCreationForm, TournamentSearchForm, BlockCreationForm
from tournaments.models import Tournament, Game, GameInfo, Team, TournamentMembership, TeamType, Block


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
        return reverse('tournaments:tournaments_all', kwargs={'page': 1})

    model = Tournament
    success_url = get_success_url


class TournamentsListView(ListView, FormView):
    """
    class-based view для отображения спискка турниров
    """

    def get_page(self):
        page = 1
        if 'page' in self.kwargs:
            page = int(self.kwargs['page'])
        return page

    def get_queryset(self):
        tournament_type = 'all'
        form = self.form_class(self.request.GET)
        if 'tournament_type' in self.kwargs:
            tournament_type = self.kwargs['tournament_type']
        tournaments = Tournament.get_by_type(tournament_type)
        if form.is_valid():
            return tournaments.filter(Q(name__icontains=form.cleaned_data['search_field']) | Q(
                city__name__icontains=form.cleaned_data['search_field']))[
                   (self.get_page() - 1) * 10:self.get_page() * 10]
        else:
            return tournaments[(self.get_page() - 1) * 10:self.get_page() * 10]

    # queryset = Tournament.objects.all()
    context_object_name = 'tournaments'
    template_name = 'tournaments/tournaments_list.html'
    form_class = TournamentSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = Tournament.objects.count()
        context['page'] = self.get_page()
        return context


class TournamentView(View):
    """
    class-based view для страницы турнира
    """

    def get(self, request, pk):
        tournament = Tournament.objects.get(id=pk)
        blocks = tournament.block_tournament.filter(tournament=tournament).order_by('creation_date')
        # Сортируем игроков по сумме очков, набранных за турнир
        # players = tournament.players.all()

        # if tournament.type.name == 'Спортивный':
        #     men_players = players.filter(sex='0')
        #     women_players = players.filter(sex='1')
        #
        #     men_players = sorted(men_players, key=tournament.get_player_points, reverse=True)
        #     women_players = sorted(women_players, key=tournament.get_player_points, reverse=True)

        # men_player_games_dict = defaultdict(list)
        # Для каждой игры  турнира создаем словарь с информацией о статистике игрока
        # for block in blocks:
        #     for player in men_players:
        #         try:
        #             men_player_games_dict[player.id].append(player.player_games.get(game=game))
        #         except GameInfo.DoesNotExist:
        #             # Если игрок не участвовал в данной игре, его результат равен 0.
        #             gi = GameInfo(result=0)
        #             men_player_games_dict[player.id].append(gi)
        #
        # women_player_games_dict = defaultdict(list)
        # # Для каждой игры  турнира создаем словарь с информацией о статистике игрока
        # for game in games:
        #     for player in women_players:
        #         try:
        #             women_player_games_dict[player.id].append(player.player_games.get(game=game))
        #         except GameInfo.DoesNotExist:
        #             # Если игрок не участвовал в данной игре, его результат равен 0.
        #             gi = GameInfo(result=0)
        #             women_player_games_dict[player.id].append(gi)

        return render(request, 'tournaments/tournament_page.html',
                      {'tournament': tournament,
                       'blocks': blocks,
                       # 'men_players': men_players,
                       # 'women_players': women_players,
                       # 'men_games_dict': men_player_games_dict,
                       # 'women_games_dict': women_player_games_dict
                       })

        # else:
        #     player_games_dict = defaultdict(list)
        #
        #     for game in games:
        #         for player in players:
        #             try:
        #                 player_games_dict[player.id].append(player.player_games.get(game=game))
        #             except GameInfo.DoesNotExist:
        #                 # Если игрок не участвовал в данной игре, его результат равен 0.
        #                 gi = GameInfo(result=0)
        #                 player_games_dict[player.id].append(gi)

        # return render(request, 'tournaments/tournament_page.html',
        #               {'tournament': tournament,
        #                'games': games,
        #                'players': players,
        #                'games_dict': player_games_dict
        #                })


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
                TournamentMembership.objects.get(player=player, tournament=tournament).delete()
        # Добавление новых игроков
        for player_pk in players_pks:
            if player_pk not in tournament_players_pks:
                player = get_object_or_404(PlayerInfo, pk=player_pk)
                TournamentMembership.objects.get_or_create(player=player,
                                                           tournament=tournament)

        return redirect(reverse('tournaments:divide_players', kwargs={'pk': pk}))


class DividePlayersByTeams(View):
    """
        class-based view для страницы разбиения игроков по командам
    """

    def get(self, request, pk):
        tournament = Tournament.objects.get(id=pk)
        players = PlayerInfo.objects.get_players_by_license_type(tournament.type)
        return render(request, 'tournaments/divide_players.html',
                      {'tournament': tournament, 'players': players})

    def post(self, request, pk):
        tournament = Tournament.objects.get(id=pk)
        players_ids = tournament.players.all().values_list('id', flat=True)
        types_ids = tournament.team_type.all().values_list('id', flat=True)
        for p_id in players_ids:
            for t_id in types_ids:
                number = request.POST.get(str(p_id) + '_' + str(t_id))
                count = 0
                if TeamType.objects.get(id=t_id).name == 'Один игрок':
                    count = 1
                elif TeamType.objects.get(id=t_id).name == 'Два игрока':
                    count = 2
                elif TeamType.objects.get(id=t_id).name == 'Три игрока':
                    count = 3
                elif TeamType.objects.get(id=t_id).name == 'Пять игроков':
                    count = 5
                if Team.objects.filter(tournament_id=pk, number=number, count=count).exists():
                    team = Team.objects.get(tournament_id=pk, number=number, count=count)
                else:
                    team = Team.objects.create(tournament_id=pk, number=number, count=count)
                team.players.add(PlayerInfo.objects.get(id=p_id))
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

    def get(self, request, tournament_pk, block_pk, game_pk):
        tournament = get_object_or_404(Tournament, pk=tournament_pk)
        game = get_object_or_404(Game, pk=game_pk)
        gameInfo = GameInfo.objects.filter(game=game)
        if tournament.type.name == 'Спортивный':
            men_game_info = filter(lambda g: g.player.sex == '0', gameInfo)
            women_game_info = [g for g in gameInfo if g.player.sex == '1']
            return render(request, 'tournaments/tournament_game_info.html',
                          {'game': game,
                           'mGameInfo': men_game_info,
                           'wGameInfo': women_game_info,
                           'tournament': tournament})

        else:
            return render(request, 'tournaments/tournament_game_info.html',
                          {'game': game,
                           'gameInfo': gameInfo,
                           'tournament': tournament})


@method_decorator(staff_member_required(), name='dispatch')
class GameCreateView(View):
    """
    class-based view для создания игры турнира
    после создаия перенаправляет на страницу турнира
    """

    def get(self, request, pk, block_pk):
        block = Block.objects.get(pk=block_pk)
        selected = block.players.all()
        game_form = GameCreationForm(block=block)
        return render(request, 'tournaments/game_create.html', {
            'my_block': block,
            'form': game_form,
            'selected': selected,
        })

    def post(self, request, pk, block_pk):
        tournament = Tournament.objects.get(pk=pk)
        block = Block.objects.get(pk=block_pk)

        game_form = GameCreationForm(request.POST, block=block)
        if game_form.is_valid():
            game = game_form.save()
            players = request.POST.getlist('select')
            for player in players:
                for team in Team.objects.filter(tournament=tournament):
                    if player in team.players.all():
                        GameInfo(team=team, game=game).save()
            return redirect(reverse('tournaments:block_page', kwargs={'pk': tournament.id, 'block_pk': block.id}))
        else:
            selected = block.players.all()
            return render(request, 'tournaments/game_create.html', {
                'form': game_form,
                'my_block': block,
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

            return redirect(reverse('tournaments:tournament_page', kwargs={"pk": tournament_pk}))


@method_decorator(staff_member_required(), name='dispatch')
class BlockCreate(View):
    """
    class-based view для создания блока/этапа
    перенаправляет на страницу добавления игроков созданного турнира
    """

    def get(self, request, tournament_pk):
        tournament = Tournament.objects.get(pk=tournament_pk)
        selected = tournament.players.all()
        block_form = BlockCreationForm()
        return render(request, 'tournaments/block_form.html', {
            'tournament': tournament,
            'form': block_form,
            'selected': selected
        })

    def post(self, request, tournament_pk):
        tournament = Tournament.objects.get(pk=tournament_pk)
        block_form = BlockCreationForm(request.POST)
        if block_form.is_valid():
            block_form.tournament = tournament
            block = block_form.save()
            players = request.POST.getlist('select')
            for player in players:
                block.players.add(player)
            return redirect(reverse('tournaments:block_page', kwargs={'pk': tournament.id, 'block_pk': block.id}))
        else:
            selected = tournament.players.all()
            return render(request, 'tournaments/block_form.html', {
                'form': block_form,
                'selected': selected
            })


class BlockView(View):
    """
    class-based view для страницы блока
    """

    def get(self, request, pk, block_pk):
        tournament = Tournament.objects.get(id=pk)
        block = Block.objects.get(id=block_pk)
        games = Game.objects.filter(block=block).order_by('date')

        # Сортируем игроков по сумме очков, набранных за турнир
        players = block.players.all()

        if tournament.type.name == 'Спортивный':
            men_players = players.filter(sex='0')
            women_players = players.filter(sex='1')

            men_players = sorted(men_players, key=tournament.get_player_points, reverse=True)
            women_players = sorted(women_players, key=tournament.get_player_points, reverse=True)

            men_player_games_dict = defaultdict(list)
            # Для каждой игры  турнира создаем словарь с информацией о статистике игрока
            for game in games:
                for player in men_players:
                    try:
                        men_player_games_dict[player.id].append(player.player_games.get(game=game))
                    except GameInfo.DoesNotExist:
                        # Если игрок не участвовал в данной игре, его результат равен 0.
                        gi = GameInfo(result=0)
                        men_player_games_dict[player.id].append(gi)

            women_player_games_dict = defaultdict(list)
            # Для каждой игры  турнира создаем словарь с информацией о статистике игрока
            for game in games:
                for player in women_players:
                    try:
                        women_player_games_dict[player.id].append(player.player_games.get(game=game))
                    except GameInfo.DoesNotExist:
                        # Если игрок не участвовал в данной игре, его результат равен 0.
                        gi = GameInfo(result=0)
                        women_player_games_dict[player.id].append(gi)

            return render(request, 'tournaments/block_page.html',
                          {'tournament': tournament,
                           'games': games,
                           'men_players': men_players,
                           'women_players': women_players,
                           'men_games_dict': men_player_games_dict,
                           'women_games_dict': women_player_games_dict,
                           'my_block': block
                           })

        else:
            player_games_dict = defaultdict(list)

            for game in games:
                for player in players:
                    try:
                        # player_games_dict[player.id].append(player.game.get(game=game))
                        pass
                    except GameInfo.DoesNotExist:
                        # Если игрок не участвовал в данной игре, его результат равен 0.
                        gi = GameInfo(result=0)
                        player_games_dict[player.id].append(gi)

            return render(request, 'tournaments/block_page.html',
                          {'tournament': tournament,
                           'my_block': block,
                           'games': games,
                           'players': players,
                           'games_dict': player_games_dict
                           })


# @method_decorator(staff_member_required(), name='dispatch')
# class BlockUpdate(UpdateView):
#     """
#     class-based view для редактирования информации о блоке
#     """
#
#     def get_success_url(self):
#         return reverse('tournaments:block_page', kwargs={'pk': self.object.tournament.id, 'block_pk': self.object.id})
#
#     def selected(self):
#         return self.object.players.all()
#
#     model = Block
#     template_name = 'tournaments/block_form.html'
#     success_url = get_success_url
#     form_class = BlockCreationForm


class BlockUpdate(View):

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(BlockUpdate, self).dispatch(request, *args, **kwargs)

    def get(self, request, tournament_pk, pk):
        block = Block.objects.get(pk=pk)
        form = BlockCreationForm(instance=block)
        # Игроки, которые уже добавлены к игре
        selected_players = block.players.all()
        # Остальные игроки, которые могут быть добавлены
        players = Tournament.objects.get(pk=tournament_pk).players.exclude(pk__in=selected_players)

        ctx = {
            'form': form,
            'tournament': Tournament.objects.get(pk=tournament_pk),
            'players': players,
            'selected': selected_players,
        }
        return render(request, 'tournaments/block_form.html', ctx)

    def post(self, request, tournament_pk, pk):
        block = Block.objects.get(pk=pk)
        form = BlockCreationForm(request.POST, instance=block)

        if form.is_valid():
            block = form.save()
            # Обновление игрок, участвующих в турнире
            block.players.clear()
            players_pk = request.POST.getlist('select')
            players = PlayerInfo.objects.filter(id__in=players_pk)
            for player in players:
                block.players.add(player)
                block.save()
                # GameInfo.objects.create(player=player, game=game)

            return redirect(reverse('tournaments:block_page', kwargs={"pk": tournament_pk, "block_pk": pk}))