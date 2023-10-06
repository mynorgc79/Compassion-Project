from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from usuario.models import Usuario
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test


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


