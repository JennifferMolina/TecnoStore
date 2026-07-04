from .models import Carrito


def cantidad_carrito(request):
    cantidad = 0
    nombre_usuario_visible = ''
    rol_usuario_visible = ''

    if request.user.is_authenticated:
        carrito = Carrito.objects.filter(
            usuario=request.user
        ).first()

        if carrito:
            for item in carrito.items.all():
                cantidad += item.cantidad

        nombre_usuario_visible = (
            request.user.get_full_name().strip()
            or request.user.username
        )

        if request.user.is_staff or request.user.is_superuser:
            rol_usuario_visible = 'Administrador'
        else:
            rol_usuario_visible = 'Cliente'

    return {
        'cantidad_carrito': cantidad,
        'nombre_usuario_visible': nombre_usuario_visible,
        'rol_usuario_visible': rol_usuario_visible
    }
