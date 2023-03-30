from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    userr = models.OneToOneField(User, on_delete=models.CASCADE)
    rank_author = models.IntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.all().aggregate(postRating=Sum('rank_of_news'))
        pRat = 0
        pRat += postRat.get('postRating') if postRat.get('postRating') else 0

        commentRat = self.userr.comment_set.all().aggregate(commentRating=Sum('rank'))
        cRat = 0
        cRat += commentRat.get('commentRating') if commentRat.get('commentRating') else 0

        self.rank_author = pRat * 3 + cRat
        self.save()


class Category(models.Model):
    name_category = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='Subscription')

    def __str__(self):
        return self.name_category.title()


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    article = 'AR'
    news = 'NW'

    Choice = (
        (article, 'Статья'),
        (news, "Новость")
    )

    category_type = models.CharField(max_length=2, choices=Choice)
    data = models.DateTimeField(auto_now_add=True)
    connect = models.ManyToManyField('Category', through='PostCategory')
    title = models.CharField(max_length=255)
    text = models.TextField()
    rank_of_news = models.IntegerField(default=0)

    def like(self):
        self.rank_of_news += 1
        self.save()

    def dislike(self):
        self.rank_of_news -= 1
        self.save()

    def preview(self):
        return self.text[0:124] + '...'

    def __str__(self):
        return f'{self.title.title()}: {self.text[:30]}'

    def get_absolute_url(self):
        return reverse('news_detail', args=[str(self.id)])


class PostCategory(models.Model):
    connect_to_post = models.ForeignKey(Post, on_delete=models.CASCADE)
    connect_to_category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    new_comment = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_from = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    data = models.DateTimeField(auto_now_add=True)
    rank = models.IntegerField(default=0)

    def like(self):
        self.rank += 1
        self.save()

    def dislike(self):
        self.rank -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='subscriptions')
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='subscriptions')

# Create your models here.
