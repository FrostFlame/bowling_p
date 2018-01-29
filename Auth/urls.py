from django.conf.urls import url
from django.urls import reverse_lazy

from Auth.views import RegisterUserView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    url(r'register/$', RegisterUserView.as_view(), name="register"),
    url(r'login/$',LoginView.as_view(template_name='Auth/login.html',redirect_authenticated_user=True), name="login"),
    url(r'logout/$',LogoutView.as_view(next_page=reverse_lazy('auth:login')),name='logout')
]
