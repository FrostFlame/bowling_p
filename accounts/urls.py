from django.conf.urls import url
from django.urls import reverse_lazy

from accounts.forms import LoginUserForm
from accounts.views import RegisterUserView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    url(r'register/$', RegisterUserView.as_view(), name="register"),
    url(r'login/$', LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True,
                                      form_class=LoginUserForm), name="login"),
    url(r'logout/$', LogoutView.as_view(next_page=reverse_lazy('bowlingApp:home')), name='logout')
]