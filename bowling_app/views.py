from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from Auth.models import RegistrationRequest


class RegistrationRequestsView(View):
    def get(self, request):
        if request.user.is_staff:
            requests = RegistrationRequest.objects.get_active_requests()
            return render(request, 'bowling_app/registration_requests.html',
                          {'requests': requests})
        else:
            return HttpResponse("Access Denied", status=403)


class RequestHandlingView(View):
    # TODO: Make Request POST and use ajax on client side
    def get(self, request, id):
        if request.user.is_staff:
            if request.GET['status'] == "accepted":
                status = RegistrationRequest.ACCEPTED
            elif request.GET['status'] == "declined":
                status = RegistrationRequest.DECLINED

            if status is not None:
                reg_request = RegistrationRequest.objects.get(id=id)
                reg_request.status = status
                reg_request.save()
                user = reg_request.user
                user.is_active = True
                user.save()
                return redirect(reverse('bowling_manage_registration'))
        else:
            return HttpResponse("Access Denied", status=403)
