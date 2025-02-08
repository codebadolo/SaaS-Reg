# providers/urls.py
from django.urls import path
from . import views

app_name = 'providers'

urlpatterns = [
    path('list/', views.provider_list, name='provider_list'),
    # ... other URL patterns ...
]
