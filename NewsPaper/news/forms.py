from django import forms
from .models import Post, PostCategory
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=128)
    text = forms.CharField(min_length=20, label='Text', widget=forms.Textarea)

    class Meta:
        model = Post
        fields = {
            'author',
            'connect',
            'title',
            'text',
        }

        def clean(self):
            cleaned_data = super().clean()
            name = cleaned_data.get('title')
            text = cleaned_data.get("text")

            if name == text:
                raise ValidationError(
                    _("Описание товара не может быть идентично названию")
                )

            return cleaned_data
