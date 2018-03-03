from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, DetailView

from news.forms import NewsCreationForm
from news.models import News


class NewsCreateView(CreateView):
    def get_success_url(self):
        return reverse('news:news_view', args=(self.object.id,))

    model = News
    template_name = 'news/news_create.html'
    success_url = get_success_url
    form_class = NewsCreationForm

class NewsView(DetailView):
    model = News

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context