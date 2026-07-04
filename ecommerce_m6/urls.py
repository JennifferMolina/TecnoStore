from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

from tienda.views import (
    home,
    registro,
    contacto,
    lista_productos,
    crear_producto,
    editar_producto,
    eliminar_producto,
    catalogo,
    detalle_producto,
    agregar_al_carrito,
    ver_carrito,
    eliminar_item_carrito,
    vaciar_carrito,
    checkout,
    checkout_envio,
    checkout_pago,
    confirmar_pago_simulado,
    mis_compras,
    compras_admin,
    usuarios_empresa,
    mensajes_contacto_admin,
    api_simular_pago,
    perfil_usuario,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),

    path('', home, name='home'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registro/', registro, name='registro'),
    path('contacto/', contacto, name='contacto'),

    path('products/', lista_productos, name='lista_productos'),
    path('products/create/', crear_producto, name='crear_producto'),
    path('products/edit/<int:id>/', editar_producto, name='editar_producto'),
    path('products/delete/<int:id>/', eliminar_producto, name='eliminar_producto'),

    path('catalogo/', catalogo, name='catalogo'),
    path('producto/<int:producto_id>/', detalle_producto, name='detalle_producto'),
    path('carrito/agregar/<int:producto_id>/', agregar_al_carrito, name='agregar_al_carrito'),
    path('carrito/', ver_carrito, name='ver_carrito'),
    path('carrito/eliminar/<int:item_id>/', eliminar_item_carrito, name='eliminar_item_carrito'),
    path('carrito/vaciar/', vaciar_carrito, name='vaciar_carrito'),

    path('checkout/', checkout, name='checkout'),
    path('checkout/envio/', checkout_envio, name='checkout_envio'),
    path('checkout/pago/', checkout_pago, name='checkout_pago'),
    path('checkout/confirmar/', confirmar_pago_simulado, name='confirmar_pago_simulado'),
    path('mis-compras/', mis_compras, name='mis_compras'),

    path('admin-compras/', compras_admin, name='compras_admin'),
    path('usuarios-empresa/', usuarios_empresa, name='usuarios_empresa'),
    path('admin-contactos/', mensajes_contacto_admin, name='mensajes_contacto_admin'),

    path('api/pagos/simular/', api_simular_pago, name='api_simular_pago'),
    path('perfil/', perfil_usuario, name='perfil_usuario'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
