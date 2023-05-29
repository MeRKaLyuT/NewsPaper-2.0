from django.contrib import admin
from .models import Category, Post, Author, PostCategory, Subscription


def nullfy_rank(modeladmin, request, queryset):
    queryset.update(rank_of_news=0)


nullfy_rank.short_description = 'Обнулить ранг'


class PostCategoryInLine(admin.TabularInline):
    model = PostCategory
    fk_name = 'connect_to_post'
    extra = 3


class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInLine]
    # Отображение в консоли джанго ( показывает во вкладке "посты" информацию сразу в поле с названием поста, без захода
    # в него)
    list_display = ['title', 'text', 'rank_of_news']
    # Сортировка по данным фильтрам. Появляется в админ панели
    list_filter = ['rank_of_news', 'title']
    # В админ панели появляется поле с поиском по данным фильтрам
    search_fields = ['title', 'category_type']
    # Под полем с поиском есть менюшка с выбором
    actions = [nullfy_rank]


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Subscription)

