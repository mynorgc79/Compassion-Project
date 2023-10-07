from django import forms
from .models import Area





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


class BeneficiarioForm(forms.Form):
    codigo = forms.IntegerField(label='Código', required=True)
    nombre_beneficiario = forms.CharField(label='Nombres', required=True)
    apellido_beneficiario = forms.CharField(label='Apellidos', required=True)
    fecha_nacimiento = forms.DateField(label='Fecha de Nacimiento', required=True)
    genero = forms.ChoiceField(
        label='Género',
        required=True,
        choices=(('femenino', 'Femenino'), ('masculino', 'Masculino')),
    )
    nivel = forms.ChoiceField(
        label='Nivel',
        required=True,
        choices=(('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')),
    )
    observacion = forms.CharField(label='Observación', required=True)