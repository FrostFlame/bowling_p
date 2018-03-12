from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from rolepermissions.mixins import HasRoleMixin

from news.forms import NewsCreationForm
from news.models import News


# todo add doc strings
class NewsCreateView(HasRoleMixin, CreateView):
    def get_success_url(self):
        return reverse('news:news_view', args=(self.object.id,))

    # todo roles in enum or const
    allowed_roles = 'redactor'
    model = News
    template_name = 'news/news_create.html'
    success_url = get_success_url
    form_class = NewsCreationForm


class NewsView(DetailView):
    model = News

    # todo ???
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class AllNewsView(ListView):
    # todo use another method
    queryset = News.objects.all().order_by('created')
    paginate_by = 10
    template_name = 'news/news_list.html'
    context_object_name = 'news'


class NewsUpdate(HasRoleMixin, UpdateView):
    def get_success_url(self):
        return reverse('news:news_view', args=(self.object.id,))

    allowed_roles = 'redactor'
    model = News
    template_name = 'news/news_create.html'
    success_url = get_success_url
    form_class = NewsCreationForm
