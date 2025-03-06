
# accounts/urls.py
from django.urls import path
from . import views
from notifications.views  import notification_list

app_name = 'accounts'

urlpatterns = [
     #path('list/', notification_list, name='notification_list'),
     path('', views.home, name='home'),  # Maps / to the home view
     path('agency/register/', views.agency_register, name='agency_register'),
     path('logout/', views.logout_view, name='logout'),
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
     path('agency/<int:agency_pk>/notifications/', notification_list, name='notification_list'),

]
