from django.shortcuts import render

from django.views.generic import ListView

# Create your views here.
from news.models import Post


class NewsList(ListView):
    paginate_by = 9
    model = Post
    template_name = 'news/news_list.html'

