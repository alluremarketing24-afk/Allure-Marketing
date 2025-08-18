from __future__ import absolute_import, unicode_literals

# Import the Celery application so it's available on project import
from .celery import app as celery_app

__all__ = ('celery_app',)

