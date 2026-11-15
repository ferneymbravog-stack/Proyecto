from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('fuentes/', views.fuentes, name='fuentes'),
    path('buscar/', views.buscar, name='buscar'),
]
