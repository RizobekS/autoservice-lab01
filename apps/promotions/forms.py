from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms

from apps.promotions.models import Promotion


class PromotionAdminForm(forms.ModelForm):
    class Meta:
        fields = ('title', 'url', 'active', 'show_at_homepage', 'tags', 'date', 'image', 'thumbnail', 'icon_thumbnail', 'short_description', 'text')
        widgets = {
            'title': forms.TextInput(attrs={'style': 'width: 400px;'}),
            'url': forms.TextInput(attrs={'style': 'width: 400px;'}),
            'short_description': CKEditorUploadingWidget(),
            'text': CKEditorUploadingWidget(),
        }
        model = Promotion
