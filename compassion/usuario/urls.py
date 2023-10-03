from django.contrib import admin
from django.urls import path
from django import views
from .import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
 
  #  path('inicio', views.inicio, name='inicio'),# Agrega la barra diagonal al final
]
