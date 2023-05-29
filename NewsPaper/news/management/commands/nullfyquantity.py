from django.core.management.base import BaseCommand, CommandError
from news.models import Post


class Command(BaseCommand):
    help = 'Обнуляет ранг всех постов'

    def handle(self, *args, **options):
        for post in Post.objects.all():
            post.rank_of_news = 0
            post.save()

            self.stdout.write(self.style.SUCCESS('Successfully nulled post "%s"' % str(post)))

