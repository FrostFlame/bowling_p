from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View

from accounts import forms
from accounts.forms import PlayerRegistrationForm, UserEditForm, PlayerEditForm
from accounts.models import PlayerInfo, User
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

            # отправка письма на регистрацию в отдельном потоке
            import threading
            t = threading.Thread(target=send_activation_mail, args=(request, player_instance), kwargs={})
            t.setDaemon(True)
            t.start()

            email = user.email
            return render(request, 'accounts/confirm_email.html',
                          {'email': email})
        else:
            return render(request, 'accounts/registration.html',
                          {'reg_form': user_form, 'player_form': profile_form})


# # email confirmation
# def activate(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except(TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#
#     if user is not None and account_activation_token.check_token(user, token):
#         user.email_confirmed = True
#         user.save()
#         RegistrationRequest.objects.create_request(user=user)
#         return render(request, 'accounts/email_confirmed.html')
#     else:
#         return render(request, 'accounts/email_unconfirmed.html')


class ProfileView(View):
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        player = get_object_or_404(PlayerInfo, user=request.user)
        return render(request, 'accounts/profile.html', {'player': player})


class ProfileEditView(View):
    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(ProfileEditView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        player = get_object_or_404(PlayerInfo, user=request.user)
        user_form = UserEditForm(instance=request.user)
        player_form = PlayerEditForm(instance=player)
        return render(request, 'accounts/profile_edit.html', {'user_form': user_form,
                                                              'player_form': player_form})

    def post(self, request):
        user_form = forms.UserEditForm(request.POST, instance=request.user)
        old_email = request.user.email
        player = get_object_or_404(PlayerInfo, user=request.user)
        player_form = forms.PlayerEditForm(request.POST, request.FILES, instance=player)
        if all([user_form.is_valid(), player_form.is_valid()]):
            user = user_form.save()
            user.save()
            player = player_form.save(commit=False)
            if old_email != user.email:
                player.is_active = False
                send_activation_mail(request, player=PlayerInfo.objects.get(user=user))
            player.save()
            return redirect(reverse('auth:profile'))
        else:
            return render(request, 'accounts/profile_edit.html',
                          {'user_form': user_form, 'player_form': player_form})


def check_email_free(request):
    email = request.GET.get('email')
    user = User.objects.filter(email=email).exists()
    print(user)
    return HttpResponse(not user)
