# endpoints/urls.py
from django.conf import settings
from django.urls import path

from endpoints.controllers.base import endpoints, aendpoints

if hasattr(settings, 'ASGI_APPLICATION') and settings.ASGI_APPLICATION is None:
    urlpatterns = [path('', endpoints, name='endpoints'), ]
else:
    urlpatterns = [path('', aendpoints, name='endpoints'), ]
