from django.conf.urls import url
from Auth.views import RegisterUserView

urlpatterns = [
    url(r'register/$', RegisterUserView.as_view(), name="register"),
]
