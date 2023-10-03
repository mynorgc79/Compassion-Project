from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
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
            return redirect('inicio')  # Cambia a la página principal después del inicio de sesión
        else:
            # Si la autenticación falla, muestra un mensaje de error
            error_message = "Credenciales inválidas. Inténtalo de nuevo."
            return render(request, 'usuarios/login.html', {'error_message': error_message})

    # Si la solicitud es GET, simplemente muestra el formulario de inicio de sesión
    return render(request, 'usuarios/login.html')

