from django.conf.urls import url

from events import views

urlpatterns = [
    url(r'^add$', views.EventAddView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)$', views.EventView.as_view(), name='view'),
    url(r'^all/(?P<page>\d+)$', views.AllEventsView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/edit$', views.EventUpdate.as_view(), name='update'),
]