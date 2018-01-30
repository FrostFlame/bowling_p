from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.generic import CreateView

from Auth.forms import PlayerRegistrationForm
from Auth.models import RegistrationRequest, PlayerInfo


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
                return redirect(reverse('bowlingApp:bowling_manage_registration'))
        else:
            return HttpResponse("Access Denied", status=403)

    def get(self, request, id):
        if request.user.is_staff:
            reg_request = RegistrationRequest.objects.get(pk=id)
            return render(request, 'bowling_app/reg_request.html',
                          {"reg_request": reg_request})


class PlayerCreate(CreateView):
    model = PlayerInfo
    template_name = "bowling_app/player_form.html"
    success_url = '/'
    form_class = PlayerRegistrationForm


class HomePage(View):
    def get(self, request):
        if request.user.is_authenticated:
            return render(request, 'bowling_app/home.html')
        else:
            return redirect(reverse('auth:login'))
