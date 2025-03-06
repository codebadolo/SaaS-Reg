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
from django.contrib.auth import login, authenticate, logout
# accounts/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.db.models import Sum, F , Q
from django.utils import timezone
from django.db import migrations, models
from django.contrib.auth.models import User
from .forms import ( 
AgencyCreationForm, AgencyLoginForm , AgencyUpdateForm , AgentLoginForm ,TransactionRegistrationForm , ServiceProviderRegistrationForm
)
from django.views.decorators.csrf import csrf_protect
from .models import Agency
from django.core.mail import send_mail
import random
from django.db import transaction

@csrf_protect
def home(request):
    agency_form = AgencyLoginForm()
    agent_form = AgentLoginForm()
    
    return render(request, 'accounts/home.html', {
        'agency_form': agency_form,
        'agent_form': agent_form,
    })

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
                return redirect('accounts:agency_detail', pk=agency.pk)  # Pass the pk argument
            else:
                form.add_error(None, "Invalid username or password.")
    else:
        form = AgencyLoginForm()
    return render(request, 'accounts/agency_login.html', {'form': form})


# accounts/views.py




@login_required
def agency_detail(request, pk):
    agency = get_object_or_404(Agency, pk=pk)

    # Authorization Check
    if request.user != agency.owner:
        return render(request, 'accounts/unauthorized.html', {'message': 'You are not authorized to view this agency.'})

    now = timezone.now()
    today_min = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_max = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    # Statistics Calculations
    today_payments_count = Transaction.objects.filter(
        agent__agency=agency,
        date_heure__range=(today_min, today_max)
    ).count()

    # Efficient Calculation
    provider_data = ServiceProvider.objects.filter(agency=agency).annotate(
        total_deposit=Sum(
            'transactions__montant',
            filter=Q(transactions__type='deposit')
        ),
        total_withdrawal=Sum(
            'transactions__montant',
            filter=Q(transactions__type='withdrawal')
        )
    ).values('name', 'total_deposit', 'total_withdrawal', 'balance')

    provider_deposits = {item['name']: item['total_deposit'] or 0 for item in provider_data}
    provider_withdrawals = {item['name']: item['total_withdrawal'] or 0 for item in provider_data}
    current_balances = {item['name']: item['balance'] for item in provider_data}


    top_5_withdrawals = Transaction.objects.filter(agent__agency=agency, type='withdrawal').order_by('-montant')[:5]
    top_5_deposits = Transaction.objects.filter(agent__agency=agency, type='deposit').order_by('-montant')[:5]

    recent_transactions = Transaction.objects.filter(agent__agency=agency).order_by('-date_heure')[:10]
    notifications = Notification.objects.filter(agency=agency).order_by('-timestamp')[:5]


    context = {
        'agency': agency,
        'today_payments_count': today_payments_count,
        'provider_deposits': provider_deposits,
        'provider_withdrawals': provider_withdrawals,
        'top_5_withdrawals': top_5_withdrawals,
        'top_5_deposits': top_5_deposits,
        'recent_transactions': recent_transactions,
        'notifications': notifications,
        'current_balances': current_balances,
    }
    return render(request, 'accounts/agency_detail.html', context)

'''@login_required
def agency_detail(request, pk):
    agency = get_object_or_404(Agency, pk=pk)

    #Authorization Check
    if request.user != agency.owner:
        return render(request, 'accounts/unauthorized.html', {'message': 'You are not authorized to view this agency.'})

    # Calculate Statistics
    total_agents = Agent.objects.filter(agency=agency).count()
    total_kyc_documents = agency.kyc_documents.count()  # Assuming you have a related_name in your KYCDocument model
    total_transactions = Transaction.objects.filter(agent__agency=agency).count()  # Assuming Transaction has a ForeignKey to Agent, and Agent has a ForeignKey to Agency
    recent_transactions = Transaction.objects.filter(agent__agency=agency).order_by('-date_heure')[:5]

    context = {
        'agency': agency,
        'total_agents': total_agents,
        'total_kyc_documents': total_kyc_documents,
        'total_transactions': total_transactions,
        'recent_transactions': recent_transactions,
    }
    return render(request, 'accounts/agency_detail.html', context)'''
'''
@login_required
def agency_detail(request, pk):
    agency = get_object_or_404(Agency, pk=pk)

    # Authorization Check
    if request.user != agency.owner:
        return render(request, 'accounts/unauthorized.html', {'message': 'You are not authorized to view this agency.'})

    # Calculate Statistics (Replace with your actual logic)
    total_agents = agency.agent_set.count()  # Assuming you have a reverse relation from Agency to Agent
    total_kyc_documents = agency.kyc_documents.count()  # Use the related_name 'kyc_documents'

    context = {
        'agency': agency,
        'total_agents': total_agents,
        'total_kyc_documents': total_kyc_documents,
    }
    return render(request, 'accounts/agency_detail.html', context)'''
'''@login_required
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
'''
@login_required
def logout_view(request):
    logout(request)
    return redirect('home')  # Redirect to your home page or login page

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



@login_required
def agency_kyc(request, pk):
    agency = get_object_or_404(Agency, pk=pk)

    # Authorization Check
    if request.user != agency.owner:
        return render(request, 'accounts/unauthorized.html', {'message': 'You are not authorized to view this agency.'})

    kyc_documents = KYCDocument.objects.filter(agency=agency)

    if request.method == 'POST':
        kyc_form = KYCDocumentForm(request.POST, request.FILES)
        if kyc_form.is_valid():
            kyc_doc = kyc_form.save(commit=False)
            kyc_doc.agency = agency
            kyc_doc.save()
            return redirect('accounts:agency_kyc', pk=pk)
    else:
        kyc_form = KYCDocumentForm()

    context = {
        'agency': agency,
        'kyc_documents': kyc_documents,
        'kyc_form': kyc_form,
    }
    return render(request, 'accounts/agency_kyc.html', context)


@login_required
def agency_info(request, pk):
    agency = get_object_or_404(Agency, pk=pk)

    # Authorization Check
    if request.user != agency.owner:
        return render(request, 'accounts/unauthorized.html', {'message': 'You are not authorized to view this agency.'})

    if request.method == 'POST':
        update_form = AgencyUpdateForm(request.POST, request.FILES, instance=agency)
        if update_form.is_valid():
            update_form.save()
            return redirect('accounts:agency_info', pk=pk)
    else:
        update_form = AgencyUpdateForm(instance=agency)

    context = {
        'agency': agency,
        'update_form': update_form,
    }
    return render(request, 'accounts/agency_info.html', context)


'''@login_required
def agent_detail(request, agency_pk, agent_pk):
    agency = get_object_or_404(Agency, pk=agency_pk)
    agent = get_object_or_404(Agent, pk=agent_pk)

    # Check if the agent belongs to the agency
    if agent.agency != agency:
        return render(request, 'accounts/unauthorized.html', {'message': 'Agent does not belong to this agency.'})

    # Get recent transactions of the agent
    agent_transactions = Transaction.objects.filter(agent=agent).order_by("-date_heure")[:10]  # Corrected model name

    context = {
        'agency': agency,
        'agent': agent,
        'agent_transactions': agent_transactions,  # transactions of agents.
    }
    return render(request, 'accounts/agent_detail.html', context)
'''


@login_required
def agent_detail(request, agency_pk, agent_pk):
    agency = get_object_or_404(Agency, pk=agency_pk)
    agent = get_object_or_404(Agent, pk=agent_pk)

    if agent.account.is_staff:
        return render(request, 'accounts/unauthorized.html', {'message': 'Not authorized to modify admin users.'})

    if agent.agency != agency:
        return render(request, 'accounts/unauthorized.html', {'message': 'Agent does not belong to this agency.'})

    if request.method == 'POST':
        is_active = request.POST.get('is_active') == 'on'
        agent.account.is_active = is_active
        agent.account.save()

        messages.success(request, 'Agent account status updated successfully.')
        return redirect('accounts:agent_detail', agency_pk=agency_pk, agent_pk=agent_pk)

    agent_transactions = Transaction.objects.filter(agent=agent).order_by("-date_heure")[:10]

    # Agent Statistics
    now = timezone.now()
    today_min = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_max = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    today_transactions_count = Transaction.objects.filter(agent=agent, date_heure__range=(today_min, today_max)).count()
    total_deposit_amount = Transaction.objects.filter(agent=agent, type='deposit').aggregate(Sum('montant'))['montant__sum'] or 0
    total_withdrawal_amount = Transaction.objects.filter(agent=agent, type='withdrawal').aggregate(Sum('montant'))['montant__sum'] or 0

    context = {
        'agency': agency,
        'agent': agent,
        'agent_transactions': agent_transactions,
        'today_transactions_count': today_transactions_count,
        'total_deposit_amount': total_deposit_amount,
        'total_withdrawal_amount': total_withdrawal_amount,
    }
    return render(request, 'accounts/agent_detail.html', context)

def agent_login(request):
    if request.method == 'POST':
        form = AgentLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None and user.is_staff is False:
                login(request, user)
                return redirect('accounts:agent_dashboard')  # Redirect to agent dashboard
            else:
                form.add_error(None, 'Invalid login credentials')
    else:
        form = AgentLoginForm()
    return render(request, 'accounts/agent_login.html', {'form': form})


@login_required
def agent_dashboard(request):
    # Retrieve agent-specific information here
    agent = request.user.agent  # Assuming you have a one-to-one relationship
    return render(request, 'accounts/agent_dashboard.html', {'agent': agent})

@login_required
@transaction.atomic
def transaction_register(request):
    agent = request.user.agent
    if request.method == 'POST':
        form = TransactionRegistrationForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False, agent=agent)
            transaction.agent = agent

            provider = transaction.provider

            if transaction.type == 'withdrawal' and provider.balance < transaction.montant:
                messages.error(request, f'Insufficient balance in {provider.name} to complete the withdrawal.')

                # Send notification to the agency owner
                agency_owner = agent.agency.owner
                agency = agent.agency
                notification_message = f'Withdrawal from {provider.name} failed due to insufficient balance.'
                Notification.objects.create(recipient=agency_owner, message=notification_message, agency=agency)
                Notification.objects.create(agency=agency, message=notification_message)

                return render(request, 'accounts/transaction_register.html', {'form': form})

            transaction.save()

            if transaction.type == 'deposit':
                provider.balance += transaction.montant
            elif transaction.type == 'withdrawal':
                provider.balance -= transaction.montant

            provider.save()

            return redirect('accounts:agent_dashboard')
        else:
            print(form.errors)
    else:
        form = TransactionRegistrationForm()

    transactions = Transaction.objects.filter(agent=agent).order_by('-date_heure')[:10]
    return render(request, 'accounts/transaction_register.html', {'form': form, 'transactions': transactions})