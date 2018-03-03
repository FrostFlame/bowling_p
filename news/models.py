from django.db import models

# Create your models here.
from accounts.utils import UploadToPathAndRename


class News(models.Model):
    title = models.CharField(max_length=40)
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to=UploadToPathAndRename('news/'))
