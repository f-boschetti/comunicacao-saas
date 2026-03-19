"""Models for clients and leads management."""

from django.conf import settings
from django.db import models


class Client(models.Model):
    """Client model for managing business clients."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Ativo"
        INACTIVE = "inactive", "Inativo"
        BLOCKED = "blocked", "Bloqueado"

    company = models.ForeignKey(
        "accounts.Company",
        on_delete=models.CASCADE,
        related_name="clients",
        verbose_name="Empresa",
    )
    name = models.CharField(max_length=200, verbose_name="Nome completo")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    cpf = models.CharField(max_length=14, blank=True, verbose_name="CPF")
    date_of_birth = models.DateField(null=True, blank=True, verbose_name="Data de nascimento")
    address = models.TextField(blank=True, verbose_name="Endereço")
    notes = models.TextField(blank=True, verbose_name="Observações")
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        verbose_name="Status",
    )
    tags = models.CharField(max_length=500, blank=True, verbose_name="Tags", help_text="Tags separadas por vírgula")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_clients",
        verbose_name="Criado por",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        ordering = ["name"]

    def __str__(self):
        return self.name

    @property
    def tag_list(self):
        if self.tags:
            return [t.strip() for t in self.tags.split(",") if t.strip()]
        return []


class Lead(models.Model):
    """Lead model for managing potential clients."""

    class Source(models.TextChoices):
        WHATSAPP = "whatsapp", "WhatsApp"
        INSTAGRAM = "instagram", "Instagram"
        WEBSITE = "website", "Website"
        REFERRAL = "referral", "Indicação"
        OTHER = "other", "Outro"

    class Status(models.TextChoices):
        NEW = "new", "Novo"
        CONTACTED = "contacted", "Contactado"
        QUALIFIED = "qualified", "Qualificado"
        CONVERTED = "converted", "Convertido"
        LOST = "lost", "Perdido"

    company = models.ForeignKey(
        "accounts.Company",
        on_delete=models.CASCADE,
        related_name="leads",
        verbose_name="Empresa",
    )
    name = models.CharField(max_length=200, verbose_name="Nome")
    email = models.EmailField(blank=True, verbose_name="E-mail")
    phone = models.CharField(max_length=20, verbose_name="Telefone")
    source = models.CharField(
        max_length=20,
        choices=Source.choices,
        default=Source.OTHER,
        verbose_name="Origem",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Status",
    )
    notes = models.TextField(blank=True, verbose_name="Observações")
    converted_client = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="from_lead",
        verbose_name="Cliente convertido",
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_leads",
        verbose_name="Responsável",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Lead"
        verbose_name_plural = "Leads"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_status_display()})"

    def convert_to_client(self, user=None):
        """Convert this lead to a client."""
        client = Client.objects.create(
            company=self.company,
            name=self.name,
            email=self.email,
            phone=self.phone,
            notes=f"Convertido de lead. {self.notes}",
            created_by=user,
        )
        self.status = self.Status.CONVERTED
        self.converted_client = client
        self.save()
        return client
