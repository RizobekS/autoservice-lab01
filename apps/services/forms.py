from django import forms

from utils.widgets import CKEditorUploadingWidget
from .models import Section, Product


class SectionAdminForm(forms.ModelForm):
    class Meta:
        exclude = tuple()

        widgets = {
            'description': CKEditorUploadingWidget(),
            'short_description': forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
        }

        model = Section


class ProductAdminForm(forms.ModelForm):
    class Meta:
        exclude = tuple()

        widgets = {
            'description': CKEditorUploadingWidget(),
            'short_description': forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
        }

        model = Product
