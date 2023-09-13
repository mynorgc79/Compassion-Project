from .models import Familias, Beneficiarios
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Beneficiarios, Familias
from datetime import date
from datetime import datetime

# Create your views here.

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")',
)


def inicio(request):
    return render(request, 'index.html')

# AGREGAR BENEFICIARIO


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
        # La familia no existe
        return None


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


def calcular_edad(fecha_nacimiento):
    try:
        # Convierte la cadena de fecha de nacimiento en un objeto de fecha
        fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d')

        # Obtiene la fecha actual
        today = datetime.today()

        # Calcula la diferencia de años entre la fecha actual y la fecha de nacimiento
        edad = today.year - fecha_nacimiento.year - \
            ((today.month, today.day) < (fecha_nacimiento.month, fecha_nacimiento.day))

        return edad
    except ValueError:
        # Maneja el caso en el que la fecha de nacimiento no sea válida
        return None

# TERMINA AGREGAR BENEFICIARIO


def listar(request):
    return render(request, 'crud-beneficiarios/listar.html')


def actualizar(request):
    return render(request, 'crud-beneficiarios/actualizar.html')


def eliminar(request):
    return render(request, 'crud-beneficiarios/eliminar.html')


def buscar(request):
    return render(request, 'crud-beneficiarios/buscar.html')


def login(request):
    return render(request, 'login.html')


def registro_usuario(request):
    return render(request, 'usuarios/registro_user.html')


def editar_usuario(request):
    return render(request, 'usuarios/editar_user.html')


def buscar_familia(request):
    return render(request, 'familias/buscar_familia.html')


def ingresar_inventario(request):
    return render(request, 'inventario/ingresar_inventario.html')


def hello(request):
    return HttpResponse("holaMundo")
