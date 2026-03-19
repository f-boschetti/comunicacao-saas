"""URL patterns for auditlog app."""

from django.urls import path
from . import views

app_name = "auditlog"

urlpatterns = [
    path("", views.audit_log_list, name="audit_log_list"),
]
