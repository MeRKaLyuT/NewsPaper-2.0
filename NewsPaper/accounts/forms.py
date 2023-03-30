from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import EmailMultiAlternatives, mail_admins


class SignUpForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )


class CustomSignUpForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name='Common users')
        user.groups.add(common_users)

        subject = 'Добро пожаловать в Новостную газету!!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, Вы успешно зарегистрировались в '
            f'<a href="http://127.0.0.1:8000/news">Новостной газете</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.',
        )

        return user

# Добавление отправки сообщения о регистрации пользователя админу. Можно менеджеру, используя mail_managers ( для
# админов надо mail_admins ), а также указать в settings.py

# class CustomSignupForm(SignupForm):
#     def save(self, request):
#         user = super().save(request)
#
#         mail_admins(
#             subject='Новый пользователь!',
#             можно юзать html_message для добавления html
#             message=f'Пользователь {user.username} зарегистрировался на сайте.'
#         )
#
#         return user
