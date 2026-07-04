from django.contrib import admin
from .models import (
    Categoria,
    Producto,
    PerfilCliente,
    Carrito,
    ItemCarrito,
    Pedido,
    DetallePedido,
    MensajeContacto
)


admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(PerfilCliente)
admin.site.register(Carrito)
admin.site.register(ItemCarrito)
admin.site.register(Pedido)
admin.site.register(DetallePedido)


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ('asunto', 'nombre', 'email', 'fecha', 'leido')
    list_filter = ('leido', 'fecha')
    search_fields = ('nombre', 'email', 'asunto', 'mensaje')
    readonly_fields = ('fecha',)
