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
from accounts.models import RegistrationRequest, PlayerInfo, User
from bowling_app.forms import StaffPlayerRegister, PlayerSearchForm, PersonalRegisterForm
from news.models import News
from tournaments.models import TournamentRequest, TournamentMembership, Tournament


class RequestsView(View):
    def get(self, request):
        if request.user.is_staff:
            registration_requests = RegistrationRequest.objects.get_active_requests()
            tournaments_requests = TournamentRequest.objects.get_active_requests()
            return render(request, 'bowling_app/registration_requests.html',
                          {'reg_requests': registration_requests, 'tournament_requests': tournaments_requests})
        else:
            return HttpResponse("Access Denied", status=403)


class RegistrationRequestHandlingView(View):
    def post(self, request, pk):
        if request.user.is_staff:
            status = None
            if request.POST['status'] == "Accept":
                status = RegistrationRequest.ACCEPTED
            elif request.POST['status'] == "Decline":
                status = RegistrationRequest.DECLINED

            if status is not None:
                # Obtain request's id from url parameters
                request_id = pk
                # Change current request's status to obtained from request
                reg_request = RegistrationRequest.objects.get(pk=request_id)
                reg_request.status = status
                reg_request.save()
                # Make user active if request is accepted
                if status == RegistrationRequest.ACCEPTED:
                    user = reg_request.user
                    user.is_active = True
                    user.save()

                user = reg_request.user
                user.is_active = True
                user.save()

                domain = get_current_site(request).domain
                mail_subject = 'Регистрация на %s' % (domain)
                ctx = {'status': status,
                       'domain': domain, }

                message = get_template('bowling_app/register_result.html').render(ctx)
                to_email = user.email
                email = EmailMultiAlternatives(mail_subject, message, 'tatar.bowling@gmail.com', [to_email])
                email.attach_alternative(message, "text/html")
                email.send()

                return redirect(reverse('bowlingApp:bowling_manage_registration'))

            return redirect(reverse('bowlingApp:bowling_manage_registration'))
        else:
            return HttpResponse("Access Denied", status=403)

    def get(self, request, pk):
        if request.user.is_staff:
            reg_request = RegistrationRequest.objects.get(pk=pk)
            similar_players = PlayerInfo.objects.get_similar_players(primary_player=reg_request.user.profile)
            return render(request, 'bowling_app/reg_request.html',
                          {"reg_request": reg_request,
                           "similar_players": similar_players})


class PlayerCreate(CreateView):
    model = PlayerInfo
    template_name = "bowling_app/player_form.html"
    success_url = reverse_lazy('bowlingApp:players_list')
    form_class = StaffPlayerRegister

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(PlayerCreate, self).dispatch(request, *args, **kwargs)


class PlayersUnionView(View):
    @method_decorator(staff_member_required())
    def dispatch(self, request, *args, **kwargs):
        return super(PlayersUnionView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        # Получаем игроков, которых необходимо объединить
        primary = PlayerInfo.objects.get(pk=request.POST['created_by_staff'])
        similar = PlayerInfo.objects.get(pk=request.POST['created_by_user'])

        # Обновляем уже существующего игрока, оставшегося удаляем
        primary.update(similar)
        similar.delete()

        # Подтверждаем аккаунт и принимаем заявку
        primary.user.is_active = True
        primary.save()

        request = RegistrationRequest.objects.get(pk=request.POST['request_id'])
        request.status = RegistrationRequest.ACCEPTED
        request.save()

        return redirect(reverse('bowlingApp:bowling_manage_registration'))


class PlayersListView(View):
    # @method_decorator(staff_member_required())
    def get(self, request):
        fullName = request.GET.get('name', None)
        players = PlayerInfo.objects.exclude(~Q(user=None) & Q(user__is_active=False))
        if fullName:
            for term in fullName.split():
                players = players.filter(
                    Q(f_name__icontains=term) | Q(i_name__icontains=term) | Q(o_name__icontains=term))
        search_form = PlayerSearchForm()
        return render(request, 'bowling_app/players_list.html', {"players": players, 'search_form': search_form})


class PlayerProfileView(View):

    def get(self, request, pk):
        player = get_object_or_404(PlayerInfo, pk=pk)

        if request.user.is_staff:
            user = User.objects.get(email=request.user)
            player_form = PlayerEditForm(instance=player)

            ctx = {
                'player': player,
                'user_form': user,
                'player_form': player_form
            }
            return render(request, 'bowling_app/player.html', ctx)
        else:
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


class PlayerBlockUnblock(View):
    def post(self, request, pk):
        player = get_object_or_404(PlayerInfo, pk=pk)
        player.user.is_active = not player.user.is_active
        player.user.save()
        return redirect(reverse('bowlingApp:player', kwargs={'pk': pk}))


class TournamentRequestHandlingView(View):
    def post(self, request, pk):
        if request.user.is_staff:
            status = None
            if request.POST['status'] == "Accept":
                status = TournamentRequest.ACCEPTED
            elif request.POST['status'] == "Decline":
                status = TournamentRequest.DECLINED

            if status is not None:
                # Obtain request's id from url parameters
                request_id = pk
                # Change current request's status to obtained from request
                tournament_request = TournamentRequest.objects.get(pk=request_id)
                tournament_request.status = status
                tournament_request.save()

                if status == TournamentRequest.ACCEPTED:
                    tournament_membership = TournamentMembership(
                        player=User.objects.get(pk=tournament_request.user.pk).profile,
                        tournament=tournament_request.tournament)
                    tournament_membership.save()

                domain = get_current_site(request).domain
                mail_subject = 'Подача заявки на участие в турнире на %s' % (domain)
                ctx = {'status': status,
                       'domain': domain, }

                message = get_template('bowling_app/tournament_result.html').render(ctx)
                to_email = tournament_request.user.email
                email = EmailMultiAlternatives(mail_subject, message, 'tatar.bowling@gmail.com', [to_email])
                email.attach_alternative(message, "text/html")
                email.send()
                return redirect(reverse('bowlingApp:bowling_manage_registration'))

            return redirect(reverse('bowlingApp:bowling_manage_registration'))
        else:
            return HttpResponse("Access Denied", status=403)

    def get(self, request, pk):
        if request.user.is_staff:
            reg_request = TournamentRequest.objects.get(pk=pk)
            return render(request, 'bowling_app/tournament_request.html',
                          {"tournament_request": reg_request,
                           })

class CreatePersonalView(FormView):
    model = User
    form_class = PersonalRegisterForm
    template_name = 'bowling_app/personal_create.html'

    def get_success_url(self):
        if self.request.POST['role']=='1':
            return reverse('bowlingApp:photographers_list')
        else:
            return reverse('bowlingApp:editors_list')

    @method_decorator(staff_member_required())
    def dispatch(self, request, *args, **kwargs):
        return super(CreatePersonalView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        user=form.save()
        if form.data['role']=='1':
            user.is_photographer=True
        else:
            user.is_editor=True
        user.is_active=True
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
