from django.conf.urls import url
from django.urls import reverse_lazy

from accounts import views
from accounts.forms import LoginUserForm
from django.contrib.auth.views import LoginView, LogoutView

from accounts.views import ProfileView,ProfileEditView

urlpatterns = [
    url(r'register/$', views.RegisterUserView.as_view(), name="register"),
    url(r'login/$', LoginView.as_view(template_name='accounts/login.html', redirect_authenticated_user=True,
                                      form_class=LoginUserForm), name="login"),
    url(r'logout/$', LogoutView.as_view(next_page=reverse_lazy('bowlingApp:home')), name='logout'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    url(r'profile/$', ProfileView.as_view(), name="profile"),
    url(r'profile/edit$', ProfileEditView.as_view(), name="profile_edit"),
]
