"""Forms for accounts app."""

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import Company

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    """Registration form for new users."""

    company_name = forms.CharField(
        max_length=200,
        required=True,
        label="Nome da empresa",
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome da sua empresa"}),
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "phone", "password1", "password2")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nome"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Sobrenome"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "E-mail"}),
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Usuário"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "placeholder": "Telefone"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["password1"].widget.attrs.update({"class": "form-control", "placeholder": "Senha"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "placeholder": "Confirmar senha"})


class CustomAuthenticationForm(AuthenticationForm):
    """Login form."""

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Usuário ou e-mail"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Senha"})
    )


class UserProfileForm(forms.ModelForm):
    """Form for editing user profile."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
        }


class CompanyForm(forms.ModelForm):
    """Form for editing company details."""

    class Meta:
        model = Company
        fields = ("name", "cnpj", "email", "phone", "address", "website", "description", "logo")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "cnpj": forms.TextInput(attrs={"class": "form-control", "placeholder": "00.000.000/0000-00"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }
