from django.contrib import admin
from .models import Category, Post, Author, PostCategory, Subscription


class PostCategoryInLine(admin.TabularInline):
    model = PostCategory
    fk_name = 'connect_to_post'
    extra = 3


class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInLine]


admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(Author)
admin.site.register(Subscription)

