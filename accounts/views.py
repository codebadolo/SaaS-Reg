from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import AgencyCreationForm, AgentCreationForm , KYCDocumentForm  # Corrected import
from .models import Agency, Agent, KYCDocument
from django.contrib import messages
from django.contrib.auth.models import Group
from transactions.models import Transaction
from notifications.models import Notification
from providers.models import ServiceProvider
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .forms import AgencyCreationForm, AgencyLoginForm , AgencyUpdateForm
from .models import Agency
from django.core.mail import send_mail
import random

def home(request):
    return render(request, 'accounts/home.html')


def agency_register(request):
    if request.method == 'POST':
        form = AgencyCreationForm(request.POST, request.FILES)
        if form.is_valid():
            agency = form.save()

            # 1. Generate Default Credentials:
            default_username = agency.agency_name.replace(" ", "").lower()
            default_password = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz0123456789') for i in range(8))

            # 2. Create a User Account:
            user = User.objects.create_user(username=default_username, password=default_password)
            agency.owner = user
            agency.save()

            # 3. Redirect to Admin Change Form:
            admin_url = reverse('admin:accounts_agency_change', args=(agency.id,))  # Correct reverse usage
            return redirect(admin_url)
    else:
        form = AgencyCreationForm()
    return render(request, 'accounts/agency_register.html', {'form': form})

def agency_login(request):
    if request.method == 'POST':
        form = AgencyLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                agency = get_object_or_404(Agency, owner=user)  # Get the agency associated with the user
                return redirect('accounts:agency_detail', pk=agency.pk)
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = AgencyLoginForm()
    return render(request, 'accounts/agency_login.html', {'form': form})


@login_required
def agency_detail(request, pk):
    agency = get_object_or_404(Agency, pk=pk)

    # Authorization Check: Only the owner can view the agency detail page
    if request.user != agency.owner:
        return render(request, 'accounts/unauthorized.html', {'message': 'You are not authorized to view this agency.'})

    if request.method == 'POST':
        update_form = AgencyUpdateForm(request.POST, request.FILES, instance=agency)  # Bind to the agency instance
        kyc_form = KYCDocumentForm(request.POST, request.FILES)
        if update_form.is_valid():
            update_form.save()
            return redirect('accounts:agency_detail', pk=pk)  # Redirect to refresh the page
        if kyc_form.is_valid():
            kyc_doc = kyc_form.save(commit=False)
            kyc_doc.agency = agency
            kyc_doc.save()
            return redirect('accounts:agency_detail', pk=pk)  # Redirect to refresh the page
    else:
        update_form = AgencyUpdateForm(instance=agency)  # Initialize with agency data
        kyc_form = KYCDocumentForm()

    kyc_documents = KYCDocument.objects.filter(agency=agency)

    context = {
        'agency': agency,
        'update_form': update_form,
        'kyc_documents': kyc_documents,
        'kyc_form': kyc_form,
    }
    return render(request, 'accounts/agency_detail.html', context)


@login_required
def agent_list(request, pk):
    agency = get_object_or_404(Agency, pk=pk)
    agents = Agent.objects.filter(agency=agency)
    return render(request, 'accounts/agent_list.html', {'agency': agency, 'agents': agents})

@login_required
def agent_register(request, pk):
    agency = get_object_or_404(Agency, pk=pk)
    if request.method == 'POST':
        form = AgentCreationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Create the User object
            agent = Agent.objects.create(agency=agency, account=user)  # Create the Agent, linking to the User
            return redirect('accounts:agent_list', pk=pk)
    else:
        form = AgentCreationForm()
    return render(request, 'accounts/agent_register.html', {'agency': agency, 'form': form})