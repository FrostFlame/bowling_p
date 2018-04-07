from django.conf.urls import url

from albums.views import AlbumsListView, AlbumDetailView,CreateAlbumView,AlbumDeletelView,AlbumEditlView,PhotoDeleteView
urlpatterns = [
    url(r'^all$', AlbumsListView.as_view(), name='albums_list'),
    url(r'^add$',CreateAlbumView.as_view(),name='add_album'),
    url(r'^(?P<pk>\d+)$',AlbumDetailView.as_view(), name='album_detail'),
    url(r'^(?P<pk>\d+)/delete$', AlbumDeletelView.as_view(), name='delete_album'),
    url(r'^(?P<pk>\d+)/edit$', AlbumEditlView.as_view(), name='edit_album'),
    url(r'^(?P<album_id>\d+)/photo/(?P<photo_id>\d+)/delete$', PhotoDeleteView.as_view(), name='delete_photo')
]

