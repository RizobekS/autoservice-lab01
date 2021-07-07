from django import forms

from apps.promotions.models import Promotion
from utils.widgets import CKEditorUploadingWidget, CKEditorWidget


class PromotionAdminForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'url', 'active', 'show_at_homepage', 'tags', 'date', 'image', 'thumbnail', 'icon_thumbnail', 'short_description', 'text')
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 400px;'}),
            'url': forms.TextInput(attrs={'style': 'width: 400px;'}),
            'short_description': CKEditorWidget(),
            'text': CKEditorUploadingWidget(),
        }
        model = Promotion
