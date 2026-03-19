"""Forms for clients app."""

from django import forms
from .models import Client, Lead


class ClientForm(forms.ModelForm):
    """Form for creating and editing clients."""

    class Meta:
        model = Client
        fields = ("name", "email", "phone", "cpf", "date_of_birth", "address", "notes", "status", "tags")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome completo"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-mail"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "(00) 00000-0000"}),
            "cpf": forms.TextInput(attrs={"class": "form-control", "placeholder": "000.000.000-00"}),
            "date_of_birth": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "tags": forms.TextInput(attrs={"class": "form-control", "placeholder": "tag1, tag2, tag3"}),
        }


class LeadForm(forms.ModelForm):
    """Form for creating and editing leads."""

    class Meta:
        model = Lead
        fields = ("name", "email", "phone", "source", "status", "notes", "assigned_to")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-mail"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "(00) 00000-0000"}),
            "source": forms.Select(attrs={"class": "form-select"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "assigned_to": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company:
            self.fields["assigned_to"].queryset = company.users.all()
