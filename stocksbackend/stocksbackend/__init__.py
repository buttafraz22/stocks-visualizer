# stocksbackend/__init.py__

from .celery import app as celery_app

__all__ = ("celery_app",)