from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import CreateView, ListView, DetailView, UpdateView
from rolepermissions.mixins import HasRoleMixin

from bowling.roles import Editor
from events.forms import EventCreationForm
from events.models import Event

from news.models import News


class EventView(DetailView):
    model = Event


class AllEventsView(ListView):
    # Если страница не указана, то первая по умолчанию
    def get_page(self):
        page = 1
        if 'page' in self.kwargs:
            page = int(self.kwargs['page'])
        return page

    def get_queryset(self):
        return Event.ordered_by_creation(amount=20, page=self.get_page())

    template_name = 'events/events_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = Event.objects.count()
        context['page'] = self.get_page()
        return context

    context_object_name = 'events'


class EventAddView(CreateView):
    model = Event
    template_name = "events/event_add.html"
    success_url = reverse_lazy('events:list')
    form_class = EventCreationForm

    @method_decorator(staff_member_required)
    def dispatch(self, request, *args, **kwargs):
        return super(EventAddView, self).dispatch(request, *args, **kwargs)


class EventUpdate(HasRoleMixin, UpdateView):
    def get_success_url(self):
        return reverse('events:view', args=(self.object.id,))

    allowed_roles = [Editor]
    model = Event
    template_name = 'events/event_add.html'
    success_url = get_success_url
    form_class = EventCreationForm


class Calendar(View):
    def get(self, request):
        news_count = Event.objects.count()
        return render(request, 'events/calendar.html',
                      {'events': News.ordered_by_creation(3), 'events_count': news_count})
