from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import m2m_changed, post_save
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from .models import *


def send_notifications(preview, pk, title, subscribers):
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': preview,
            'link': f'http://127.0.0.1:8000/news/{pk}',
        }
    )

    msg = EmailMultiAlternatives(
        subject=title,
        body='',
        from_email=settings.EMAIL_HOST_USER,
        to=subscribers,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()




@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':

        categories = instance.connect.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()

        subscribers = [s.email for s in subscribers]

        send_notifications(instance.preview(), instance.pk, instance.title, subscribers)


