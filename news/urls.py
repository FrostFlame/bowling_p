from django.conf.urls import url

from news.views import NewsCreateView, NewsView

urlpatterns = [
    url(r'^create$', NewsCreateView.as_view(), name='news_create'),
    url(r'^(?P<pk>\d+)$', NewsView.as_view(), name='news_view')
]