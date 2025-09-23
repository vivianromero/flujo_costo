from django.urls import path
from .views import usuario_actual

urlpatterns = [
    path('usuario/', usuario_actual),
]


