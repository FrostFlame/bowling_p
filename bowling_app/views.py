from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, FormView, ListView

from accounts.forms import PlayerEditForm
from accounts.models import PlayerInfo, User
from bowling_app.forms import StaffPlayerRegister, PlayerSearchForm, PersonalRegisterForm
from news.models import News
from tournaments.models import Tournament


class PlayerCreate(CreateView):
    model = PlayerInfo
    template_name = "bowling_app/player_form.html"
    success_url = reverse_lazy('bowlingApp:players_list')
    form_class = StaffPlayerRegister

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PlayerCreate, self).dispatch(request, *args, **kwargs)


class PlayersListView(View):
    # @method_decorator(staff_member_required())
    def get(self, request):
        fullName = request.GET.get('name', None)
        players = PlayerInfo.objects.exclude()
        if fullName:
            for term in fullName.split():
                players = players.filter(
                    Q(f_name__icontains=term) | Q(i_name__icontains=term) | Q(o_name__icontains=term))
        search_form = PlayerSearchForm()
        return render(request, 'bowling_app/players_list.html', {"players": players, 'search_form': search_form})


class PlayerProfileView(View):

    def get(self, request, pk):
        player = get_object_or_404(PlayerInfo, pk=pk)
        ctx = {
            'player': player
        }
        return render(request, 'bowling_app/player.html', ctx)

    def post(self, request, pk):
        player = get_object_or_404(PlayerInfo, pk=pk)
        player_form = PlayerEditForm(request.POST, instance=player)
        if player_form.is_valid():
            player = player_form.save(commit=False)
            player.save()
            print(player)
            return redirect(reverse('bowlingApp:player', kwargs={'pk': player.pk}))
        else:
            return HttpResponse(player_form.errors)


class HomePage(View):
    def get(self, request):
        news_count = News.objects.count()
        tournaments_count = Tournament.objects.count()
        return render(request, 'bowling_app/home.html',
                      {'news': News.ordered_by_creation(3), 'tournaments': Tournament.ordered_by_creation(3),
                       'news_count': news_count, 'tournaments_count': tournaments_count})


class CreatePersonalView(FormView):
    model = User
    form_class = PersonalRegisterForm
    template_name = 'bowling_app/personal_create.html'

    def get_success_url(self):
        if self.request.POST['role'] == '1':
            return reverse('bowlingApp:photographers_list')
        else:
            return reverse('bowlingApp:editors_list')

    @method_decorator(staff_member_required())
    def dispatch(self, request, *args, **kwargs):
        return super(CreatePersonalView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        if form.data['role'] == '1':
            user.is_photographer = True
        else:
            user.is_editor = True
        user.is_active = True
        user.save()
        return super().form_valid(form)


class PhotographerListView(ListView):
    model = User
    queryset = User.objects.filter(is_photographer=True)
    template_name = 'bowling_app/photographers_list.html'


class EditorsListView(ListView):
    model = User
    queryset = User.objects.filter(is_editor=True)
    template_name = 'bowling_app/editors_list.html'
