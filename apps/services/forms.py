from django import forms

from utils.widgets import CKEditorUploadingWidget, CKEditorWidget
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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['car_pack'].empty_label = 'Все машины'

    class Meta:
        exclude = tuple()

        widgets = {
            'description': CKEditorUploadingWidget(),
            'master_advise': CKEditorUploadingWidget(),
            'short_description': forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
            'anons': forms.Textarea(attrs={"style": "width: 400px; height: 68px;"}),
            'homepage_description': CKEditorWidget(),
            'branches': forms.CheckboxSelectMultiple(),
        }

        model = Product
