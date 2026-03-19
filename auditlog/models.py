"""Models for audit logging."""

from django.conf import settings
from django.db import models


class AuditLog(models.Model):
    """Audit log entry for tracking user actions."""

    class Action(models.TextChoices):
        CREATE = "create", "Criação"
        UPDATE = "update", "Atualização"
        DELETE = "delete", "Exclusão"
        LOGIN = "login", "Login"
        LOGOUT = "logout", "Logout"
        VIEW = "view", "Visualização"
        EXPORT = "export", "Exportação"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
        verbose_name="Usuário",
    )
    action = models.CharField(max_length=20, choices=Action.choices, verbose_name="Ação")
    model_name = models.CharField(max_length=100, verbose_name="Modelo")
    object_id = models.CharField(max_length=100, blank=True, verbose_name="ID do objeto")
    object_repr = models.CharField(max_length=300, blank=True, verbose_name="Representação")
    changes = models.JSONField(default=dict, blank=True, verbose_name="Alterações")
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="Endereço IP")
    user_agent = models.TextField(blank=True, verbose_name="User Agent")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Data/hora")

    class Meta:
        verbose_name = "Log de auditoria"
        verbose_name_plural = "Logs de auditoria"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.get_action_display()} - {self.model_name} - {self.user} ({self.timestamp:%d/%m/%Y %H:%M})"

    @classmethod
    def log(cls, user, action, model_name, object_id="", object_repr="", changes=None, request=None):
        """Create an audit log entry."""
        ip_address = None
        user_agent = ""
        if request:
            ip_address = cls._get_client_ip(request)
            user_agent = request.META.get("HTTP_USER_AGENT", "")

        return cls.objects.create(
            user=user,
            action=action,
            model_name=model_name,
            object_id=str(object_id),
            object_repr=str(object_repr)[:300],
            changes=changes or {},
            ip_address=ip_address,
            user_agent=user_agent,
        )

    @staticmethod
    def _get_client_ip(request):
        """Extract client IP from request."""
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")
