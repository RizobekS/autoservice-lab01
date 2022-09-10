from django.urls import path

from apps.editor_pages.views import EditorPageView

app_name = 'editor_pages'

WORK_ON_QUARANTINE_URL = 'rabota-v-period-karantina'
CORPORATE_PARKS_URL = 'obsluzhivanie-korporativnyh-parkov'
GUARANTEES_URL = 'garantii'

urlpatterns = [
    path(f'{WORK_ON_QUARANTINE_URL}/', EditorPageView.as_view(url=WORK_ON_QUARANTINE_URL), name='work_on_quarantine'),
    path(f'{CORPORATE_PARKS_URL}/', EditorPageView.as_view(url=CORPORATE_PARKS_URL), name='corporate_parks'),
    path(f'{GUARANTEES_URL}/', EditorPageView.as_view(url=GUARANTEES_URL), name='guarantees'),
    path('reviews/', EditorPageView.as_view(url='reviews'), name='reviews')
]
