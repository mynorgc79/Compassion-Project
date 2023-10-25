from django.contrib import admin
from django.urls import path
from django import views
from .import views
from django.contrib.auth.decorators import login_required



# importamos desde views
urlpatterns = [

     path('inicio', views.inicio, name="inicio"),
     path('', views.vista_raiz,name="vista_raiz"),
     
#    path('login/', views.login, name='login'),
 #   path('registro_usuario', views.registro_usuario, name='registro_usuario'),
    #path('index/', views.index, name='index'),

   path('verificar_codigo_existente', views.verificar_codigo_existente, name='verificar_codigo_existente'),
  # path('verificar_codigo/', views.verificar_codigo, name='verificar_codigo'), 
   path('agregar', views.agregar, name='agregar'),
   path('agregar_existente', views.agregar_existente, name='agregar_existente'),
   path('listar', views.listar, name='listar'),

    path('editar_usuario/<int:codigo_beneficiario>/', views.actualizar_beneficiario, name='editar_usuario'),
#path('actualizar/<int:codigo_beneficiario>/', views.actualizar_beneficiario, name='actualizar_beneficiario'),
    path('salida_beneficiario', views.salida_beneficiario,
         name='salida_beneficiario'),

    path('beneficiarios_retirados', views.beneficiarios_retirados,
         name='beneficiarios_retirados'),

    path('listar_familias', views.listar_familias, name='listar_familias'),

   # path('editar_usuario', views.editar_usuario, name='editar_usuario'),


    path('registrar_articulo', views.registrar_articulo, name='registrar_articulo'),
    path('crear_area', views.crear_area, name='crear_area'),
    path('listar_articulos', views.listar_articulos, name='listar_articulos'),
    path('buscar_area', views.buscar_area, name='buscar_area'),
    path('editar_articulo', views.editar_articulo, name='editar_articulo'),
    path('listar_bajas', views.listar_bajas, name='listar_bajas'),
    path('baja_articulo', views.baja_articulo, name='baja_articulo'),

    path('exportar_pdf/', views.exportar_pdf, name='exportar_pdf'),


]
