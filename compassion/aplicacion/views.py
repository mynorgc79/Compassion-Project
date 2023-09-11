from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Beneficiarios

# Create your views here.

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")',
)


def inicio(request):
    return render(request, 'index.html')


def agregar(request):
    if request.method == 'POST':
        # agrego los datos
        if request.POST.get('codigo') and request.POST.get('nombre') and request.POST.get('apellido') and request.POST.get('nivel') and request.POST.get('fecha_nacimiento') and request.POST.get('genero') and request.POST.get('observacion') and request.POST.get('id_familia'):
            if request.POST.get('id_familia') and Beneficiarios.objects.filter(
                    id_familia=request.POST.get('id_familia')).exists():
                beneficiario = Beneficiarios()
                # insertando valores obtenidos a los modelos
                beneficiario.codigo = request.POST.get('codigo')
                beneficiario.nombre = request.POST.get('nombre')
                beneficiario.apellido = request.POST.get('apellido')
                beneficiario.nivel = request.POST.get('nivel')
                beneficiario.fecha_nacimiento = request.POST.get(
                    'fecha_nacimiento')
                beneficiario.genero = request.POST.get('genero')
                beneficiario.observacion = request.POST.get('observacion')
                beneficiario.id_familia = request.POST.get('id_familia')
                beneficiario.save()

                # Despues de ingresar los datos nos redirecciona a la lista de usuarios
                return redirect('listar')
            else:
                return render(request, 'crud-beneficiarios/agregar.html', {
                    'error': 'El ID de la familia no es valido.'
                })
    else:
        return render(request, 'crud-beneficiarios/agregar.html')


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
