from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.


class UsuarioManager(BaseUserManager):
    def create_user(self, username, email, nombres, apellidos, password=None):
        if not email:
            raise ValueError('El usuario debe tener correo electrónico')
        usuario = self.model(
            username=username,
            email=self.normalize_email(email),
            nombres=nombres,
            apelllidos=apellidos
        )

# -----ENCRIPTA LA CONTRASEÑA CON LOS METODOS DE DJANGO
        usuario.set_password(password)
        usuario.save()
        return usuario

# -------creamos al superusuario
    def create_superuser(self, username, email, nombres, apellidos, password):
        usuario = self.create_user(
            email,
            username=username,
            nombres=nombres,
            apelllidos=apellidos
        )
        usuario.usuario_administrador = True
        usuario.save()


# ------------DEFINIENDO MODELO USUARIO
class Usuario(AbstractBaseUser):
    username = models.CharField(
        'Nombre de usuario', unique=True, max_length=80)
    email = models.EmailField(
        'correo Electrónico', unique=True, max_length=200)
    nombres = models.CharField(
        'nombres', blank=True, null=True, max_length=100)
    apellidos = models.CharField(
        'Apellidos', blank=True, null=True, max_length=100)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    objects = UsuarioManager

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'nombres', 'apellidos']

    def __str__(self):
        return f'{self.nomrbres}, {self.apellidost}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador


# ------------DEFINIENDO MODELO FAMILIAS
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
