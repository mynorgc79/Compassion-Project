from django.contrib import admin
from django.urls import path
from django import views
from .import views
from usuario.models import Usuario


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views._logout, name='logout'),
    path('registro_usuario', views.registrar_usuario, name='registro_usuario'),
    path('editar_usuario', views.editar_usuario, name='editar_usuario'),
    path('actualizar_usuario/', views.actualizar_usuario, name='actualizar_usuario'),
    
]

  #  path('inicio', views.inicio, name='inicio'),# Agrega la barra diagonal al final

