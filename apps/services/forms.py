from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import *


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
            'favourite_text': CKEditorWidget(),
            'short_description': forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
        }

        model = Product
