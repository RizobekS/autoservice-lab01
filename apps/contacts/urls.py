from django.urls import path

from apps.contacts.views import ContactsView

app_name = 'contacts'

urlpatterns = [
    path('', ContactsView.as_view(), name='contacts')
]
