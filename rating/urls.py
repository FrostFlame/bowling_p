from django.conf.urls import url

from rating.views import *

urlpatterns = [
    url(r'^create$', RatingCreate.as_view(), name='create'),
    url(r'^list$', RatingListView.as_view(), name='list'),
    url(r'^list/(?P<page>\d+)$', RatingListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)$', RatingDetailView.as_view(), name='page'),
    url(r'^(?P<pk>\d+)/delete$', RatingDeleteView.as_view(), name='delete'),
    url(r'^(?P<pk>\d+)/edit$', RatingUpdateView.as_view(), name='edit')
]
