from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path(r'homepage', views.index, name='homepage'),
    path(r'Map', views.Map, name='Map'),
    path(r'associate', views.associate, name='associate'),
    path(r'pathPlanning', views.pathPlanning, name='pathPlanning'),
]