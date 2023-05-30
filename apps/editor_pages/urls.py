from django.urls import path, register_converter

from apps.editor_pages.models import EditorPage
from apps.editor_pages.views import EditorPageView
from utils.urlconverters import url_converter_factory

app_name = 'editor_pages'

# WORK_ON_QUARANTINE_URL = 'rabota-v-period-karantina'
# CORPORATE_PARKS_URL = 'obsluzhivanie-korporativnyh-parkov'
# GUARANTEES_URL = 'garantii'
EditorPageUrlFilter = url_converter_factory(EditorPage)
register_converter(EditorPageUrlFilter, 'editor_page_filter')

urlpatterns = [
    path(f'<editor_page_filter:url>/', EditorPageView.as_view(), name='editor_page'),
]
