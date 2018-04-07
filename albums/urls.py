from django.conf.urls import url

from albums.views import AlbumsListView, AlbumDetailView,CreateAlbumView
urlpatterns = [
    url(r'^all$', AlbumsListView.as_view(), name='albums_list'),
    url(r'^add$',CreateAlbumView.as_view(),name='add_album'),
    url(r'^(?P<pk>\d+)$',AlbumDetailView.as_view(), name='album_detail')
]

