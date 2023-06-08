import datetime
from .models import *
from news.filters import PostFilter
from django.urls import reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_protect
from django.views import View
from .tasks import hello, printer
from django.http import HttpResponse
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.utils import timezone
import pytz


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
        context['time_now'] = datetime.datetime.utcnow()
        context['next_news'] = None
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'flatpages/new.html'
    context_object_name = 'article'
    # Кэшировать код до изменений ( при изменениях сразу обновлять ). Еще надо в моделях пофурычить
    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)
        return obj


class NewsCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('news.add_post',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'


class NewsUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('news.change_post',)
    form_class = PostForm
    model = Post
    template_name = 'flatpages/post_edit.html'


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('news.delete_post',)
    model = Post
    template_name = 'flatpages/post_delete.html'
    success_url = reverse_lazy('news_list')


class CategoryListView(ListView):
    model = Post
    template_name = 'account/category_list.html'
    context_object_name = 'category_news_list'

    # чтобы отличался от обычного списка новостей надо отфильтровать новости
    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['pk'])
        queryset = Post.objects.filter(connect=self.category).order_by('data')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_subscriber'] = self.request.user not in self.category.subscribers.all()
        context['category'] = self.category
        return context


@login_required()
def subscribe(request, pk):
    user = request.user
    category = Category.objects.get(id=pk)
    category.subscribers.add(user)

    message = _('Вы успешно подписались на рассылку новостей категории')
    return render(request, 'subscriptions.html', {'category': category, 'message': message})


class IndexView(View):
    def get(self, request):
        hello.delay()
        printer.delay(10)
        return HttpResponse('Hello!')


class Index(View):
    def get(self, request):
        current_time = timezone.now()

        models = MyModel.objects.all()
        context = {
            'models': models,
            'current_time': timezone.now(),
            'timezones': pytz.common_timezones

        }

        return HttpResponse(render(request, 'default.html', context))

    def post(self, request):
        request.session['django_timezone'] = request.POST['timezone']
        return redirect('/')
