from django import forms
from django.core.validators import validate_image_file_extension
from transliterate import translit

from apps.work_gallery.models import Work, Image
from utils.widgets import CKEditorWidget


class WorkAdminForm(forms.ModelForm):
    multiple_images = forms.FileField(label='Добавить сразу несколько изображений', widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    def clean_multiple_images(self):
        """Make sure only images were uploaded."""
        for upload in self.files.getlist("images"):
            validate_image_file_extension(upload)

    def save_multiple_images(self, work):
        """Save each uploaded image."""
        for upload in self.files.getlist('multiple_images'):
            upload.name = translit(upload.name, 'ru', reversed=True)
            image = Image(work=work, image=upload)
            image.save()

    class Meta:
        model = Work
        exclude = tuple()

        widgets = {
            'text': CKEditorWidget(),
        }
