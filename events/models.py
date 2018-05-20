from django.db import models


class Event(models.Model):
    class Meta:
        verbose_name_plural = 'Мероприятия'
    name = models.CharField(max_length=140)
    description = models.TextField(max_length=500, blank=True, default='')
    date = models.DateTimeField()

    def __str__(self):
        return self.name

    @classmethod
    def ordered_by_creation(cls, amount=0, reversed=True, page=1):
        if amount == 0:
            amount = Event.objects.count()
        # return Event.objects.all()
        if not reversed:
            return Event.objects.order_by('date')[(page - 1) * amount:page * amount]
        else:
            x = Event.objects.order_by('-date')[(page - 1) * amount:page * amount]
            return x
