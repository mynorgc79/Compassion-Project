from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")',
)


def index(request):
    return render(request, 'index.html')


def agregar(request):
    return render(request, 'crud-beneficiarios/agregar.html')


def listar(request):
    return render(request, 'crud-beneficiarios/listar.html')


def actualizar(request):
    return render(request, 'crud-beneficiarios/actualizar.html')


def eliminar(request):
    return render(request, 'crud-beneficiarios/eliminar.html')


def buscar(request):
    return render(request, 'crud-beneficiarios/buscar.html')
