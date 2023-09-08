from django.db import models

# Create your models here.


class Familias(models.Model):
    id_familia = models.AutoField(primary_key=True)
    apellido_familia = models.CharField(max_length=30, null=False)
    direccion = models.CharField(max_length=50, null=True)
    contacto = models.CharField(max_length=30, null=True)
    cantidad_hijos = models.IntegerField(null=True)

    class Meta:
        db_table = 'familias'
