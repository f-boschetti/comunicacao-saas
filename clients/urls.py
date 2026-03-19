"""URL patterns for clients app."""

from django.urls import path
from . import views

app_name = "clients"

urlpatterns = [
    path("", views.client_list, name="client_list"),
    path("create/", views.client_create, name="client_create"),
    path("<int:pk>/", views.client_detail, name="client_detail"),
    path("<int:pk>/edit/", views.client_edit, name="client_edit"),
    path("<int:pk>/delete/", views.client_delete, name="client_delete"),
    path("leads/", views.lead_list, name="lead_list"),
    path("leads/create/", views.lead_create, name="lead_create"),
    path("leads/<int:pk>/edit/", views.lead_edit, name="lead_edit"),
    path("leads/<int:pk>/delete/", views.lead_delete, name="lead_delete"),
    path("leads/<int:pk>/convert/", views.lead_convert, name="lead_convert"),
]
