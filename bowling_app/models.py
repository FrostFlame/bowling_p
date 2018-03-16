from django.db import models

# Create your models here.

class Event (models.Model):
    name = models.CharField(max_length=140)
    description = models.TextField(max_length=500)
    date = models.DateTimeField()

    def __str__(self):
        return self.name