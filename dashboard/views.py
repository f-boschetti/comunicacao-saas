"""Views for dashboard app."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta

from clients.models import Client, Lead
from appointments.models import Appointment
from communications.models import Interaction


@login_required
def index(request):
    """Main dashboard view with analytics."""
    company = request.user.company
    if not company:
        return render(request, "dashboard/no_company.html")

    now = timezone.now()
    today = now.date()
    week_start = today - timedelta(days=today.weekday())
    month_start = today.replace(day=1)

    # Counts
    total_clients = Client.objects.filter(company=company, status="active").count()
    total_leads = Lead.objects.filter(company=company).exclude(status="converted").exclude(status="lost").count()
    today_appointments = Appointment.objects.filter(
        company=company, date_time__date=today
    ).count()
    upcoming_appointments = Appointment.objects.filter(
        company=company,
        date_time__gte=now,
        status__in=["scheduled", "confirmed"],
    ).order_by("date_time")[:5]

    # Recent activity
    recent_interactions = Interaction.objects.filter(
        company=company
    ).select_related("client").order_by("-created_at")[:10]

    recent_leads = Lead.objects.filter(company=company).order_by("-created_at")[:5]

    # Stats for charts
    lead_stats = Lead.objects.filter(company=company).values("status").annotate(count=Count("id"))
    appointment_stats = Appointment.objects.filter(
        company=company, date_time__date__gte=month_start
    ).values("status").annotate(count=Count("id"))

    # New clients this month
    new_clients_month = Client.objects.filter(
        company=company, created_at__date__gte=month_start
    ).count()

    # New leads this week
    new_leads_week = Lead.objects.filter(
        company=company, created_at__date__gte=week_start
    ).count()

    context = {
        "total_clients": total_clients,
        "total_leads": total_leads,
        "today_appointments": today_appointments,
        "upcoming_appointments": upcoming_appointments,
        "recent_interactions": recent_interactions,
        "recent_leads": recent_leads,
        "lead_stats": list(lead_stats),
        "appointment_stats": list(appointment_stats),
        "new_clients_month": new_clients_month,
        "new_leads_week": new_leads_week,
    }
    return render(request, "dashboard/index.html", context)
