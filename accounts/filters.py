import django_filters
from transactions.models import Transaction
from providers.models import ServiceProvider
from .models import Agent
import django_filters
from django import forms



import django_filters
from django import forms


class TransactionFilter(django_filters.FilterSet):
    date_range = django_filters.DateFromToRangeFilter(
        field_name='date_heure',
        label='Date Range (YYYY-MM-DD)',
        widget=django_filters.widgets.RangeWidget(
            attrs={'type': 'date', 'class': 'form-control'}
        )
    )
    
    montant_min = django_filters.NumberFilter(
        field_name='montant', 
        lookup_expr='gte',
        label='Minimum Amount',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    montant_max = django_filters.NumberFilter(
        field_name='montant', 
        lookup_expr='lte',
        label='Maximum Amount',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    provider = django_filters.ModelChoiceFilter(
        queryset=ServiceProvider.objects.all(),
        label='Service Provider',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    agent = django_filters.ModelChoiceFilter(
        queryset=Agent.objects.all(),
        label='Responsible Agent',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    type = django_filters.ChoiceFilter(
        choices=Transaction.TRANSACTION_TYPES,
        label='Transaction Type',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    numero_piece = django_filters.CharFilter(
        field_name='numero_piece',
        lookup_expr='icontains',
        label='ID Document',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    numero_expediteur = django_filters.CharFilter(
        field_name='numero_expediteur',
        lookup_expr='icontains',
        label='Sender Number',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    numero_recepteur = django_filters.CharFilter(
        field_name='numero_recepteur',
        lookup_expr='icontains',
        label='Receiver Number',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Transaction
        fields = {
            'type': ['exact'],
            'numero_piece': ['icontains'],
            'numero_expediteur': ['icontains'],
            'numero_recepteur': ['icontains'],
        }
