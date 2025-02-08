# accounts/forms.py
from django import forms
from .models import Agency, Agent, KYCDocument
from django.contrib.auth import get_user_model

from django.contrib.auth.forms import UserCreationForm

class AgencyCreationForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['agency_name', 'contact_info', 'logo']  # Exclude owner for now

class AgencyLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

class AgencyUpdateForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['agency_name', 'contact_info', 'logo']  # Include all editable fields

class KYCDocumentForm(forms.ModelForm):
    class Meta:
        model = KYCDocument
        fields = ['document_name', 'document_file']  # Specify the fields you want in the form
        

class AgentCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()  # Ensure it uses the project's user model
        fields = UserCreationForm.Meta.fields + ('email', 'first_name', 'last_name')