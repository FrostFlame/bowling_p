from django.conf.urls import url
from Auth.views import RegisterUserView
from django.contrib.auth.views import LoginView

urlpatterns = [
    url(r'register/$', RegisterUserView.as_view(), name="register"),
    url(r'login/$', LoginView.as_view(template_name='Auth/login.html'), name="login"),
]
