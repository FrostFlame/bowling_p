from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView

from accounts.models import RegistrationRequest, PlayerInfo
from bowling_app.forms import StaffPlayerRegister, EventCreationForm
from bowling_app.models import Event
from news.models import News


class RegistrationRequestsView(View):
    def get(self, request):
        if request.user.is_staff:
            requests = RegistrationRequest.objects.get_active_requests()
            return render(request, 'bowling_app/registration_requests.html',
                          {'requests': requests})
        else:
            return HttpResponse("Access Denied", status=403)


class RequestHandlingView(View):
    def post(self, request, id):
        if request.user.is_staff:
            status = None
            if request.POST['status'] == "Accept":
                status = RegistrationRequest.ACCEPTED
            elif request.POST['status'] == "Decline":
                status = RegistrationRequest.DECLINED

            if status is not None:
                # Obtain request's id from url parameters
                request_id = id
                # Change current request's status to obtained from request
                reg_request = RegistrationRequest.objects.get(id=request_id)
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

    def get(self, request, id):
        if request.user.is_staff:
            reg_request = RegistrationRequest.objects.get(pk=id)
            similar_players = PlayerInfo.objects.get_similar_players(primary_player=reg_request.user.profile)
            return render(request, 'bowling_app/reg_request.html',
                          {"reg_request": reg_request,
                           "similar_players": similar_players})


class PlayerCreate(CreateView):
    model = PlayerInfo
    template_name = "bowling_app/player_form.html"
    success_url = '/'
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
        request = RegistrationRequest.objects.get(pk=request.POST['request_id'])
        request.status = RegistrationRequest.ACCEPTED
        request.save()

        return redirect(reverse('bowlingApp:bowling_manage_registration'))


class PlayersListView(View):
    # @method_decorator(staff_member_required())
    def get(self, request):
        players = PlayerInfo.objects.all()
        return render(request, 'bowling_app/players_list.html', {"players": players})


class PlayerProfileView(View):
    def get(self, request, id):
        player = PlayerInfo.objects.get(pk=id)
        return render(request, 'bowling_app/player.html', {'player': player})


class HomePage(View):
    def get(self, request):
        news_count = News.objects.count()
        return render(request, 'bowling_app/home.html', {'news': News.ordered_by_creation(3),
                                                         'news_count': news_count})


class PlayerBlockUnblock(View):
    def post(self, request, id):
        player = get_object_or_404(PlayerInfo, pk=id)
        player.user.is_active = not player.user.is_active
        player.user.save()
        return redirect(reverse('bowlingApp:player', kwargs={'id': id}))


class EventAddView(CreateView):
    model = Event
    template_name = "bowling_app/event_add.html"
    success_url = '/'
    form_class = EventCreationForm

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EventAddView, self).dispatch(request, *args, **kwargs)
