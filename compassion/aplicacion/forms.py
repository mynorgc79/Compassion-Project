from django import forms
from .models import Area


class BeneficiarioForm(forms.Form):
    nombre_padre = forms.CharField(max_length=100, required=True)
    apellido_padre = forms.CharField(max_length=100, required=True)
    nombre_madre = forms.CharField(max_length=100, required=True)
    apellido_madre = forms.CharField(max_length=100, required=True)
    direccion = forms.CharField(max_length=200, required=True)
    contacto = forms.CharField(max_length=20, required=True)
    codigo = forms.IntegerField(required=True)
    nombre_beneficiario = forms.CharField(max_length=100, required=True)
    apellido_beneficiario = forms.CharField(max_length=100, required=True)
    fecha_nacimiento = forms.DateField(required=True)
    genero = forms.ChoiceField(
        choices=[('femenino', 'Femenino'), ('masculino', 'Masculino')], required=True)
    nivel = forms.IntegerField(required=True)
    observacion = forms.CharField(max_length=200, required=True)


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
