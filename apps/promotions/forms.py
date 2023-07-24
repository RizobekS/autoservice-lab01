from django import forms

from apps.news.models import Article
from apps.promotions.models import Promotion
from utils.widgets import CKEditorUploadingWidget, CKEditorWidget


class PromotionAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['articles'].queryset = Article.objects.filter(is_news=False).order_by('title')
        self.fields['products'].queryset = self.fields['products'].queryset.order_by('title')

    class Meta:
        fields = (
        'title', 'url', 'absolute_url', 'active', 'tags', 'date', 'image', 'thumbnail', 'icon_thumbnail', 'show_at_homepage', 'homepage_description', 'short_description', 'text')
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 400px;'}),
            'url': forms.TextInput(attrs={'style': 'width: 400px;'}),
            'short_description': CKEditorWidget(),
            'homepage_description': CKEditorWidget(),
            'text': CKEditorUploadingWidget(),
        }
        model = Promotion
