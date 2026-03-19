"""Celery configuration for comunicacao-saas project."""

import os
from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("comunicacao_saas")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
