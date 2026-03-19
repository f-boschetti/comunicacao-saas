"""Models for communications and interactions."""

from django.conf import settings
from django.db import models


class Interaction(models.Model):
    """Record of interactions with clients."""

    class Channel(models.TextChoices):
        WHATSAPP = "whatsapp", "WhatsApp"
        INSTAGRAM = "instagram", "Instagram"
        EMAIL = "email", "E-mail"
        PHONE = "phone", "Telefone"
        IN_PERSON = "in_person", "Presencial"
        SYSTEM = "system", "Sistema"

    class Direction(models.TextChoices):
        INBOUND = "inbound", "Recebida"
        OUTBOUND = "outbound", "Enviada"

    company = models.ForeignKey(
        "accounts.Company",
        on_delete=models.CASCADE,
        related_name="interactions",
        verbose_name="Empresa",
    )
    client = models.ForeignKey(
        "clients.Client",
        on_delete=models.CASCADE,
        related_name="interactions",
        verbose_name="Cliente",
    )
    channel = models.CharField(
        max_length=20,
        choices=Channel.choices,
        verbose_name="Canal",
    )
    direction = models.CharField(
        max_length=20,
        choices=Direction.choices,
        default=Direction.OUTBOUND,
        verbose_name="Direção",
    )
    subject = models.CharField(max_length=300, blank=True, verbose_name="Assunto")
    content = models.TextField(verbose_name="Conteúdo")
    is_automated = models.BooleanField(default=False, verbose_name="Automatizada")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="interactions",
        verbose_name="Criado por",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Interação"
        verbose_name_plural = "Interações"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.get_channel_display()} - {self.client.name} ({self.created_at:%d/%m/%Y})"


class MessageTemplate(models.Model):
    """Reusable message templates for automated communications."""

    class TemplateType(models.TextChoices):
        REMINDER = "reminder", "Lembrete"
        WELCOME = "welcome", "Boas-vindas"
        FOLLOW_UP = "follow_up", "Follow-up"
        CONFIRMATION = "confirmation", "Confirmação"
        CUSTOM = "custom", "Personalizado"

    company = models.ForeignKey(
        "accounts.Company",
        on_delete=models.CASCADE,
        related_name="message_templates",
        verbose_name="Empresa",
    )
    name = models.CharField(max_length=200, verbose_name="Nome do template")
    template_type = models.CharField(
        max_length=20,
        choices=TemplateType.choices,
        default=TemplateType.CUSTOM,
        verbose_name="Tipo",
    )
    subject = models.CharField(max_length=300, blank=True, verbose_name="Assunto")
    content = models.TextField(
        verbose_name="Conteúdo",
        help_text="Use {nome}, {empresa}, {data}, {hora} como variáveis.",
    )
    is_active = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Template de mensagem"
        verbose_name_plural = "Templates de mensagens"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_template_type_display()})"

    def render(self, context=None):
        """Render template with context variables."""
        text = self.content
        if context:
            for key, value in context.items():
                text = text.replace(f"{{{key}}}", str(value))
        return text
