# chat/routing.py
from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^trafficSituation/', consumers.DriverConsumer.as_asgi()),
]