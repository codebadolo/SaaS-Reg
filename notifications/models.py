from django.db import models
from django.conf import settings #To refer to the custom User model
from providers.models import ServiceProvider

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications') #Can be Agent or Agency Manager
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message
