from django.urls import re_path
from .consumers import QRLoginConsumer

websocket_urlpatterns = [
    re_path(r'ws/qr-login/$', QRLoginConsumer.as_asgi()),
]
