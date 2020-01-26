from __future__ import absolute_import, unicode_literals
from .celery import app as celery_app
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
__all__ = ('celery_app',)
