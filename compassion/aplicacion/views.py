from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageTemplate
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
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
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test









# Create your views here.

TEMPLATE_DIRS = (
    'os.path.join(BASE_DIR, "templates")',
)



@login_required
def inicio(request):
    return render(request, 'index.html')
@login_required
def vista_raiz(request):
    return render(request, 'index.html')

#-------------------DECORADORES DE PERMISOS----------


def es_usuario_beneficiario(user):
    return user.is_authenticated and user.rol == 'usuariobeneficiario'
#------------------END DECORADORES DE PERMISOS------

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

@login_required
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

        # Verificar si el código ya existe en la base de datos
        if Beneficiarios.objects.filter(codigo_beneficiario=codigo_beneficiario).exists():
            error_message = "El código de beneficiario ya existe."
        else:
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

#-----------------------VERIFICAR CODIGO-----


def verificar_codigo(request):
    try:
        codigo = request.GET.get('codigo', '')
        
        # Realiza la verificación de código aquí

        return JsonResponse({'exists': exists})
    except Exception as e:
        # Registra la excepción para diagnóstico
        print(e)
        return JsonResponse({'exists': False})


#-------------------END VERIFICAR CODIGO-------



#--------------------AGREGAR A FAMILIA EISTENTE
def agregar_existente(request):
    if request.method == 'POST':
        # Obtener el ID de la familia desde el formulario
        familia_id = request.POST.get('familia_id')
        # ---------OBTENIENDO DATOS DEL BENEFICIARIO
        codigo_beneficiario = request.POST.get('codigo')
        nombre_beneficiario = request.POST.get('nombre_beneficiario')
        apellido_beneficiario = request.POST.get('apellido_beneficiario')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')
        genero = request.POST.get('genero')
        nivel = request.POST.get('nivel')
        observacion = request.POST.get('observacion')
        # Resto de tu código para obtener los datos del beneficiario

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
        return redirect('listar_familias')
    else:
        return render(request, 'familias/listar_familias.html')


#-------------------END AGREGAR A FAMILIA EXISTENTE




# ----------------------------------LISTAR BENEFICIARIO--------------------------------
@login_required
#@user_passes_test(es_usuario_beneficiario)
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
@login_required
def actualizar(request):
    beneficiarios = Beneficiarios.objects.all()
    datos = {'beneficiarios': beneficiarios}
    return render(request, 'crud-beneficiarios/actualizar.html', datos)

# --------------------------------TERMINA ACTUALIZAR BENEFICIARIO-------------------------------


# --------------------------------DAR SALIDA A  BENEFICIARIO-------------------------------
@login_required
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
@login_required
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
@login_required
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

@login_required
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

@login_required
def listar_articulos(request):
    # Obtener el nombre de la solicitud GET
    descripcion = request.GET.get('descripcion', '')
    valor_compra = request.GET.get('valor_compra', '')


    # Filtrar articulo por nombre
    inventario = ItemInventario.objects.filter(
        Q(descripcion_articulo__icontains=descripcion),
        estado=True
    )
    # Calcular la suma de los valores de compra
    total_gastado = inventario.aggregate(Sum('valor_compra'))['valor_compra__sum']
     # Filtrar artículos por valor de compra
    if valor_compra:
        inventario = inventario.filter(Q(valor_compra__icontains=valor_compra))

    datos = {'inventario': inventario, 'total_gastado': total_gastado}

    return render(request, 'inventario/listar_articulos.html', datos)

# ----------------------------------------------------------------




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
    if request.method == 'POST':
        id_inventario = request.POST.get('id_articulo')
        fecha_movimiento = request.POST.get('fecha_movimiento')
        tipo_movimiento = request.POST.get('tipo_movimiento')
        descripcion = request.POST.get('descripcion')

        # Valida el valor del campo `fecha_movimiento`
        try:
            fecha_movimiento = datetime.datetime.strptime(
                fecha_movimiento, '%Y-%m-%d'
            )
        except ValueError:
            # El valor del campo `fecha_movimiento` no está en el formato correcto
            return render(
                request, 'inventario/listar_bajas.html', {'error': 'El valor del campo `fecha_movimiento` no está en el formato correcto.'}
            )

        # Obtén el artículo
        articulo = ItemInventario.objects.get(id_inventario=id_inventario)

        # Cambia el estado del artículo a inactivo
        articulo.estado = False
        articulo.save()

        # Registra un movimiento de salida
        movimiento = Movimientos(
            tipo_movimiento='S',
            fecha_movimiento=fecha_movimiento,
            descripcion=descripcion,
            inventario_id=articulo
        )
        movimiento.save()

        # Redirige a donde desees después de dar de baja el artículo
        return redirect('listar_articulos')






# -------------------------TERMINA  INVENTARIO-------------------------------




# REGISTRO DE USUARIO





# --------------reporteria EXPORTAR PDF-------------





def exportar_pdf(request):
    # Crear un objeto BytesIO para guardar el PDF en memoria
    buffer = BytesIO()

    # Crear un objeto PDF con orientación horizontal (landscape)
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Crear una lista para almacenar los datos de la tabla
    data = [["CÓDIGO", "NOMBRE", "APELLIDO", "EDAD",
             "NIVEL", "FECHA NACIMIENTO", "OBSERVACIONES"]]

    # Filtrar beneficiarios por estado activo y agregarlos a la lista
    beneficiarios = Beneficiarios.objects.filter(estado=True)
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
       ('BACKGROUND', (0, 0), (-1, 0), (0.8, 0.8, 0.8)),
   #     ('TEXTCOLOR', (0, 0), (-1, 0), (1, 1, 1)),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
       # ('BACKGROUND', (0, 1), (-1, -1), (0.9, 0.9, 0.9)),
        ('GRID', (0, 0), (-1, -1), 1, (0, 0, 0)),
    ]))

    # Crear el PDF y agregar la tabla
    elements = []
    # Establecer el título del documento
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    elements.append(Paragraph("Lista de Beneficiarios Activos", title_style))
    elements.append(table)

    doc.build(elements)

    # Configurar el objeto BytesIO para la lectura desde el principio
    buffer.seek(0)

    # Devolver el PDF como una respuesta de archivo
    response = FileResponse(buffer, as_attachment=True,
                            filename='lista_beneficiarios_activos.pdf')
    return response
# ---------------------------


#--------------------------------
#restriccion de acceso
