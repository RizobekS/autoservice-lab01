from django import forms

from apps.about.models import EditorContent
from utils.widgets import CKEditorUploadingWidget


class EditorContentForm(forms.ModelForm):
    class Meta:
        model = EditorContent
        exclude = tuple()
        widgets = {'text': CKEditorUploadingWidget}
