from django.core.management.base import CommandError, BaseCommand
from news.models import Post, Category


class Command(BaseCommand):
    help = 'Resets all news in a certain category'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str)

    def handle(self, *args, **options):
        confirm = input('Do u really want delete news?  yes/no : ')

        if confirm != 'yes':
            self.stdout.write(self.style.ERROR('The resets is denied'))
            return

        elif confirm == 'yes':
            try:
                category = Category.objects.get(name_category=options['category'])
                Post.objects.filter(connect=category).delete()
                self.stdout.write(self.style.SUCCESS(f'Successfully deleted category and news in category'))
            except Post.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'''Couldn't find category {options}'''))
