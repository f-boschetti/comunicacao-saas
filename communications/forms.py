"""Forms for communications app."""

from django import forms
from .models import Interaction, MessageTemplate


class InteractionForm(forms.ModelForm):
    """Form for logging interactions."""

    class Meta:
        model = Interaction
        fields = ("client", "channel", "direction", "subject", "content")
        widgets = {
            "client": forms.Select(attrs={"class": "form-select"}),
            "channel": forms.Select(attrs={"class": "form-select"}),
            "direction": forms.Select(attrs={"class": "form-select"}),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Assunto"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Conteúdo da mensagem"}),
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company:
            self.fields["client"].queryset = company.clients.filter(status="active")


class MessageTemplateForm(forms.ModelForm):
    """Form for creating and editing message templates."""

    class Meta:
        model = MessageTemplate
        fields = ("name", "template_type", "subject", "content", "is_active")
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "template_type": forms.Select(attrs={"class": "form-select"}),
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 5,
                                              "placeholder": "Use {nome}, {empresa}, {data}, {hora} como variáveis."}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class SendMessageForm(forms.Form):
    """Form for sending a message to a client."""

    CHANNEL_CHOICES = [
        ("email", "E-mail"),
        ("whatsapp", "WhatsApp"),
        ("instagram", "Instagram"),
    ]

    client = forms.IntegerField(widget=forms.HiddenInput())
    channel = forms.ChoiceField(
        choices=CHANNEL_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Canal",
    )
    subject = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Assunto (para e-mail)"}),
        label="Assunto",
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 4, "placeholder": "Mensagem"}),
        label="Mensagem",
    )
    template = forms.ModelChoiceField(
        queryset=MessageTemplate.objects.none(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
        label="Usar template",
        empty_label="-- Selecione um template --",
    )

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company:
            self.fields["template"].queryset = MessageTemplate.objects.filter(
                company=company, is_active=True
            )


class AIResponseForm(forms.Form):
    """Form for generating AI responses."""

    prompt = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3,
                                     "placeholder": "Digite a mensagem do cliente para gerar uma resposta automática..."}),
        label="Mensagem do cliente",
    )
    context = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 2,
                                     "placeholder": "Contexto adicional (opcional)"}),
        label="Contexto",
    )
