from django.db import models
from accounts.models import Agency, Agent
class ServiceProvider(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='service_providers')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name
    
    
