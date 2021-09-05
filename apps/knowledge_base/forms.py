from django import forms
from django.core.exceptions import ValidationError

from apps.knowledge_base.models import FaqEntry, Symptom
from utils.widgets import CKEditorUploadingWidget


class FaqEntryAdminForm(forms.ModelForm):
    def clean(self):
        answered = self.cleaned_data.get('answered')
        title = self.cleaned_data.get('title')
        url = self.cleaned_data.get('url')
        answer = self.cleaned_data.get('answer')
        master = self.cleaned_data.get('master')
        date = self.cleaned_data.get('date')

        if answered:
            fieldnames = []
            if not title:
                fieldnames.append('title')
            if not url:
                fieldnames.append('url')
            if not answer:
                fieldnames.append('answer')
            if not master:
                fieldnames.append('master')
            if not date:
                fieldnames.append('date')
            if fieldnames:
                raise ValidationError({item: 'При галочке на поле "Отвечен" данное поле не может быть пустым' for item in fieldnames})
        return self.cleaned_data

    class Meta:
        exclude = tuple()

        model = FaqEntry
        widgets = {
            'title': forms.Textarea(attrs={'style': 'width: 400px; height: 34px;'}),
            'question': forms.Textarea(attrs={'style': 'width: 800px; height: 128px;'}),
            'answer': CKEditorUploadingWidget(),
        }


class SymptomAdminForm(forms.ModelForm):
    class Meta:
        exclude = tuple()

        model = Symptom
        widgets = {
            'title': forms.Textarea(attrs={'style': 'width: 400px; height: 34px;'}),
            'answer': CKEditorUploadingWidget(),
        }


class AskQuestionForm(forms.ModelForm):
    class Meta:
        fields = ('question', 'asking_name', 'asking_email')
        model = FaqEntry
