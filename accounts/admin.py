# accounts/admin.py
from django.contrib import admin
from .models import Agency, Agent, KYCDocument  # Import your models

# accounts/admin.py
from django.contrib import admin
from .models import Agency, Agent, KYCDocument


class AgencyAdmin(admin.ModelAdmin):
    list_display = ('agency_name', 'owner', 'contact_info', 'created_at')  # Customize columns
    list_filter = ('owner',)  # Enable filtering by owner
    search_fields = ('agency_name', 'contact_info')  # Enable searching

admin.site.register(Agency , AgencyAdmin)
admin.site.register(Agent)
admin.site.register(KYCDocument)

