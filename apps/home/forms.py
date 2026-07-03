from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms
from .models import Slide


class SectionAdminForm(forms.ModelForm):
    class Meta:
        exclude = tuple()

        widgets = {
            'description': CKEditorUploadingWidget(),
        }

        model = Slide
