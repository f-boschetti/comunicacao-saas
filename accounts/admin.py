"""Admin configuration for accounts app."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Company


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "role", "company", "is_active")
    list_filter = ("role", "is_active", "company")
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Informações adicionais", {"fields": ("role", "phone", "company")}),
    )


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "cnpj", "email", "phone", "is_active", "created_at")
    list_filter = ("is_active",)
    search_fields = ("name", "cnpj", "email")
    prepopulated_fields = {"slug": ("name",)}
