"""bowling URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^account/', include('accounts.urls', namespace='auth')),
                  url(r'^', include('bowling_app.urls', namespace="bowlingApp")),
                  url(r'^tournaments/', include('tournaments.urls', namespace='tournaments')),
                  url(r'^news/', include('news.urls', namespace='news')),
                  url(r'^album/', include('albums.urls', namespace='album')),
                  url(r'^events/', include('events.urls', namespace='events')),
                  # summernote
                  url(r'^summernote/', include('django_summernote.urls')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
