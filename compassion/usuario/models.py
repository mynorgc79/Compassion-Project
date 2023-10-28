from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager



# Create your models here.


class UsuarioManager(BaseUserManager):
    def create_user(self,  username, nombres, apellidos, password=None,rol=None):
        if not username:
             raise ValueError('Debe tener un nombre de usuario')

        usuario = self.model(
            username=username,
            # email=self.normalize_email(email),
            nombres=nombres,
            apellidos=apellidos,
            rol=rol
        )

        # Encripta la contraseña correctamente
        usuario.set_password(password)
        usuario.save()
        return usuario

    def create_superuser(self, username, nombres, apellidos, password):
        usuario = self.create_user(
            # email,
            username=username,
            nombres=nombres,
            apellidos=apellidos,
            password=password  # Añade la contraseña aquí
        )
        usuario.usuario_administrador = True
        usuario.save()


class Usuario(AbstractBaseUser):
    username = models.CharField(
        'Nombre de usuario', unique=True, max_length=80)
    
    nombres = models.CharField(
        'nombres', blank=True, null=True, max_length=100)
    apellidos = models.CharField(
        'Apellidos', blank=True, null=True, max_length=100)
    usuario_activo = models.BooleanField(default=True)
    usuario_administrador = models.BooleanField(default=False)
    rol = models.CharField(
        'rol', blank=True, null=True, max_length=100)
    objects = UsuarioManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['nombres', 'apellidos']

    def get_full_name(self):
        # Devuelve el nombre completo del usuario
        return f'{self.nombres} {self.apellidos}'

    def __str__(self):
        return f'{self.nombres}, {self.apellidos}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.usuario_administrador
