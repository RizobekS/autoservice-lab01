from django import forms

from apps.promotions.models import Promotion
from utils.widgets import CKEditorUploadingWidget, CKEditorWidget


class PromotionAdminForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'url', 'active', 'tags', 'date', 'image', 'thumbnail', 'icon_thumbnail', 'show_at_homepage', 'homepage_description', 'short_description', 'text')
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 400px;'}),
            'url': forms.TextInput(attrs={'style': 'width: 400px;'}),
            'short_description': CKEditorWidget(),
            'homepage_description': CKEditorWidget(),
            'text': CKEditorUploadingWidget(),
        }
        model = Promotion
