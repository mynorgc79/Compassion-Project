from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from usuario.models import Usuario
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm 


# Create your views here.


# def inicio(request):
 #   return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        # Obten los datos de inicio de sesión del formulario
        username = request.POST['usuario']
        password = request.POST['contraseña']

        # Autentica al usuario utilizando las credenciales proporcionadas
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Si el usuario es autenticado con éxito, inicia la sesión
            login(request, user)
            request.session['user_name'] = user.get_full_name()
            return redirect('inicio')  # Cambia a la página principal después del inicio de sesión
        else:
            # Si la autenticación falla, muestra un mensaje de error
            error_message = "Credenciales inválidas. Inténtalo de nuevo."
            messages.error(request, error_message)
            return render(request, 'usuarios/login.html')

    # Si la solicitud es GET, simplemente muestra el formulario de inicio de sesión
    return render(request, 'usuarios/login.html')


def _logout(request):
    logout(request)
    return redirect('login')



@login_required
def registrar_usuario(request):
    if request.method == 'POST':
        # Obtén los datos del formulario
        username = request.POST['username']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role']

        # Verifica que las contraseñas coincidan
        if password != confirm_password:
            return render(request, 'usuarios/registro_usuario.html', {'error_message': 'Las contraseñas no coinciden'})

        # Crea el usuario
        user = get_user_model().objects.create_user(
            username=username,
            password=password,
            nombres=first_name,
            apellidos=last_name,
            rol=role
            
        )

        # Asigna el valor de usuario_administrador
        if role == 'Administrador':
            user.usuario_administrador = 1
        else:
            user.usuario_administrador = 0
           

        user.save()

        # Inicia sesión al usuario recién registrado
        login(request, user)

        # Redirige a donde desees después del registro exitoso
        return redirect('inicio')

    return render(request, 'usuarios/registro_usuario.html')
# END REGISTRAR USUARIO




def editar_usuario(request):
     usuarios = Usuario.objects.all()
     return render(request, 'usuarios/editar_usuario.html', {'usuarios': usuarios})



#--------------GUARDAR ESTADO---------

def actualizar_usuario(request):
    if request.method == 'POST':
        for usuario in Usuario.objects.all():
            estado_key = f'estado_{usuario.id}'
            nuevo_estado = request.POST.get(estado_key)

            # El campo de checkbox devolverá "on" si está marcado o será None si no está marcado
            if nuevo_estado == 'on':
                usuario.is_active = True
            else:
                usuario.is_active = False

            usuario.save()

        # Agrega un mensaje de éxito
        messages.success(request, 'Los estados de los usuarios se han actualizado correctamente.')

    # Redirige a la página de lista de usuarios (o la que desees)
    return redirect('usuarios/registro_usuario')

def cambiar_contrasena(request):
    if request.method == 'POST':
        usuario_id = request.POST.get('usuario_id')
        nueva_contrasena = request.POST.get('nueva_contrasena')
        confirmar_contrasena = request.POST.get('confirmar_contrasena')

        # Tu lógica de validación y cambio de contraseña aquí
        if nueva_contrasena == confirmar_contrasena:
            # Cambia la contraseña y guarda el usuario
            usuario = Usuario.objects.get(id=usuario_id)
            usuario.set_password(nueva_contrasena)
            usuario.save()
            messages.success(request, 'Contraseña cambiada con éxito.')
        else:
            messages.error(request, 'No se pudo cambiar la contraseña. Las contraseñas no coinciden.')

        return redirect('registro_usuario')

#---------------------CAMBIO DE CONTRASEÑA----------------
