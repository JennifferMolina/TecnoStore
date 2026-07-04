import json
import random
import requests

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .models import (
    Producto,
    Categoria,
    Carrito,
    ItemCarrito,
    Pedido,
    DetallePedido,
    PerfilCliente,
    MensajeContacto
)
from .forms import (
    CheckoutEnvioForm,
    ContactoForm,
    PagoSimuladoForm,
    ProductoForm,
    UserPerfilForm,
    PerfilClienteForm
)


def es_admin(user):
    return user.is_staff or user.is_superuser


@login_required
def home(request):
    return render(request, 'home.html')


def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'registro.html', {'form': form})


def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(
                request,
                _('Tu mensaje fue enviado correctamente. Te contactaremos pronto.')
            )
            return redirect('contacto')
    else:
        initial = {}

        if request.user.is_authenticated:
            initial = {
                'nombre': request.user.get_full_name() or request.user.username,
                'email': request.user.email
            }

        form = ContactoForm(initial=initial)

    return render(request, 'contacto.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def lista_productos(request):
    productos = Producto.objects.all()
    return render(request, 'productos/lista.html', {'productos': productos})


@login_required
@user_passes_test(es_admin)
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            messages.success(request, _('Producto creado correctamente.'))
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'productos/formulario.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def editar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)

    if request.method == 'POST':
        form = ProductoForm(
            request.POST,
            request.FILES,
            instance=producto
        )

        if form.is_valid():
            form.save()
            messages.success(request, _('Producto actualizado correctamente.'))
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'productos/formulario.html', {'form': form})


@login_required
@user_passes_test(es_admin)
def eliminar_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    producto.delete()
    messages.success(request, _('Producto eliminado correctamente.'))
    return redirect('lista_productos')


@login_required
def catalogo(request):
    productos = Producto.objects.all()
    categorias = Categoria.objects.all()

    categoria_id = request.GET.get('categoria')
    orden = request.GET.get('orden')
    busqueda = request.GET.get('q')

    if busqueda:
        productos = productos.filter(nombre__icontains=busqueda)

    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)

    if orden == 'precio_asc':
        productos = productos.order_by('precio')
    elif orden == 'precio_desc':
        productos = productos.order_by('-precio')
    elif orden == 'nombre_asc':
        productos = productos.order_by('nombre')
    else:
        productos = productos.order_by('id')

    mas_vendidos = Producto.objects.all()[:5]

    tecnologia = Producto.objects.filter(categoria__nombre__iexact='Tecnología')[:4]
    accesorios = Producto.objects.filter(categoria__nombre__iexact='Accesorios')[:4]
    gaming = Producto.objects.filter(categoria__nombre__iexact='Gaming')[:4]

    return render(
        request,
        'productos/catalogo.html',
        {
            'productos': productos,
            'categorias': categorias,
            'categoria_seleccionada': categoria_id,
            'orden_seleccionado': orden,
            'busqueda': busqueda,
            'mas_vendidos': mas_vendidos,
            'tecnologia': tecnologia,
            'accesorios': accesorios,
            'gaming': gaming
        }
    )


def detalle_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    return render(
        request,
        'productos/detalle_producto.html',
        {
            'producto': producto
        }
    )


@login_required
def agregar_al_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)

    carrito, creado = Carrito.objects.get_or_create(
        usuario=request.user
    )

    item, creado = ItemCarrito.objects.get_or_create(
        carrito=carrito,
        producto=producto
    )

    if not creado:
        item.cantidad += 1
        item.save()

    messages.success(request, _('Producto agregado al carrito.'))
    return redirect('catalogo')


@login_required
def ver_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(
        usuario=request.user
    )

    return render(
        request,
        'carrito.html',
        {
            'carrito': carrito
        }
    )


@login_required
def eliminar_item_carrito(request, item_id):
    item = get_object_or_404(
        ItemCarrito,
        id=item_id,
        carrito__usuario=request.user
    )

    if item.cantidad > 1:
        item.cantidad -= 1
        item.save()
        messages.success(request, _('Se descontó una unidad del producto.'))
    else:
        item.delete()
        messages.success(request, _('Producto eliminado del carrito.'))

    return redirect('ver_carrito')


@login_required
def vaciar_carrito(request):
    carrito, creado = Carrito.objects.get_or_create(
        usuario=request.user
    )

    carrito.items.all().delete()

    messages.success(request, _('Carrito vaciado correctamente.'))
    return redirect('ver_carrito')


@login_required
def checkout(request):
    return redirect('checkout_envio')


@login_required
def checkout_envio(request):
    carrito, creado = Carrito.objects.get_or_create(
        usuario=request.user
    )

    if carrito.items.count() == 0:
        messages.error(request, _('No puedes finalizar una compra con el carrito vacío.'))
        return redirect('ver_carrito')

    initial = request.session.get('datos_envio', {})

    if not initial:
        initial = {
            'nombre_completo': request.user.get_full_name() or request.user.username,
            'email': request.user.email
        }

    if request.method == 'POST':
        form = CheckoutEnvioForm(request.POST)

        if form.is_valid():
            request.session['datos_envio'] = form.cleaned_data
            request.session.modified = True
            return redirect('checkout_pago')

        print('Errores checkout_envio:', form.errors)
        messages.error(
            request,
            _('Revisa los datos de envío. Hay campos obligatorios o inválidos.')
        )
    else:
        form = CheckoutEnvioForm(initial=initial)

    return render(
        request,
        'checkout_envio.html',
        {
            'form': form,
            'carrito': carrito
        }
    )


@login_required
def checkout_pago(request):
    carrito, creado = Carrito.objects.get_or_create(
        usuario=request.user
    )

    if carrito.items.count() == 0:
        messages.error(request, _('No puedes pagar un carrito vacío.'))
        return redirect('ver_carrito')

    if not request.session.get('datos_envio'):
        messages.error(request, _('Primero debes completar los datos de envío.'))
        return redirect('checkout_envio')

    form = PagoSimuladoForm()

    return render(
        request,
        'checkout_pago.html',
        {
            'form': form,
            'carrito': carrito,
            'datos_envio': request.session.get('datos_envio')
        }
    )


@login_required
@require_POST
def confirmar_pago_simulado(request):
    carrito, creado = Carrito.objects.get_or_create(
        usuario=request.user
    )

    if carrito.items.count() == 0:
        messages.error(request, _('No puedes pagar un carrito vacío.'))
        return redirect('ver_carrito')

    datos_envio = request.session.get('datos_envio')

    if not datos_envio:
        messages.error(request, _('Primero debes completar los datos de envío.'))
        return redirect('checkout_envio')

    form = PagoSimuladoForm(request.POST)

    if not form.is_valid():
        print('Errores checkout_pago:', form.errors)
        messages.error(
            request,
            _('Revisa los datos de la tarjeta. Hay campos obligatorios o inválidos.')
        )
        return render(
            request,
            'checkout_pago.html',
            {
                'form': form,
                'carrito': carrito,
                'datos_envio': datos_envio
            }
        )

    pedido = Pedido.objects.create(
        usuario=request.user,
        total=carrito.total(),
        estado='Pago simulado aprobado',
        nombre_completo=datos_envio.get('nombre_completo', ''),
        region=datos_envio.get('region', ''),
        ciudad=datos_envio.get('ciudad', ''),
        direccion=datos_envio.get('direccion', ''),
        telefono=datos_envio.get('telefono', ''),
        email=datos_envio.get('email', '')
    )

    for item in carrito.items.all():
        DetallePedido.objects.create(
            pedido=pedido,
            producto=item.producto,
            cantidad=item.cantidad,
            precio_unitario=item.producto.precio
        )

    carrito.items.all().delete()
    request.session.pop('datos_envio', None)

    messages.success(request, _('Compra confirmada correctamente.'))

    return redirect('mis_compras')


@login_required
def mis_compras(request):
    pedidos = Pedido.objects.filter(
        usuario=request.user
    ).order_by('-fecha')

    return render(
        request,
        'mis_compras.html',
        {
            'pedidos': pedidos
        }
    )


@login_required
@user_passes_test(es_admin)
def compras_admin(request):
    pedidos = Pedido.objects.select_related(
        'usuario'
    ).prefetch_related(
        'detalles__producto'
    ).order_by('-fecha')

    return render(
        request,
        'admin_compras.html',
        {
            'pedidos': pedidos
        }
    )


@login_required
@user_passes_test(es_admin)
def usuarios_empresa(request):
    usuarios = User.objects.filter(is_staff=True)

    return render(
        request,
        'usuarios_empresa.html',
        {
            'usuarios': usuarios
        }
    )


@login_required
@user_passes_test(es_admin)
def mensajes_contacto_admin(request):
    mensajes_contacto = MensajeContacto.objects.all()

    return render(
        request,
        'admin_contactos.html',
        {
            'mensajes_contacto': mensajes_contacto
        }
    )


@login_required
def perfil_usuario(request):
    perfil, creado = PerfilCliente.objects.get_or_create(
        usuario=request.user
    )

    if request.method == 'POST':
        user_form = UserPerfilForm(
            request.POST,
            instance=request.user
        )

        perfil_form = PerfilClienteForm(
            request.POST,
            request.FILES,
            instance=perfil
        )

        if user_form.is_valid() and perfil_form.is_valid():
            user_form.save()
            perfil_form.save()

            messages.success(
                request,
                _('Perfil actualizado correctamente.')
            )
            return redirect('perfil_usuario')
    else:
        user_form = UserPerfilForm(instance=request.user)
        perfil_form = PerfilClienteForm(instance=perfil)

    return render(
        request,
        'perfil_usuario.html',
        {
            'user_form': user_form,
            'perfil_form': perfil_form,
            'perfil': perfil
        }
    )


@csrf_exempt
@require_POST
def api_simular_pago(request):
    try:
        data = json.loads(request.body)

        monto = data.get('monto')
        metodo_pago = data.get('metodo_pago')
        cliente = data.get('cliente')

        if not monto or float(monto) <= 0:
            return JsonResponse(
                {
                    'estado': 'RECHAZADO',
                    'mensaje': 'El monto debe ser mayor a 0.'
                },
                status=400
            )

        codigo_transaccion = f"TXN-{random.randint(100000, 999999)}"

        return JsonResponse(
            {
                'estado': 'APROBADO',
                'codigo_transaccion': codigo_transaccion,
                'monto': monto,
                'metodo_pago': metodo_pago,
                'cliente': cliente,
                'mensaje': 'Pago simulado aprobado correctamente.'
            },
            status=200
        )

    except Exception as error:
        return JsonResponse(
            {
                'estado': 'ERROR',
                'mensaje': str(error)
            },
            status=500
        )
