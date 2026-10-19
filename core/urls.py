from django.urls import path
from telemedicine import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'), # இங்கே 'views.login_page' இருக்கணும்
    path('doctor/register/', views.doctor_register, name='doctor_register'),
    path('doctor/login/', views.doctor_login, name='doctor_login'),
    path('patient/dashboard/', views.patient_dashboard, name='patient_dashboard'),
    path('doctor/dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    path('logout/', views.logout_user, name='logout'),
    # புது மாடியூல்ஸ்:
    path('update-profile/', views.update_profile, name='update_profile'),
    path('cancel-appointment/<int:appt_id>/', views.cancel_appointment, name='cancel_appointment'),
]