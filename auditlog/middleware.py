"""Audit logging middleware."""

from .models import AuditLog


class AuditLogMiddleware:
    """Middleware to automatically log certain user actions."""

    TRACKED_METHODS = ("POST", "PUT", "PATCH", "DELETE")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if (
            request.method in self.TRACKED_METHODS
            and hasattr(request, "user")
            and request.user.is_authenticated
            and response.status_code in (200, 201, 302)
        ):
            path = request.path
            action = self._determine_action(request.method, path)
            if action:
                model_name = self._extract_model_name(path)
                AuditLog.log(
                    user=request.user,
                    action=action,
                    model_name=model_name,
                    object_repr=f"{request.method} {path}",
                    request=request,
                )

        return response

    def _determine_action(self, method, path):
        """Determine the action type based on HTTP method and path."""
        if "/delete" in path:
            return "delete"
        if "/create" in path or "/register" in path:
            return "create"
        if method in ("PUT", "PATCH") or "/edit" in path:
            return "update"
        if method == "POST":
            return "create"
        return None

    def _extract_model_name(self, path):
        """Extract a model name from the URL path."""
        parts = [p for p in path.strip("/").split("/") if p and not p.isdigit()]
        if parts:
            return parts[-1] if len(parts) == 1 else parts[0]
        return "unknown"
