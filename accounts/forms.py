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
        fields = ['provider', 'nom', 'prenom', 'numero_piece', 'numero_expediteur', 'numero_recepteur', 'montant', 'type']  # Exclude 'agent' from fields
        widgets = {
            'provider': forms.Select(attrs={'class': 'form-control'}),
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_piece': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_expediteur': forms.TextInput(attrs={'class': 'form-control'}),
            'numero_recepteur': forms.TextInput(attrs={'class': 'form-control'}),
            'montant': forms.NumberInput(attrs={'class': 'form-control'}),
            'type': forms.Select(attrs={'class': 'form-control'}),
        }


    def save(self, commit=True, agent=None):
        instance = super().save(commit=False)
        if agent:
            instance.agent = agent
        if commit:
            instance.save()
        return instance
# providers/forms.py
from django import forms
from providers.models import ServiceProvider

class ServiceProviderRegistrationForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ['name', 'description', 'balance']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }



class DepositForm(forms.Form):
    amount = forms.DecimalField(
        label="Deposit Amount",
        decimal_places=2,
        max_digits=10,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )