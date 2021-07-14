from django.contrib.auth.views import LogoutView
from django.urls import path, include

from .views import *

app_name = 'accounts'

appointment_urlpatterns = [
    path('new/', SubmitAppointmentView.as_view(), name='new'),
    path('', AppointmentListView.as_view(), name='list')
]

personal_area_urlpatterns = [

    path('', PersonalAreaIndex.as_view(), name='index'),
    path('garage/', PersonalAreaGarage.as_view(), name='garage'),
    path('appointments/', include((appointment_urlpatterns, 'appointment'), namespace='appointment')),
    path('edit/<int:id>/', PersonalAreaGarage.as_view(), name='remove_from_garage'),
    path('edit/', PersonalAreaEdit.as_view(), name='edit'),
]

password_reset_urlpatterns = [
    path('email/', PasswordResetView.as_view(), name='reset'),
    path('done/', PasswordResetDoneView.as_view(), name='done'),
    path('new-password/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='new-password'),
]

urlpatterns = [
    # Authentication and authorization
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('password-reset/', include((password_reset_urlpatterns, 'password'), namespace='password')),
    path('', include((personal_area_urlpatterns, 'pa'), namespace='pa')),
]
