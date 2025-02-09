"""
URL configuration for saasmain project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
     path('', views.home, name='home'),  # Maps / to the home view
      path('agency/register/', views.agency_register, name='agency_register'),
    path('agency/login/', views.agency_login, name='agency_login'),
        path('agency/<int:pk>/', views.agency_detail, name='agency_detail'),
            path('agency/<int:pk>/agents/', views.agent_list, name='agent_list'),
    path('agency/<int:pk>/agents/register/', views.agent_register, name='agent_register'),
      path('agency/<int:pk>/info/', views.agency_info, name='agency_info'),
      path('agency/<int:pk>/kyc/', views.agency_kyc, name='agency_kyc'),  
         path('agency/<int:pk>/agents/', views.agent_list, name='agent_list'),
    path('agency/<int:pk>/agents/register/', views.agent_register, name='agent_register'),
      path('agency/<int:agency_pk>/agents/<int:agent_pk>/', views.agent_detail, name='agent_detail'),
         path('agent/login/', views.agent_login, name='agent_login'),
    path('agent/dashboard/', views.agent_dashboard, name='agent_dashboard'),
        path('transaction/register/', views.transaction_register, name='transaction_register'),# New URL pattern
]
    # Other URL patterns
    # 

    # ... other URL patterns ...

