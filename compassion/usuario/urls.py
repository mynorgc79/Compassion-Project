from django.contrib import admin
from django.urls import path
from django import views
from .import views
from usuario.models import Usuario
from usuario.views import ResetPasswordView


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views._logout, name='logout'),
    path('registro_usuario', views.registrar_usuario, name='registro_usuario'),
    path('editar_usuario', views.editar_usuario, name='editar_usuario'),
    path('actualizar_usuario/', views.actualizar_usuario, name='actualizar_usuario'),
    path('cambiar_contrasena/', views.cambiar_contrasena, name='cambiar_contrasena'),
    path('password_reset/', ResetPasswordView.as_view(), name='password_reset'),
    #path('password_reset/', views.ResetPasswordView,  name='password_resetr'),
]

  #  path('inicio', views.inicio, name='inicio'),# Agrega la barra diagonal al final

