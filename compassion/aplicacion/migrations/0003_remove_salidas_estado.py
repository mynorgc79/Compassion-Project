# Generated by Django 4.1.7 on 2023-09-15 19:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aplicacion', '0002_remove_familias_cantidad_hijos_beneficiarios_estado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salidas',
            name='estado',
        ),
    ]