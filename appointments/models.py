"""Models for appointments/scheduling."""

from django.conf import settings
from django.db import models


class Appointment(models.Model):
    """Appointment model for scheduling."""

    class Status(models.TextChoices):
        SCHEDULED = "scheduled", "Agendado"
        CONFIRMED = "confirmed", "Confirmado"
        COMPLETED = "completed", "Concluído"
        CANCELLED = "cancelled", "Cancelado"
        NO_SHOW = "no_show", "Não compareceu"

    company = models.ForeignKey(
        "accounts.Company",
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Empresa",
    )
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.CASCADE,
        related_name="appointments",
        verbose_name="Cliente",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="appointments",
        verbose_name="Profissional",
    )
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(blank=True, verbose_name="Descrição")
    date_time = models.DateTimeField(verbose_name="Data e hora")
    duration_minutes = models.PositiveIntegerField(default=60, verbose_name="Duração (minutos)")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SCHEDULED,
        verbose_name="Status",
    )
    reminder_sent = models.BooleanField(default=False, verbose_name="Lembrete enviado")
    reminder_time_hours = models.PositiveIntegerField(
        default=24,
        verbose_name="Antecedência do lembrete (horas)",
    )
    notes = models.TextField(blank=True, verbose_name="Observações")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_appointments",
        verbose_name="Criado por",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Agendamento"
        verbose_name_plural = "Agendamentos"
        ordering = ["date_time"]

    def __str__(self):
        return f"{self.title} - {self.client.name} ({self.date_time:%d/%m/%Y %H:%M})"

    @property
    def end_time(self):
        from datetime import timedelta
        return self.date_time + timedelta(minutes=self.duration_minutes)
