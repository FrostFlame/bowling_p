import os

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

# Create your views here.
from django.urls import reverse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from django.views.generic import FormView
from django.views.generic import ListView

from albums.forms import AddImagesForm,CreatAlbumForm
from albums.models import Album, Photo
from bowling.settings import MEDIA_URL


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
            photos_id={}
            for f in request.FILES.getlist('images'):
                photo = Photo.objects.create(
                    image=f,
                    album=album
                )
                photo.save()
                photos.append(str(photo.image))
                photos_id[str(photo.image)]=photo.id
            return JsonResponse({
                'new_photos':photos,
                'photos_id':photos_id
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


class AlbumDeletelView(DeleteView):
    model = Album
    success_url = reverse_lazy('album:albums_list')


class AlbumEditlView (View):
    def get(self,request,pk):
        album=get_object_or_404(Album,pk=pk)
        form = CreatAlbumForm(initial={
            'name':album.name,
            'cover':album.cover,
            'tournament':album.tournament
        })
        return render(request,'albums/edit_album.html',{'form':form,'album_id':pk})

    def post(self,request,pk):
        instance = get_object_or_404(Album, pk=pk)
        form=CreatAlbumForm(request.POST,instance=instance)
        if form.is_valid():
            form.save()
            return redirect(reverse('album:album_detail',kwargs={'pk':pk}))
        else:
            return render(request,'albums/edit_album.html',{'form':form,'album_id':pk})


class PhotoDeleteView(View):
    def post(self,request,album_id,photo_id):
        try:
            photo = Photo.objects.get(id=photo_id)
            photo.image.delete()
            photo.delete()
            return JsonResponse("ok",status=200,safe=False)
        except Exception:
            return JsonResponse("Oops",status=500,safe=False)




