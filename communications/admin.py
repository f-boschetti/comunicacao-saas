"""Admin configuration for communications app."""

from django.contrib import admin
from .models import Interaction, MessageTemplate


@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    list_display = ("client", "channel", "direction", "subject", "is_automated", "created_at")
    list_filter = ("channel", "direction", "is_automated", "company")
    search_fields = ("subject", "content", "client__name")
    date_hierarchy = "created_at"


@admin.register(MessageTemplate)
class MessageTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "template_type", "is_active", "company", "created_at")
    list_filter = ("template_type", "is_active", "company")
    search_fields = ("name", "content")
