from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from apps.news.models import Article, Comment


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'url', 'tags', 'short_description', 'status', 'date', 'text', 'image', 'thumbnail')
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 400px;'}),
            'url': forms.TextInput(attrs={'style': 'width: 400px;'}),
            'short_description': forms.Textarea(attrs={'style': 'width: 400px; height: 68px;'}),
            'text': CKEditorUploadingWidget(),
        }
        model = Article


class CommentForm(forms.ModelForm):
    class Meta:
        fields = ('article', 'author', 'reply_to', 'text')
        widgets = {
            'article': forms.HiddenInput(),
            'reply_to': forms.HiddenInput(),
            'text': forms.Textarea(attrs={'class': 'form-control', 'cols': '45', 'rows': '8', 'required': 'required', 'placeholder': 'Комментарий'})
        }
        model = Comment
