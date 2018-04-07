from django.db import models

# Create your models here.
from accounts.utils import UploadToPathAndRename


class News(models.Model):
    title = models.CharField(max_length=140)
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=UploadToPathAndRename('news/'))

    @classmethod
    def ordered_by_creation(cls, amount=0, reversed=True, page=1):
        if amount == 0:
            amount = News.objects.count()
        if not reversed:
            return News.objects.order_by('created').values('id', 'title', 'image', 'created')[(page - 1) * amount:page * amount]
        else:
            return News.objects.order_by('-created').values('id', 'title', 'image', 'created')[(page - 1) * amount:page * amount]
