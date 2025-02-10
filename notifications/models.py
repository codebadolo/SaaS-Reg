from django.db import models
from django.conf import settings #To refer to the custom User model
from providers.models import ServiceProvider
from django.contrib.auth import get_user_model
from accounts.models import Agency, Agent
class Notification(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    recipient = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='notifications', null=True, blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message