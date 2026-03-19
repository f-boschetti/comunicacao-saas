"""Views for appointments app."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q

from .models import Appointment
from .forms import AppointmentForm


@login_required
def appointment_list(request):
    """List all appointments for the user's company."""
    company = request.user.company
    if not company:
        messages.error(request, "Você não está associado a nenhuma empresa.")
        return redirect("dashboard:index")

    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")
    date_filter = request.GET.get("date", "")

    appointments = Appointment.objects.filter(company=company)
    if query:
        appointments = appointments.filter(
            Q(title__icontains=query) | Q(client__name__icontains=query)
        )
    if status_filter:
        appointments = appointments.filter(status=status_filter)
    if date_filter == "today":
        today = timezone.now().date()
        appointments = appointments.filter(date_time__date=today)
    elif date_filter == "week":
        today = timezone.now().date()
        from datetime import timedelta
        week_end = today + timedelta(days=7)
        appointments = appointments.filter(date_time__date__gte=today, date_time__date__lte=week_end)
    elif date_filter == "upcoming":
        appointments = appointments.filter(date_time__gte=timezone.now())

    return render(request, "appointments/appointment_list.html", {
        "appointments": appointments,
        "query": query,
        "status_filter": status_filter,
        "date_filter": date_filter,
        "status_choices": Appointment.Status.choices,
    })


@login_required
def appointment_create(request):
    """Create a new appointment."""
    company = request.user.company
    if request.method == "POST":
        form = AppointmentForm(request.POST, company=company)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.company = company
            appointment.created_by = request.user
            appointment.save()
            messages.success(request, f"Agendamento '{appointment.title}' criado com sucesso!")
            return redirect("appointments:appointment_list")
    else:
        form = AppointmentForm(company=company)
    return render(request, "appointments/appointment_form.html", {"form": form, "title": "Novo Agendamento"})


@login_required
def appointment_detail(request, pk):
    """View appointment details."""
    appointment = get_object_or_404(Appointment, pk=pk, company=request.user.company)
    return render(request, "appointments/appointment_detail.html", {"appointment": appointment})


@login_required
def appointment_edit(request, pk):
    """Edit an appointment."""
    appointment = get_object_or_404(Appointment, pk=pk, company=request.user.company)
    company = request.user.company
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment, company=company)
        if form.is_valid():
            form.save()
            messages.success(request, f"Agendamento '{appointment.title}' atualizado com sucesso!")
            return redirect("appointments:appointment_detail", pk=appointment.pk)
    else:
        form = AppointmentForm(instance=appointment, company=company)
    return render(request, "appointments/appointment_form.html", {
        "form": form, "title": "Editar Agendamento", "appointment": appointment
    })


@login_required
def appointment_delete(request, pk):
    """Delete an appointment."""
    appointment = get_object_or_404(Appointment, pk=pk, company=request.user.company)
    if request.method == "POST":
        title = appointment.title
        appointment.delete()
        messages.success(request, f"Agendamento '{title}' excluído com sucesso!")
        return redirect("appointments:appointment_list")
    return render(request, "appointments/appointment_confirm_delete.html", {"appointment": appointment})


@login_required
def appointment_calendar(request):
    """Calendar view for appointments."""
    company = request.user.company
    if not company:
        return redirect("dashboard:index")

    appointments = Appointment.objects.filter(
        company=company,
        status__in=["scheduled", "confirmed"],
    ).select_related("client", "assigned_to")

    events = []
    for apt in appointments:
        events.append({
            "id": apt.pk,
            "title": f"{apt.title} - {apt.client.name}",
            "start": apt.date_time.isoformat(),
            "end": apt.end_time.isoformat(),
            "status": apt.status,
        })

    import json
    return render(request, "appointments/calendar.html", {
        "events_json": json.dumps(events),
    })
