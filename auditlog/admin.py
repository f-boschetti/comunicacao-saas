"""Admin configuration for auditlog app."""

from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("user", "action", "model_name", "object_repr", "ip_address", "timestamp")
    list_filter = ("action", "model_name")
    search_fields = ("object_repr", "user__username")
    date_hierarchy = "timestamp"
    readonly_fields = ("user", "action", "model_name", "object_id", "object_repr",
                       "changes", "ip_address", "user_agent", "timestamp")
