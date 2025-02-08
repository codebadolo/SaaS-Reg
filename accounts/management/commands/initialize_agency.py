# accounts/management/commands/initialize_agency.py
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from accounts.models import Agency, Agent
from providers.models import ServiceProvider
from transactions.models import Transaction
from django.utils import timezone
import random

class Command(BaseCommand):
    help = 'Initializes an agency with providers, agents, and transactions (with default values)'

    def add_arguments(self, parser):
        # No longer require agency_name and owner_username as arguments
        # parser.add_argument('agency_name', type=str, help='Name of the agency')
        # parser.add_argument('owner_username', type=str, help='Username of the agency owner')

        parser.add_argument('--num_agents', type=int, default=2, help='Number of agents to create (default: 2)')
        parser.add_argument('--num_transactions', type=int, default=5, help='Number of transactions to create per agent (default: 5)')

    def handle(self, *args, **options):
        # Set default values for agency_name and owner_username
        agency_name = "Default Agency Name"  # Change to your desired default
        owner_username = "saas"  # Change to your desired default

        num_agents = options['num_agents']
        num_transactions = options['num_transactions']

        self.stdout.write(f"Initializing agency: {agency_name}")

        # 1. Get or create the agency owner (assuming superuser)
        User = get_user_model()
        try:
            owner = User.objects.get(username=owner_username)
        except User.DoesNotExist:
            self.stderr.write(f"Error: Owner with username '{owner_username}' not found.")
            return

        # 2. Create the Agency
        agency = Agency.objects.create(
            agency_name=agency_name,
            owner=owner,
            contact_info=f"Contact for {agency_name}"  # Example contact info
        )
        self.stdout.write(self.style.SUCCESS(f"  - Agency '{agency_name}' created."))

        # 3. Create Service Providers (if they don't exist)
        orange_money, created = ServiceProvider.objects.get_or_create(
            provider_name='Orange Money',
            defaults={'description': 'Orange Money service'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS("  - Orange Money provider created."))

        moov_money, created = ServiceProvider.objects.get_or_create(
            provider_name='Moov Money',
            defaults={'description': 'Moov Money service'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS("  - Moov Money provider created."))

        # 4. Create Agents
        for i in range(num_agents):
            agent_username = f'agent_{agency_name}_{i+1}'
            agent = Agent.objects.create(
                username=agent_username,
                agency=agency,
                first_name='Agent',
                last_name=str(i+1),
                email=f'{agent_username}@example.com'
            )
            self.stdout.write(self.style.SUCCESS(f"  - Agent '{agent_username}' created."))

            # 5. Create Transactions for each agent
            for j in range(num_transactions):
                provider = random.choice([orange_money, moov_money])
                transaction = Transaction.objects.create(
                    agent=agent,
                    provider=provider,
                    montant=random.randint(100, 1000),  # Example amount
                    type=random.choice(['deposit', 'withdrawal']),
                    date_heure=timezone.now()
                )
                self.stdout.write(f"    - Transaction {j+1} created for agent '{agent_username}'.")

        self.stdout.write(self.style.SUCCESS("Initialization complete!"))
