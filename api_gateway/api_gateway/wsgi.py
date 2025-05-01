"""
WSGI config for api_gateway project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'api_gateway.settings')

application = get_wsgi_application()
