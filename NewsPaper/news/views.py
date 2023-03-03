from datetime import datetime
from .models import Post
from news.filters import PostFilter
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .forms import PostForm


class NewsList(ListView):
    model = Post
    ordering = 'data'
    template_name = 'flatpages/news.html'
    context_object_name = 'news'
    paginate_by = 10
    


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['time_now'] = datetime.utcnow()
        context['next_news'] = None
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'article'


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'


class NewsDelete(DeleteView):
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('news_list')


