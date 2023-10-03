from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.pagesizes import letter, landscape
from .models import Familias, Beneficiarios
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Beneficiarios, Familias, Salidas, Area, ItemInventario, ItemInventario, Movimientos
from datetime import date
from datetime import datetime
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Count
from django.db import models
from django.db.models import Q
from django.contrib.auth.views import LoginView
from django.http import FileResponse
from django.shortcuts import render
from reportlab.pdfgen import canvas
from io import BytesIO
from django.views.generic import TemplateView
from pynotifier import Notification
from django.contrib import messages
import re
from django.db.models import Sum




# Create your views here.

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")',
)




def inicio(request):
    return render(request, 'index.html')


# --------------------AGREGAR BENEFICIARIO------------------------------------------------


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


# --------------------------------TERMINA AGREGAR BENEFICIARIO------------------------------------


# ----------------------------------LISTAR BENEFICIARIO--------------------------------
def listar(request):
    # Obtener el nombre de la solicitud GET
    nombre_query = request.GET.get('nombre', '')

    # Filtrar beneficiarios por nombre
    beneficiarios = Beneficiarios.objects.filter(
        Q(nombre__icontains=nombre_query) | Q(
            apellido__icontains=nombre_query),
        estado=True
    )
    datos = {'beneficiarios': beneficiarios}
    return render(request, 'crud-beneficiarios/listar.html', datos)

# --------------------------------TERMINA LISTAR BENEFICIARIO-------------------------------


# --------------------------------ACTUALIZAR BENEFICIARIO-------------------------------
def actualizar(request):
    beneficiarios = Beneficiarios.objects.all()
    datos = {'beneficiarios': beneficiarios}
    return render(request, 'crud-beneficiarios/actualizar.html', datos)

# --------------------------------TERMINA ACTUALIZAR BENEFICIARIO-------------------------------


# --------------------------------DAR SALIDA A  BENEFICIARIO-------------------------------
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

# -----------------------------TERMINA DAR SALIDA BENEFICIARIO-------------------------------


# -----------BENEFICIARIOS RETIRADOS --------
def beneficiarios_retirados(request):

    beneficiarios = Beneficiarios.objects.filter(estado=0).all()

    # Obtener la fecha de salida de cada beneficiario y agregarla a la lista de beneficiarios
    for beneficiario in beneficiarios:
        salida = Salidas.objects.filter(
            codigo_beneficiario=beneficiario).first()
        if salida:
            beneficiario.fecha_salida = salida.fecha_salida
            beneficiario.tipo_salida = salida.tipo_salida
            beneficiario.motivo = salida.motivo

    return render(request, 'crud-beneficiarios/beneficiarios_retirados.html', {
        'beneficiarios': beneficiarios
    })


# ------------FIN BENEFICIARIOS RETIRADOS --------------------------------


# -----------------listar familias --------
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

# --------------------TERMINA LISTAR FAMILIAS-------------------------------


# ----------------------- INVENTARIO-------------------------------
def registrar_articulo(request):
    if request.method == 'POST':
        try:
            # Capturar los datos del formulario
            cantidad = request.POST.get('cantidad')
            descripcion_articulo = request.POST.get('descripcion_articulo')
            fecha_compra = request.POST.get('fecha_compra')
            area_id = request.POST.get('area')
            donacion = request.POST.get('donacion')
            numero_cheque = request.POST.get('numero_cheque')
            numero_factura = request.POST.get('numero_factura')
            proveedor = request.POST.get('proveedor')
            encargado = request.POST.get('encargado')
            valor_compra = request.POST.get('valor_compra')
            numero_acta = request.POST.get('numero_acta')

            # Obtener la instancia del modelo Area correspondiente al valor de la variable id_area
            area = Area.objects.get(id_area=area_id)

            # Crear una instancia del modelo con los datos
            nuevo_articulo = ItemInventario(
                cantidad=cantidad,
                descripcion_articulo=descripcion_articulo,
                fecha_compra=fecha_compra,
                area_id=area,  # Asignar el objeto Area, no su ID
                donacion=donacion,
                numero_cheque=numero_cheque,
                numero_factura=numero_factura,
                proveedor=proveedor,
                encargado=encargado,
                valor_compra=valor_compra,
                numero_acta=numero_acta,
                estado=True,
                auditado=False
            )

            # Guardar en la base de datos
            nuevo_articulo.save()

            # Redirigir a la página de éxito o a donde desees
            return redirect('listar')

        except Exception as e:
            # Captura la excepción y muestra una alerta al usuario
            messages.error(request, f"Se produjo un error: {str(e)}")

    areas = Area.objects.all()
    datos = {'areas': areas}
    return render(request, 'inventario/registrar_articulo.html', datos)



# ------------------------------------------------------


def crear_area(request):
    if request.method == 'POST':
        nombre_area = request.POST.get('nombre_area')
        ubicacion = request.POST.get('ubicacion')
        descripcion = request.POST.get('descripcion')

        # Validar que `nombre_area` solo contenga letras
        if not re.match("^[A-Za-z ]+$", nombre_area):
            # Si no contiene solo letras, puedes mostrar un mensaje de error o tomar otra acción
            error_message = "El nombre del área debe contener solo letras y espacios."
            return render(request, 'inventario/crear_area.html', {'error_message': error_message})

        nueva_area = Area(
            nombre_area=nombre_area,
            ubicacion=ubicacion,
            descripcion=descripcion,
        )

        nueva_area.save()

        # Agrega un mensaje de éxito

        # Redirige al usuario a la página de inicio
        return redirect('listar')

    return render(request, 'inventario/crear_area.html')

# ----------------------------------------------------------------


def listar_articulos(request):
    # Obtener el nombre de la solicitud GET
    descripcion = request.GET.get('descripcion', '')

    # Filtrar beneficiarios por nombre
    inventario = ItemInventario.objects.filter(
        Q(descripcion_articulo__icontains=descripcion),
        estado=True
    )
    
    # Calcular la suma de los valores de compra
    total_gastado = inventario.aggregate(Sum('valor_compra'))['valor_compra__sum']
    
    datos = {'inventario': inventario, 'total_gastado': total_gastado}

    return render(request, 'inventario/listar_articulos.html', datos)

# ----------------------------------------------------------------


from django.db.models import Sum

def buscar_area(request):
    areas = Area.objects.all()
    articulos = ItemInventario.objects.filter(estado=True)

    if request.method == 'GET':
        # Obtener el ID del área seleccionada desde la solicitud GET
        area_id = request.GET.get('area_id')

        # Filtrar los artículos por área
        if area_id:
            articulos = articulos.filter(area_id=area_id)

    # Calcular la suma de los valores de compra para los artículos filtrados
    total_gastado = articulos.aggregate(Sum('valor_compra'))['valor_compra__sum']

    return render(request, 'inventario/buscar_area.html', {
        'areas': areas,
        'articulos': articulos,
        'total_gastado': total_gastado
    })

#----------------------------------------------------------------

def editar_articulo(request):
    return render(request, 'inventario/editar_articulo.html')


def listar_bajas(request):
    return render(request, 'inventario/listar_bajas.html')





def baja_articulo(request):
    return render(request, 'inventario/baja_articulo.html')

# -------------------------TERMINA  INVENTARIO-------------------------------




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


# --------------reporteria EXPORTAR PDF-------------


def exportar_pdf(request):
    # Crear un objeto BytesIO para guardar el PDF en memoria
    buffer = BytesIO()

    # Crear un objeto PDF con orientación horizontal (landscape)
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Crear una lista para almacenar los datos de la tabla
    data = [["CÓDIGO", "NOMBRE", "APELLIDO", "EDAD",
             "NIVEL", "FECHA NACIMIENTO", "OBSERVACIONES"]]

    # Agregar datos a la lista desde tu modelo (asegúrate de importar Beneficiarios)
    beneficiarios = Beneficiarios.objects.all()
    for beneficiario in beneficiarios:
        data.append([
            beneficiario.codigo_beneficiario,
            beneficiario.nombre,
            beneficiario.apellido,
            beneficiario.edad,
            beneficiario.nivel,
            beneficiario.fecha_nacimiento,
            beneficiario.observacion,
        ])

    # Crear una tabla y definir su estilo
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    # Crear el PDF y agregar la tabla
    elements = [table]
    doc.build(elements)

    # Configurar el objeto BytesIO para la lectura desde el principio
    buffer.seek(0)

    # Devolver el PDF como una respuesta de archivo
    response = FileResponse(buffer, as_attachment=True,
                            filename='lista_beneficiarios.pdf')
    return response


# ---------------------------
