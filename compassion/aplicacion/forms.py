from django import forms
from .models import Area


class BeneficiariosForm(forms.ModelForm):
    class Meta:
        model = Beneficiarios
        fields = ['nombre', 'apellido', 'fecha_nacimiento', 'genero', 'nivel', 'estado', 'observacion']


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['nombre_area', 'ubicacion', 'descripcion']


def crear_area(request):
    if request.method == 'POST':
        # Valida el formulario
        formulario = AreaForm(request.POST)
        if formulario.is_valid():
            # Procesa el formulario
            nueva_area = formulario.save()

            # Agrega un mensaje de éxito
            messages.success(request, 'Área creada con éxito.')

            return redirect('listar')

        # Muestra un mensaje de error
        messages.error(request, 'Error al crear el área.')

    return render(request, 'inventario/crear_area.html')
