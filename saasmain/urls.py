# core/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # Directs URLs starting with 'accounts/' to accounts app
    path('transactions/', include('transactions.urls')),
    path('providers/', include('providers.urls')),
    path('notifications/', include('notifications.urls')),
    # Add other app URLs here
    path('', include('accounts.urls')), # If you want the accounts app to handle the root URL
]
