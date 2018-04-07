from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import FormView
from django.views.generic import ListView

from albums.forms import AddImagesForm,CreatAlbumForm
from albums.models import Album, Photo


class AlbumsListView(ListView):
    model = Album
    template_name = 'albums/albums_list.html'

class AlbumDetailView(View):

    def get(self,request,pk):
        album=get_object_or_404(Album,pk=pk)
        return render(request,'albums/album_detail.html',{
            'form':AddImagesForm,
            'photos':Photo.objects.filter(album_id=pk),
            'album':album
        })

    def post(self,request,pk):
        if request.FILES:
            album=get_object_or_404(Album,pk=pk)
            photos=[]
            for f in request.FILES.getlist('images'):
                photo = Photo.objects.create(
                    image=f,
                    album=album
                )
                photo.save()
                photos.append(str(photo.image))
            return JsonResponse({
                'new_photos':photos
            },status=200,safe=False)
        else:
            return JsonResponse("Файлы не выбраны",status=500)


class CreateAlbumView(FormView):
    model = Album
    form_class = CreatAlbumForm
    template_name = 'albums/add_album.html'
    success_url = reverse_lazy('album:albums_list')

    def form_valid(self, form):
        album=form.save()
        album.save()
        return super().form_valid(form)


