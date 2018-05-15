from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, DetailView, DeleteView, UpdateView

from rating.forms import RatingCreationForm
from rating.models import Rating


@method_decorator(staff_member_required(), name='dispatch')
class RatingCreate(CreateView):
    model = Rating
    template_name = 'rating/rating_create.html'
    success_url = reverse_lazy('rating:list')
    form_class = RatingCreationForm


@method_decorator(staff_member_required(), name='dispatch')
class RatingListView(ListView):
    items_on_page = 10

    def get_page(self):
        page = 1
        if 'page' in self.kwargs:
            page = int(self.kwargs['page'])
        return page

    def get_queryset(self):
        # выбираем сущности в зависимости от страницы
        ratings = Rating.objects.order_by('name')[
                  (self.get_page() - 1) * self.items_on_page: self.get_page() * self.items_on_page]
        return ratings

    template_name = 'rating/rating_list.html'
    context_object_name = 'ratings'


@method_decorator(staff_member_required(), name='dispatch')
class RatingDetailView(DetailView):
    model = Rating

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['players'] = self.object.get_unique_players()
        return context


class RatingDeleteView(DeleteView):
    model = Rating
    success_url = reverse_lazy('rating:list')


class RatingUpdateView(UpdateView):

    def get_success_url(self):
        return reverse_lazy('rating:page', kwargs={'pk': self.object.id})

    model = Rating
    fields = '__all__'
    success_url = get_success_url
