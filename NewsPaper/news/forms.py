from django import forms
from .models import Post
from django.core.exceptions import ValidationError


class PostForm(forms.ModelForm):
    title = forms.CharField(label='Title', max_length=128)
    text = forms.CharField(min_length=20, label='Text', widget=forms.Textarea)

    class Meta:
        model = Post
        fields = {
            'title',
            'author',
            'text',
        }

        def clean(self):
            cleaned_data = super().clean()
            name = cleaned_data.get('title')
            text = cleaned_data.get("text")

            if name == text:
                raise ValidationError(
                    "Описание товара не может быть идентично названию"
                )

            return cleaned_data
