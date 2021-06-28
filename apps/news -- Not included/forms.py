from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from apps.news.models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'url', 'category', 'short_text', 'meta_description', 'status', 'date', 'text', 'image', 'thumbnail_size')
        widgets = {
            'title': forms.Textarea(attrs={'style': 'width: 400px; height: 34px;'}),
            'url': forms.Textarea(attrs={'style': 'width: 400px; height: 34px;'}),
            'short_text': forms.Textarea(attrs={'style': 'width: 400px; height: 68px;'}),
            'text': CKEditorUploadingWidget(),
            'meta_description': forms.Textarea(attrs={'style': 'width: 400px; height: 68px;'}),
        }
        model = Article
