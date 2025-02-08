from django.db import models

class ServiceProvider(models.Model):
    provider_name = models.CharField(max_length=100, unique=True)
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0.00)

    def __str__(self):
        return self.provider_name
