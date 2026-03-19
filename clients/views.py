"""Views for clients app."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q

from .models import Client, Lead
from .forms import ClientForm, LeadForm


@login_required
def client_list(request):
    """List all clients for the user's company."""
    company = request.user.company
    if not company:
        messages.error(request, "Você não está associado a nenhuma empresa.")
        return redirect("dashboard:index")

    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")

    clients = Client.objects.filter(company=company)
    if query:
        clients = clients.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query))
    if status_filter:
        clients = clients.filter(status=status_filter)

    return render(request, "clients/client_list.html", {
        "clients": clients,
        "query": query,
        "status_filter": status_filter,
        "status_choices": Client.Status.choices,
    })


@login_required
def client_create(request):
    """Create a new client."""
    company = request.user.company
    if request.method == "POST":
        form = ClientForm(request.POST)
        if form.is_valid():
            client = form.save(commit=False)
            client.company = company
            client.created_by = request.user
            client.save()
            messages.success(request, f"Cliente '{client.name}' criado com sucesso!")
            return redirect("clients:client_detail", pk=client.pk)
    else:
        form = ClientForm()
    return render(request, "clients/client_form.html", {"form": form, "title": "Novo Cliente"})


@login_required
def client_detail(request, pk):
    """View client details."""
    client = get_object_or_404(Client, pk=pk, company=request.user.company)
    interactions = client.interactions.all()[:20]
    appointments = client.appointments.all().order_by("-date_time")[:10]
    return render(request, "clients/client_detail.html", {
        "client": client,
        "interactions": interactions,
        "appointments": appointments,
    })


@login_required
def client_edit(request, pk):
    """Edit a client."""
    client = get_object_or_404(Client, pk=pk, company=request.user.company)
    if request.method == "POST":
        form = ClientForm(request.POST, instance=client)
        if form.is_valid():
            form.save()
            messages.success(request, f"Cliente '{client.name}' atualizado com sucesso!")
            return redirect("clients:client_detail", pk=client.pk)
    else:
        form = ClientForm(instance=client)
    return render(request, "clients/client_form.html", {"form": form, "title": "Editar Cliente", "client": client})


@login_required
def client_delete(request, pk):
    """Delete a client."""
    client = get_object_or_404(Client, pk=pk, company=request.user.company)
    if request.method == "POST":
        name = client.name
        client.delete()
        messages.success(request, f"Cliente '{name}' excluído com sucesso!")
        return redirect("clients:client_list")
    return render(request, "clients/client_confirm_delete.html", {"client": client})


@login_required
def lead_list(request):
    """List all leads for the user's company."""
    company = request.user.company
    if not company:
        messages.error(request, "Você não está associado a nenhuma empresa.")
        return redirect("dashboard:index")

    query = request.GET.get("q", "")
    status_filter = request.GET.get("status", "")
    source_filter = request.GET.get("source", "")

    leads = Lead.objects.filter(company=company)
    if query:
        leads = leads.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(phone__icontains=query))
    if status_filter:
        leads = leads.filter(status=status_filter)
    if source_filter:
        leads = leads.filter(source=source_filter)

    return render(request, "clients/lead_list.html", {
        "leads": leads,
        "query": query,
        "status_filter": status_filter,
        "source_filter": source_filter,
        "status_choices": Lead.Status.choices,
        "source_choices": Lead.Source.choices,
    })


@login_required
def lead_create(request):
    """Create a new lead."""
    company = request.user.company
    if request.method == "POST":
        form = LeadForm(request.POST, company=company)
        if form.is_valid():
            lead = form.save(commit=False)
            lead.company = company
            lead.save()
            messages.success(request, f"Lead '{lead.name}' criado com sucesso!")
            return redirect("clients:lead_list")
    else:
        form = LeadForm(company=company)
    return render(request, "clients/lead_form.html", {"form": form, "title": "Novo Lead"})


@login_required
def lead_edit(request, pk):
    """Edit a lead."""
    lead = get_object_or_404(Lead, pk=pk, company=request.user.company)
    company = request.user.company
    if request.method == "POST":
        form = LeadForm(request.POST, instance=lead, company=company)
        if form.is_valid():
            form.save()
            messages.success(request, f"Lead '{lead.name}' atualizado com sucesso!")
            return redirect("clients:lead_list")
    else:
        form = LeadForm(instance=lead, company=company)
    return render(request, "clients/lead_form.html", {"form": form, "title": "Editar Lead", "lead": lead})


@login_required
def lead_delete(request, pk):
    """Delete a lead."""
    lead = get_object_or_404(Lead, pk=pk, company=request.user.company)
    if request.method == "POST":
        name = lead.name
        lead.delete()
        messages.success(request, f"Lead '{name}' excluído com sucesso!")
        return redirect("clients:lead_list")
    return render(request, "clients/lead_confirm_delete.html", {"lead": lead})


@login_required
def lead_convert(request, pk):
    """Convert a lead to a client."""
    lead = get_object_or_404(Lead, pk=pk, company=request.user.company)
    if request.method == "POST":
        client = lead.convert_to_client(user=request.user)
        messages.success(request, f"Lead '{lead.name}' convertido para cliente com sucesso!")
        return redirect("clients:client_detail", pk=client.pk)
    return render(request, "clients/lead_convert_confirm.html", {"lead": lead})
