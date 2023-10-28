from functools import wraps
from django.shortcuts import redirect


# Decorador personalizado para el rol de Administrador
def administrador_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.usuario_administrador:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('inicio')  # Reemplaza 'pagina_de_denegacion' con la URL apropiada para la página de denegación de acceso para no administradores
    return _wrapped_view

# Decorador personalizado para el rol de Usuario Beneficiario
def usuario_beneficiario_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.usuario_administrador or request.user.rol == 'usuarioBeneficiario':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('inicio')  # Reemplaza 'pagina_de_denegacion' con la URL apropiada para la página de denegación de acceso para usuarios no beneficiarios
    return _wrapped_view

# Decorador personalizado para el rol de Usuario Inventario
def usuario_inventario_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.usuario_administrador or request.user.rol == 'usuarioInventario':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('inicio')  # Reemplaza 'pagina_de_denegacion' con la URL apropiada para la página de denegación de acceso para usuarios no de inventario
    return _wrapped_view

