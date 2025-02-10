# notifications/urls.py
from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('list/', views.notification_list, name='notification_list'),
        path('mark_as_read/<int:notification_id>/', views.mark_as_read, name='mark_as_read'),
         path('', views.notification_list, name='notification_list'),
    # ... other URL patterns ...
]
