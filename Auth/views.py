from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from Auth import forms
from Auth.forms import PlayerRegistrationForm
from Auth.models import RegistrationRequest, PlayerInfo, User

from django.contrib.auth import login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .tokens import account_activation_token


class RegisterUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse("You've already been registered <-_->")
        else:
            user_form = forms.RegisterUserForm()
            player_form = forms.PlayerRegistrationForm()
            return render(request, 'Auth/registration.html',
                          {'reg_form': user_form,
                           'player_form': player_form})

    def post(self, request):
        user_form = forms.RegisterUserForm(request.POST)
        profile_form = forms.PlayerRegistrationForm(request.POST, request.FILES, request=request)
        if all([user_form.is_valid(), profile_form.is_valid()]):
            user = user_form.save(request)
            player = PlayerInfo(user=user)
            player = PlayerRegistrationForm(request.POST, request.FILES, instance=player, request=request)
            player.is_active = False
            player.save()
            email = user.email
            return render(request, 'Auth/confirm_email.html',
                          {'email': email})
        else:
            return render(request, 'Auth/registration.html',
                          {'reg_form': user_form, 'player_form': profile_form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.email_confirmed = True
        user.save()
        RegistrationRequest.objects.create_request(user=user)
        return HttpResponse('Ваш почтовый адрес подтвержден. Заявка на регистрацию отправлена на рассмотрение. '
                            'Вам будет отправлено письмо, как только ее подтвердят.')
    else:
        return HttpResponse('Ссылка на подтверждение почтового адреса недействительна!')