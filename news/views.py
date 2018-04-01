from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView, UpdateView
from rolepermissions.mixins import HasRoleMixin

from news.forms import NewsCreationForm
from news.models import News
from bowling.roles import Editor


class NewsCreateView(HasRoleMixin, CreateView):
    """
    class-based view for news creation

    allowed_roles - list of roles that has permission to create news
    """

    def get_success_url(self):
        return reverse('news:news_view', args=(self.object.id,))

    allowed_roles = [Editor]
    model = News
    template_name = 'news/news_create.html'
    success_url = get_success_url
    form_class = NewsCreationForm


class NewsView(DetailView):
    """
    class-based view for news detailed view
    """
    model = News


class AllNewsView(ListView):
    """
    class-based view for news list

    queryset - uses News class method to get all objects' only titles and images
    paginate_by - paginates by 10 items per page
    """

    def get_queryset(self):
        return News.ordered_by_creation(amount=10, page=int(self.request.GET['page']))

    template_name = 'news/news_list.html'
    context_object_name = 'news'


class NewsUpdate(HasRoleMixin, UpdateView):
    """
    class-based view for news update

    allowed_roles - list of roles that has permission to create news
    """

    def get_success_url(self):
        return reverse('news:news_view', args=(self.object.id,))

    allowed_roles = [Editor]
    model = News
    template_name = 'news/news_create.html'
    success_url = get_success_url
    form_class = NewsCreationForm
