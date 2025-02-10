from django.shortcuts import render

# providers/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from accounts.models import Agency
from .models import ServiceProvider
from accounts.forms import ServiceProviderRegistrationForm, DepositForm

@login_required
def service_provider_list(request, agency_pk):
    agency = get_object_or_404(Agency, pk=agency_pk)

    if request.user != agency.owner:
        return render(request, 'accounts/unauthorized.html', {'message': 'You are not authorized to view this agency.'})

    if request.method == 'POST' and 'register_provider' in request.POST:
        provider_form = ServiceProviderRegistrationForm(request.POST)
        if provider_form.is_valid():
            new_provider = provider_form.save(commit=False)
            new_provider.agency = agency
            new_provider.save()
            messages.success(request, 'New service provider registered successfully.')
            return redirect('providers:service_provider_list', agency_pk=agency_pk)
        else:
            messages.error(request, 'Provider Registration Failed: Please correct the errors below.')
    else:
        provider_form = ServiceProviderRegistrationForm()

    service_providers = ServiceProvider.objects.filter(agency=agency)

    context = {
        'agency': agency,
        'provider_form': provider_form,
        'service_providers': service_providers,
    }
    return render(request, 'providers/service_provider_list.html', context)


@login_required
@transaction.atomic
def service_provider_detail(request, agency_pk, provider_pk):
    agency = get_object_or_404(Agency, pk=agency_pk)
    try:
        provider = ServiceProvider.objects.select_for_update().get(pk=provider_pk, agency=agency)
    except ServiceProvider.DoesNotExist:
        return render(request, 'accounts/unauthorized.html', {'message': 'No access to the service provider'})

    if request.method == 'POST':
        deposit_form = DepositForm(request.POST)
        if deposit_form.is_valid():
            amount = deposit_form.cleaned_data['amount']
            provider.balance += amount
            provider.save()
            messages.success(request, f'Successfully deposited {amount} into {provider.name}.')
            return redirect('providers:service_provider_detail', agency_pk=agency_pk, provider_pk=provider_pk)
        else:
            messages.error(request, 'Invalid deposit amount. Please correct the errors below.')
    else:
        deposit_form = DepositForm()

    context = {
        'agency': agency,
        'provider': provider,
        'deposit_form': deposit_form,
    }
    return render(request, 'providers/service_provider_detail.html', context)
