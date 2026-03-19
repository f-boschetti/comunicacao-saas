"""URL patterns for communications app."""

from django.urls import path
from . import views

app_name = "communications"

urlpatterns = [
    path("interactions/", views.interaction_list, name="interaction_list"),
    path("interactions/create/", views.interaction_create, name="interaction_create"),
    path("send/<int:client_id>/", views.send_message, name="send_message"),
    path("templates/", views.template_list, name="template_list"),
    path("templates/create/", views.template_create, name="template_create"),
    path("templates/<int:pk>/edit/", views.template_edit, name="template_edit"),
    path("templates/<int:pk>/delete/", views.template_delete, name="template_delete"),
    path("ai/", views.ai_response, name="ai_response"),
    path("ai/api/", views.ai_response_api, name="ai_response_api"),
]
