"""Admin configuration for clients app."""

from django.contrib import admin
from .models import Client, Lead


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "status", "company", "created_at")
    list_filter = ("status", "company")
    search_fields = ("name", "email", "phone", "cpf")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "phone", "source", "status", "company", "created_at")
    list_filter = ("status", "source", "company")
    search_fields = ("name", "email", "phone")
