from ckeditor.widgets import CKEditorWidget as BaseCKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget as BaseCKEditorUploadingWidget
from django.conf import settings
from django.templatetags.static import static
from js_asset import JS


class CKEditorUploadingWidget(BaseCKEditorUploadingWidget):
    """
        Overrides CKEditor widget with custom configurations
    """

    class Media:
        js = (
            JS(
                "ckeditor/ckeditor-init.js",
                {
                    "id": "ckeditor-init-script",
                    "data-ckeditor-basepath": getattr(
                        settings,
                        "CKEDITOR_BASEPATH",
                        static("ckeditor/ckeditor/"),
                    ),
                },
            ),
            "ckeditor/ckeditor/ckeditor.js",
            static('js/custom/ckeditor.js')
        )


class CKEditorWidget(BaseCKEditorWidget):
    """
        Overrides CKEditor widget with custom configurations
    """

    class Media:
        js = (
            JS(
                "ckeditor/ckeditor-init.js",
                {
                    "id": "ckeditor-init-script",
                    "data-ckeditor-basepath": getattr(
                        settings,
                        "CKEDITOR_BASEPATH",
                        static("ckeditor/ckeditor/"),
                    ),
                },
            ),
            "ckeditor/ckeditor/ckeditor.js",
            static('js/custom/ckeditor.js')
        )
