from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import UserManager
# Create your models here.

# -----------f, username):-DEFINIENDO MODELO FAMILIAS


class Familias(models.Model):
    id_familia = models.AutoField(primary_key=True)
    apellido_familia = models.CharField(
        max_length=50, null=False, verbose_name='apellido_familia')
    direccion = models.CharField(
        max_length=50, null=True, verbose_name='direccion')
    contacto = models.CharField(
        max_length=30, null=True, verbose_name='contacto')
    nombre_padre = models.CharField(
        max_length=40, null=True, verbose_name='nombre_padre')
    nombre_madre = models.CharField(
        max_length=40, null=True, verbose_name='nombre_madre')

    def __str__(self):
        return f'Familia {self.apellido_familia}'


class Beneficiarios(models.Model):
    codigo_beneficiario = models.IntegerField(
        primary_key=True, verbose_name='codigo')
    nombre = models.CharField(max_length=40, null=False, verbose_name='nombre')
    apellido = models.CharField(
        max_length=40, null=False, verbose_name='apellido')
    fecha_nacimiento = models.DateField(
        null=False, verbose_name='fecha_nacimiento')
    edad = models.IntegerField(null=True, verbose_name='edad')
    genero = models.CharField(max_length=25, null=False, verbose_name='genero')
    nivel = models.IntegerField(null=False, verbose_name='nivel')
    observacion = models.CharField(
        max_length=150, null=True, verbose_name='observacion')
    estado = models.BooleanField(default='True', verbose_name='estado')
    id_familia = models.ForeignKey(Familias, on_delete=models.CASCADE)

    def __str__(self):
        return f'Beneficiario {self.codigo_beneficiario}'


class Salidas(models.Model):
    id_salidas = models.AutoField(primary_key=True)
    tipo_salida = models.CharField(
        max_length=20, verbose_name='Tipo de Salida')
    fecha_salida = models.DateField(
        null=False, verbose_name='Fecha de salida')
    motivo = models.CharField(
        max_length=60, null='true', verbose_name='Motivo')
    codigo_beneficiario = models.ForeignKey(
        Beneficiarios, on_delete=models.CASCADE)

    def __str__(self):
        return f'Salida {self.id_salidas}'


class Area(models.Model):
    id_area = models.AutoField(primary_key=True)
    nombre_area = models.CharField(max_length=75)
    ubicacion = models.CharField(max_length=60)
    descripcion = models.TextField(blank=True, null=True)


class ItemInventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    cantidad = models.PositiveIntegerField()
    descripcion_articulo = models.TextField()
    fecha_compra = models.DateField()
    donacion = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True)
    numero_cheque = models.CharField(max_length=50, blank=True, null=True)
    numero_factura = models.CharField(max_length=50, blank=True, null=True)
    proveedor = models.CharField(max_length=75)
    encargado = models.CharField(max_length=100)
    valor_compra = models.DecimalField(max_digits=10, decimal_places=2)
    numero_acta = models.CharField(max_length=20, blank=True, null=True)
    estado = models.BooleanField(default='True', verbose_name='estado')
    auditado = models.BooleanField(default=False)
    area_id = models.ForeignKey(Area, on_delete=models.CASCADE)


class Movimientos(models.Model):
    id_movimiento = models.AutoField(primary_key=True)
    tipo_movimiento = models.CharField(
        max_length=20, verbose_name='Tipo de Salida')
    fecha_movimiento = models.DateField(
        null=False, verbose_name='Fecha de salida')
    descripcion = models.TextField()
    inventario_id = models.ForeignKey(
        ItemInventario, on_delete=models.CASCADE)

# ----------------------MODELOS PARA EL INVENTARIO
