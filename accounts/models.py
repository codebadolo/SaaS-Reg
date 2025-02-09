# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

# Remove the get_default_agency function as it's no longer needed

class Agency(models.Model):
    agency_name = models.CharField(max_length=200, unique=True)
    contact_info = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank = True)  # Make it nullable and blank
    logo = models.ImageField(upload_to='agency_logos/', blank=True, null=True)  # Optional logo

    def __str__(self):
        return self.agency_name


class KYCDocument(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE, related_name='kyc_documents' )
    document_name = models.CharField(max_length=255)  # e.g., "Business License," "Tax ID"
    document_file = models.FileField(upload_to='kyc_documents/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.document_name} for {self.agency.agency_name}"


class Agent(AbstractUser):
    agency = models.ForeignKey('Agency',  on_delete=models.CASCADE   , null = True, blank = True) # Set nullable and blank
    is_manager = models.BooleanField(default=False)
    account = models.OneToOneField(get_user_model(), on_delete=models.CASCADE , primary_key=True) 
    groups = models.ManyToManyField(
        Group,
        verbose_name=('groups'),
        blank=True,
        help_text=(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="agent_groups",
        related_query_name="agent_group",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=('user permissions'),
        blank=True,
        help_text=('Specific permissions for this user.'),
        related_name="agent_permissions",
        related_query_name="agent_permission",
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = _("Agent")
        verbose_name_plural = _("Agents")
