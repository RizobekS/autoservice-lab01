from django.urls import path

from apps.editor_pages.views import EditorPageView

app_name = 'editor_pages'

# WORK_ON_QUARANTINE_URL = 'rabota-v-period-karantina'
# CORPORATE_PARKS_URL = 'obsluzhivanie-korporativnyh-parkov'
# GUARANTEES_URL = 'garantii'

urlpatterns = [
    path(f'<str:url>/', EditorPageView.as_view(), name='editor_page'),
]
