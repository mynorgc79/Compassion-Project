from .models import Familias, Beneficiarios
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Beneficiarios, Familias, Salidas
from datetime import date
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Count
from django.db import models
from django.db.models import Q
# Create your views here.

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")',
)


def inicio(request):
    return render(request, 'index.html')

# AGREGAR BENEFICIARIO


def calcular_edad(fecha_nacimiento):
    try:
        # Convierte la cadena de fecha de nacimiento al formato ISO 8601
        fecha_iso = datetime.strptime(
            fecha_nacimiento, '%Y-%m-%d').strftime('%Y-%m-%d')

        # Obtiene la fecha actual en formato ISO 8601
        today = datetime.today().strftime('%Y-%m-%d')

        # Calcula la diferencia de años entre la fecha actual y la fecha de nacimiento
        edad = int(today[:4]) - int(fecha_iso[:4]) - \
            (today[5:] < fecha_iso[5:])

        return edad
    except ValueError:
        # Maneja el caso en el que la fecha de nacimiento no sea válida
        return None


def validar_familia(request):
    apellido_padre = request.POST.get('apellido_padre')
    apellido_madre = request.POST.get('apellido_madre')
    nombre_padre = request.POST.get('nombre_padre')
    nombre_madre = request.POST.get('nombre_madre')
    direccion = request.POST.get('direccion')
    contacto = request.POST.get('contacto')
    apellido_familia = f"{apellido_padre} {apellido_madre}"

    # Verificar si existe una familia con los apellidos y nombres especificados
    familia = Familias.objects.filter(
        apellido_familia__iexact=apellido_familia,
        nombre_padre__iexact=nombre_padre,
        nombre_madre__iexact=nombre_madre
    )

    if familia.exists():
        # La familia existe, devuelve su ID
        return familia.first().id_familia
    else:
        # La familia no existe, crea una nueva familia y luego devuelve su ID
        nueva_familia = Familias(
            apellido_familia=apellido_familia,
            nombre_padre=nombre_padre,
            nombre_madre=nombre_madre,
            direccion=direccion,
            contacto=contacto
        )
        nueva_familia.save()
        return nueva_familia.id_familia


def agregar(request):
    if request.method == 'POST':
        # Obtener datos del formulario
        # ---------OBTENIENDO DATOS DE FAMILIARES
        nombre_padre = request.POST.get('nombre_padre')
        nombre_madre = request.POST.get('nombre_madre')
        apellido_padre = request.POST.get('apellido_padre')
        apellido_madre = request.POST.get('apellido_madre')
        direccion = request.POST.get('direccion')
        contacto = request.POST.get('contacto')
        apellido_familia = f"{apellido_padre} {apellido_madre}"

        # ---------OBTENIENDO DATOS DEL BENEFICIARIO
        codigo_beneficiario = request.POST.get('codigo')
        nombre_beneficiario = request.POST.get('nombre_beneficiario')
        apellido_beneficiario = request.POST.get('apellido_beneficiario')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        genero = request.POST.get('genero')
        nivel = request.POST.get('nivel')
        observacion = request.POST.get('observacion')

        # Obtener el ID de la familia
        familia_id = validar_familia(request)

        # Asignar el ID de la familia al beneficiario
        beneficiario = Beneficiarios(
            codigo_beneficiario=codigo_beneficiario,
            nombre=nombre_beneficiario,
            apellido=apellido_beneficiario,
            fecha_nacimiento=fecha_nacimiento,
            genero=genero,
            nivel=nivel,
            observacion=observacion,
            edad=calcular_edad(fecha_nacimiento),
            estado=True,
            id_familia_id=familia_id
        )

        # Guardar el beneficiario en la base de datos
        beneficiario.save()

        # Redirigir a la lista de beneficiarios u otra vista apropiada
        return redirect('listar')
    else:
        return render(request, 'crud-beneficiarios/agregar.html')


# TERMINA AGREGAR BENEFICIARIO


def listar(request):
    beneficiarios = Beneficiarios.objects.all()
    datos = {'beneficiarios': beneficiarios}
    return render(request, 'crud-beneficiarios/listar.html', datos)


def actualizar(request):
    beneficiarios = Beneficiarios.objects.all()
    datos = {'beneficiarios': beneficiarios}
    return render(request, 'crud-beneficiarios/actualizar.html', datos)


def eliminar(request):
    return render(request, 'crud-beneficiarios/eliminar.html')


def buscar(request):
    return render(request, 'crud-beneficiarios/buscar.html')

# --------Salida Beneficiarios


def salida_beneficiario(request):
    if request.method == 'POST':
        codigo_beneficiario = request.POST.get('codigo_beneficiario')
        fecha_salida = request.POST.get('fecha_salida')
        tipo_salida = request.POST.get('tipo_salida')
        motivo = request.POST.get('motivo')

        try:
            beneficiario = Beneficiarios.objects.get(
                codigo_beneficiario=codigo_beneficiario)
        except Beneficiarios.DoesNotExist:
            beneficiario = None

        if beneficiario:
            beneficiario.estado = 0  # Cambia el estado del beneficiario a inactivo
            beneficiario.save()

            salida = Salidas(
                codigo_beneficiario=beneficiario,
                fecha_salida=fecha_salida,
                tipo_salida=tipo_salida,
                motivo=motivo
            )
            salida.save()

            # Redirige a donde desees después de registrar la salida
            return redirect('listar')
        else:
            # Maneja adecuadamente el caso en el que el beneficiario no existe
            return render(request, 'crud-beneficiarios/salida_beneficiario.html')

    beneficiarios = Beneficiarios.objects.all()
    datos = {'beneficiarios': beneficiarios}
    return render(request, 'crud-beneficiarios/salida_beneficiario.html', datos)


# --------fin salida beneficiario
def ingresar_inventario(request):
    return render(request, 'inventario/ingresar_inventario.html')


def login(request):
    return render(request, 'login.html')

# REGISTRO DE USUARIO


def registro_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            messages.success(request, f'Usuario {username} creado')
            return redirect('login')

    else:
        form = UserCreationForm()
    context = {'form': form}
    return render(request, 'usuarios/registro_user.html')

# END REGISTRAR USUARIO


def editar_usuario(request):
    return render(request, 'usuarios/editar_user.html')


def listar_familias(request):
    # Obtener el apellido de la solicitud GET
    apellido = request.GET.get('apellido', '')

    # Filtrar familias por apellido
    familias = Familias.objects.annotate(
        cantidad_beneficiarios=Count(
            'beneficiarios', filter=Q(beneficiarios__estado=True))
    ).filter(apellido_familia__icontains=apellido, cantidad_beneficiarios__gt=0)

    datos = {'familias': familias}
    return render(request, 'familias/listar_familias.html', datos)


def ingresar_inventario(request):
    return render(request, 'inventario/ingresar_inventario.html')
