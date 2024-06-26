# resolver/routing.py
from django.urls import re_path
from .consumers import ResolverConsumer

websocket_urlpatterns = [
    re_path(r'ws/resolver/$', ResolverConsumer.as_asgi()),
]
