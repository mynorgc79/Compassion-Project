from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Familias(models.Model):
    id_familia = models.AutoField(primary_key=True)
    apellido_familia = models.CharField(
        max_length=50, null=False, verbose_name='apellido Familia')
    direccion = models.CharField(
        max_length=50, null=True, verbose_name='direccion')
    contacto = models.CharField(
        max_length=30, null=True, verbose_name='contacto')
    cantidad_hijos = models.IntegerField(
        null=True, verbose_name='cantidad Hijos')

    def __str__(self):
        return f'Familia {self.apellido_familia}'


class Beneficiarios(models.Model):
    codigo_beneficiario = models.IntegerField(
        primary_key=True, verbose_name='Codigo')
    nombre = models.CharField(max_length=25, null=False, verbose_name='Nombre')
    apellido = models.CharField(
        max_length=25, null=False, verbose_name='Apellido')
    fecha_nacimiento = models.DateField(
        null=False, verbose_name='Fecha de nacimiento')
    edad = models.IntegerField(null=False, verbose_name='E   dad')
    genero = models.CharField(max_length=25, null=False, verbose_name='Genero')
    nivel = models.IntegerField(null=False, verbose_name='Nivel')
    observacion = models.CharField(
        max_length=100, null=True, verbose_name='observacion')
    id_familia = models.ForeignKey(Familias, on_delete=models.CASCADE)

    def __str__(self):
        return f'Beneficiario {self.codigo_beneficiario}'


class salidas(models.Model):
    id_salidas = models.AutoField(primary_key=True)
    tipo_salida = models.CharField(
        max_length=20, verbose_name='Tipo de Salida')
    fecha_salida = models.DateField(
        null=False, verbose_name='Fecha de salida')
    motivo = models.CharField(
        max_length=60, null='true', verbose_name='Motivo')
    estado = models.BooleanField(default='True', verbose_name='Estado')
    codigo_beneficiario = models.ForeignKey(
        Beneficiarios, on_delete=models.CASCADE)

    def __str__(self):
        return f'Salida {self.id_salidas}'
