from django import forms


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
