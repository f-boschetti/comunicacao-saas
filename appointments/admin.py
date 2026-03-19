"""Admin configuration for appointments app."""

from django.contrib import admin
from .models import Appointment


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("title", "client", "assigned_to", "date_time", "status", "reminder_sent")
    list_filter = ("status", "reminder_sent", "company")
    search_fields = ("title", "client__name")
    date_hierarchy = "date_time"
