"""Views for audit log app."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import AuditLog


@login_required
def audit_log_list(request):
    """List audit logs for the company."""
    if not request.user.is_admin_user:
        messages.error(request, "Acesso restrito a administradores.")
        return redirect("dashboard:index")

    company = request.user.company
    logs = AuditLog.objects.filter(user__company=company).select_related("user")

    action_filter = request.GET.get("action", "")
    user_filter = request.GET.get("user_id", "")

    if action_filter:
        logs = logs.filter(action=action_filter)
    if user_filter:
        logs = logs.filter(user_id=user_filter)

    logs = logs[:200]

    users = company.users.all() if company else []

    return render(request, "auditlog/audit_log_list.html", {
        "logs": logs,
        "action_filter": action_filter,
        "user_filter": user_filter,
        "action_choices": AuditLog.Action.choices,
        "users": users,
    })
