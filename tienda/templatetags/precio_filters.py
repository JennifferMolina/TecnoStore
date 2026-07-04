from django import template

register = template.Library()


@register.filter
def precio_clp(valor):
    try:
        valor = int(valor)
        return f"${valor:,}".replace(",", ".")
    except:
        return valor