"""
ASGI config for Whatsapp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/asgi/
"""

import os
import django
from channels.routing import get_default_application
from .routing import application


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Bulk.settings")
django.setup()
application = get_default_application()
