# accounts/forms.py
from django import forms
from .models import Agency, Agent, KYCDocument
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from  transactions.models import Transaction
class AgencyCreationForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['agency_name', 'contact_info', 'logo']

        widgets = {
            'agency_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # No widget customization for 'logo' as it's a FileField (handled differently)
        }

class AgencyLoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class AgencyUpdateForm(forms.ModelForm):
    class Meta:
        model = Agency
        fields = ['agency_name', 'contact_info', 'logo']
        widgets = {
            'agency_name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_info': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            # No widget customization for 'logo' as it's a FileField (handled differently)
        }

class KYCDocumentForm(forms.ModelForm):
    class Meta:
        model = KYCDocument
        fields = ['document_name', 'document_file']
        widgets = {
            'document_name': forms.TextInput(attrs={'class': 'form-control'}),
            'document_file': forms.FileInput(attrs={'class': 'form-control'}),  # Might need custom styling
        }

class AgentCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'  # Apply to all fields
class AgentLoginForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    


class TransactionRegistrationForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['provider', 'nom', 'prenom', 'numero_piece', 'numero_expediteur', 'numero_recepteur', 'montant', 'type', 'agent']  # Add 'agent' to fields
        widgets = {
            'provider': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_piece': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_expediteur': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_recepteur': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
            'agent': forms.HiddenInput(),  # Directly set HiddenInput in widgets
        }
