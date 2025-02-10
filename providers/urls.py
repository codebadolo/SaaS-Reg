# providers/urls.py
from django.urls import path
from . import views

app_name = 'providers'

urlpatterns = [
    path('agency/<int:agency_pk>/', views.service_provider_list, name='service_provider_list'),
    path('agency/<int:agency_pk>/provider/<int:provider_pk>/', views.service_provider_detail, name='service_provider_detail'),
]
