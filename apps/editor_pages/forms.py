from django import forms

from apps.editor_pages.models import EditorPage
from utils.widgets import CKEditorUploadingWidget


class EditorPageForm(forms.ModelForm):
    class Meta:
        exclude = tuple()
        widgets = {
            'content': CKEditorUploadingWidget(),
        }
        model = EditorPage
