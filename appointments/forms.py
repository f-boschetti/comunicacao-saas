"""Forms for appointments app."""

from django import forms
from .models import Appointment


class AppointmentForm(forms.ModelForm):
    """Form for creating and editing appointments."""

    class Meta:
        model = Appointment
        fields = ("title", "client", "assigned_to", "description", "date_time",
                  "duration_minutes", "status", "reminder_time_hours", "notes")
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Título do agendamento"}),
            "client": forms.Select(attrs={"class": "form-select"}),
            "assigned_to": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "date_time": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
            "duration_minutes": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "reminder_time_hours": forms.NumberInput(attrs={"class": "form-control"}),
            "notes": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }

    def __init__(self, *args, company=None, **kwargs):
        super().__init__(*args, **kwargs)
        if company:
            self.fields["client"].queryset = company.clients.filter(status="active")
            self.fields["assigned_to"].queryset = company.users.all()
