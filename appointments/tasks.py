"""Celery tasks for appointment reminders."""

from celery import shared_task
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_appointment_reminders():
    """Send reminders for upcoming appointments."""
    from .models import Appointment
    from communications.services import send_reminder

    now = timezone.now()
    appointments = Appointment.objects.filter(
        status__in=["scheduled", "confirmed"],
        reminder_sent=False,
    )

    for appointment in appointments:
        reminder_time = appointment.date_time - timedelta(hours=appointment.reminder_time_hours)
        if now >= reminder_time and now < appointment.date_time:
            send_reminder(appointment)
            appointment.reminder_sent = True
            appointment.save(update_fields=["reminder_sent"])


@shared_task
def mark_no_show_appointments():
    """Mark appointments as no-show if past due and still scheduled."""
    from .models import Appointment

    threshold = timezone.now() - timedelta(hours=2)
    Appointment.objects.filter(
        status="scheduled",
        date_time__lt=threshold,
    ).update(status="no_show")
