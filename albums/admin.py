from django.contrib import admin

# Register your models here.
from albums.models import Album, Photo


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    pass

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass
