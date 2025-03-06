# transactions/urls.py
from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
  path('register/', views.transaction_registerr, name='transaction_register'),  # Correct spelling

]
