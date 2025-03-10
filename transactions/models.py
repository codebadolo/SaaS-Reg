from django.db import models
from accounts.models import Agent
from providers.models import ServiceProvider



class Transaction(models.Model):
    TRANSACTION_TYPES = (
    ('deposit', 'Deposit'),
    ('withdrawal', 'Withdrawal'),
)
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name='transactions')
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name='transactions')
    nom = models.CharField(max_length=200)
    prenom = models.CharField(max_length=200)
    numero_piece = models.CharField(max_length=50)
    numero_expediteur = models.CharField(max_length=50)
    numero_recepteur = models.CharField(max_length=50)
    montant = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    date_heure = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction ID: {self.id}"
