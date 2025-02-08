# notifications/urls.py
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('list/', views.notification_list, name='notification_list'),
    # ... other URL patterns ...
]
