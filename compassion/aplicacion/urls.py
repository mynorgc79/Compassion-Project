from django.contrib import admin
from django.urls import path
from django import views
from .import views

# importamos desde views
urlpatterns = [
    path('', views.index, name='index'),
    path('agregar', views.agregar, name='agregar'),
    path('listar', views.listar, name='listar'),
    path('actualizar', views.actualizar, name='actualizar'),
    path('eliminar', views.eliminar, name='eliminar'),
    path('buscar', views.buscar, name='buscar'),


    # path('nosotros', views.nosotros, name='nosotros'),
    # path('beneficiarios', views.beneficiarios, name='beneficiarios'),
    # path('beneficiarios/crear', views.crearBeneficiario,
    #    name='crearBeneficiario'),
    # path('beneficiarios/editar', views.editarBeneficiario,
    #    name='editarBeneficiario'),



]
