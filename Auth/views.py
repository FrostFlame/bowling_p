from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from Auth import forms
from Auth.forms import PlayerRegistrationForm
from Auth.models import RegistrationRequest, PlayerInfo


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
        profile_form = forms.PlayerRegistrationForm(request.POST, request.FILES)
        if all([user_form.is_valid(), profile_form.is_valid()]):
            user = user_form.save()
            player = PlayerInfo(user=user)
            player = PlayerRegistrationForm(request.POST, request.FILES, instance=player)
            player.save()
            RegistrationRequest.objects.create_request(user=user)
            return HttpResponse("You've been registered!")
        else:
            return render(request, 'Auth/registration.html',
                          {'reg_form': user_form, 'player_form': profile_form})
