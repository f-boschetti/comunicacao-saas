"""Views for communications app."""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse

from .models import Interaction, MessageTemplate
from .forms import InteractionForm, MessageTemplateForm, SendMessageForm, AIResponseForm
from .services import send_email_message, send_whatsapp_message, send_instagram_message, generate_ai_response
from clients.models import Client


@login_required
def interaction_list(request):
    """List all interactions."""
    company = request.user.company
    if not company:
        return redirect("dashboard:index")

    interactions = Interaction.objects.filter(company=company).select_related("client", "created_by")
    channel_filter = request.GET.get("channel", "")
    if channel_filter:
        interactions = interactions.filter(channel=channel_filter)

    return render(request, "communications/interaction_list.html", {
        "interactions": interactions[:100],
        "channel_filter": channel_filter,
        "channel_choices": Interaction.Channel.choices,
    })


@login_required
def interaction_create(request):
    """Log a new interaction."""
    company = request.user.company
    if request.method == "POST":
        form = InteractionForm(request.POST, company=company)
        if form.is_valid():
            interaction = form.save(commit=False)
            interaction.company = company
            interaction.created_by = request.user
            interaction.save()
            messages.success(request, "Interação registrada com sucesso!")
            return redirect("communications:interaction_list")
    else:
        form = InteractionForm(company=company)
    return render(request, "communications/interaction_form.html", {"form": form, "title": "Registrar Interação"})


@login_required
def send_message(request, client_id):
    """Send a message to a client."""
    company = request.user.company
    client = get_object_or_404(Client, pk=client_id, company=company)

    if request.method == "POST":
        form = SendMessageForm(request.POST, company=company)
        if form.is_valid():
            channel = form.cleaned_data["channel"]
            subject = form.cleaned_data["subject"]
            message_text = form.cleaned_data["message"]
            success = False

            if channel == "email" and client.email:
                success = send_email_message(client.email, subject, message_text)
            elif channel == "whatsapp" and client.phone:
                success = send_whatsapp_message(client.phone, message_text)
            elif channel == "instagram":
                success = send_instagram_message(str(client.pk), message_text)

            Interaction.objects.create(
                company=company,
                client=client,
                channel=channel,
                direction="outbound",
                subject=subject,
                content=message_text,
                created_by=request.user,
            )

            if success:
                messages.success(request, f"Mensagem enviada para {client.name}!")
            else:
                messages.warning(request, f"Mensagem registrada, mas o envio via {channel} não está configurado.")
            return redirect("clients:client_detail", pk=client.pk)
    else:
        form = SendMessageForm(company=company, initial={"client": client.pk})

    return render(request, "communications/send_message.html", {
        "form": form, "client": client,
    })


@login_required
def template_list(request):
    """List message templates."""
    company = request.user.company
    if not company:
        return redirect("dashboard:index")
    templates = MessageTemplate.objects.filter(company=company)
    return render(request, "communications/template_list.html", {"templates": templates})


@login_required
def template_create(request):
    """Create a message template."""
    company = request.user.company
    if request.method == "POST":
        form = MessageTemplateForm(request.POST)
        if form.is_valid():
            template = form.save(commit=False)
            template.company = company
            template.save()
            messages.success(request, f"Template '{template.name}' criado com sucesso!")
            return redirect("communications:template_list")
    else:
        form = MessageTemplateForm()
    return render(request, "communications/template_form.html", {"form": form, "title": "Novo Template"})


@login_required
def template_edit(request, pk):
    """Edit a message template."""
    template = get_object_or_404(MessageTemplate, pk=pk, company=request.user.company)
    if request.method == "POST":
        form = MessageTemplateForm(request.POST, instance=template)
        if form.is_valid():
            form.save()
            messages.success(request, f"Template '{template.name}' atualizado!")
            return redirect("communications:template_list")
    else:
        form = MessageTemplateForm(instance=template)
    return render(request, "communications/template_form.html", {"form": form, "title": "Editar Template"})


@login_required
def template_delete(request, pk):
    """Delete a message template."""
    template = get_object_or_404(MessageTemplate, pk=pk, company=request.user.company)
    if request.method == "POST":
        template.delete()
        messages.success(request, "Template excluído!")
        return redirect("communications:template_list")
    return render(request, "communications/template_confirm_delete.html", {"template": template})


@login_required
def ai_response(request):
    """Generate an AI-powered response."""
    response_text = None
    if request.method == "POST":
        form = AIResponseForm(request.POST)
        if form.is_valid():
            prompt = form.cleaned_data["prompt"]
            context = form.cleaned_data.get("context", "")
            response_text = generate_ai_response(prompt, context)
    else:
        form = AIResponseForm()
    return render(request, "communications/ai_response.html", {
        "form": form, "response_text": response_text,
    })


@login_required
def ai_response_api(request):
    """API endpoint for AI response generation."""
    if request.method == "POST":
        prompt = request.POST.get("prompt", "")
        context = request.POST.get("context", "")
        if prompt:
            response_text = generate_ai_response(prompt, context)
            return JsonResponse({"response": response_text})
    return JsonResponse({"error": "Invalid request"}, status=400)
