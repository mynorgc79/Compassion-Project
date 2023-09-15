from django.contrib import admin
from django.urls import path
from django import views
from .import views


# importamos desde views
urlpatterns = [
    path('', views.inicio, name='index'),
    path('inicio', views.inicio, name='inicio'),
    path('agregar', views.agregar, name='agregar'),
    path('listar', views.listar, name='listar'),
    path('actualizar', views.actualizar, name='actualizar'),
    path('eliminar', views.eliminar, name='eliminar'),
    path('buscar', views.buscar, name='buscar'),
    path('login', views.login, name='login'),
    path('registro_usuario', views.registro_usuario, name='registro_usuario'),
    path('editar_usuario', views.editar_usuario, name='editar_usuario'),

    path('listar_familias', views.listar_familias, name='listar_familias'),
    path('ingresar_inventario', views.ingresar_inventario,
         name='ingresar_inventario'),

    path('salida_beneficiario', views.salida_beneficiario,
         name='salida_beneficiario'),



]
