from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from accounts import forms
from accounts.forms import PlayerRegistrationForm
from accounts.models import RegistrationRequest, PlayerInfo, User, City

from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from accounts.utils import send_activation_mail
from .tokens import account_activation_token


class RegisterUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return HttpResponse("You've already been registered <-_->")
        else:
            user_form = forms.RegisterUserForm()
            player_form = forms.PlayerRegistrationForm()
            return render(request, 'accounts/registration.html',
                          {'reg_form': user_form,
                           'player_form': player_form})

    def post(self, request):
        user_form = forms.RegisterUserForm(request.POST)
        profile_form = forms.PlayerRegistrationForm(request.POST, request.FILES)
        if all([user_form.is_valid(), profile_form.is_valid()]):
            user = user_form.save(request)
            player = PlayerInfo(user=user)
            player = PlayerRegistrationForm(request.POST, request.FILES, instance=player)
            player.is_active = False
            player_instance = player.save()
            player_instance.watermark()
            player_instance.save()
            send_activation_mail(request, player_instance)
            email = user.email
            return render(request, 'accounts/confirm_email.html',
                          {'email': email})
        else:
            return render(request, 'accounts/registration.html',
                          {'reg_form': user_form, 'player_form': profile_form})


# email confirmation
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
        return render(request, 'accounts/email_confirmed.html')
    else:
        return render(request, 'accounts/email_unconfirmed.html')