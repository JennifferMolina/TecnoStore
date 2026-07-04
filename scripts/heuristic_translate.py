"""
Traducción heurística simple para `i18n_dynamic.json`.

No usa servicios externos. Hace reemplazos basados en un diccionario
de términos comunes y algunos mapeos por palabra.

Ejecuta localmente con:
    python scripts/heuristic_translate.py

El script actualizará `tienda/static/tienda/i18n_dynamic.json`.
"""
from pathlib import Path
import json
import re

OUT = Path('tienda') / 'static' / 'tienda' / 'i18n_dynamic.json'

REPLACEMENTS = {
    # frases completas (mayor longitud primero)
    'los más vendidos': 'best sellers',
    'más vendido': 'best seller',
    'ver productos': 'see products',
    'ver más ›': 'see more ›',
    'ver más': 'see more',
    'todos los productos': 'all products',
    'todas las categorías': 'all categories',
    'orden por defecto': 'default order',
    'precio menor a mayor': 'price: low to high',
    'precio mayor a menor': 'price: high to low',
    'nombre a-z': 'name A-Z',
    'aplicar': 'apply',
    'limpiar': 'clear',
    'enviar mensaje': 'send message',
    'contacto': 'contact',
    'inicio': 'home',
    'catálogo': 'catalog',
    'perfil': 'profile',
    'mis compras': 'my purchases',
    'carrito': 'cart',
    'agregar al carrito': 'add to cart',
    'agregar': 'add',
    'nuevo': 'new',
    'oferta': 'offer',
    'disponible': 'available',
    'envíos gratis': 'free shipping',
    'hasta 12 cuotas': 'up to 12 installments',
    'compra segura': 'secure purchase',
    'atención personalizada': 'personalized support',
    'datos de contacto': 'contact details',
    'ubicación': 'location',
    'correo': 'email',
    'teléfono': 'phone',
    'horario': 'hours',
    'volver arriba ↑': 'Back to top ↑',
}

WORD_MAP = {
    'tecnología': 'technology',
    'tecnologico': 'technological',
    'tecnológicos': 'technologies',
    'productos': 'products',
    'producto': 'product',
    'precio': 'price',
    'precio$': 'price',
    'precio:': 'price:',
    's/': '',
    'con': 'with',
    'y': 'and',
    'para': 'for',
    'seleccionados': 'selected',
    'clientes': 'customers',
    'descubre': 'discover',
    'los': 'the',
    'las': 'the',
    'el': 'the',
    'la': 'the',
    'de': 'of',
    '📦': '📦',
}

def normalize(s):
    return re.sub(r"\s+", ' ', s.strip()).lower()

def translate_phrase(s):
    if not s or not isinstance(s, str):
        return s
    orig = s
    key = normalize(s)
    # try full replacements first
    for k in sorted(REPLACEMENTS.keys(), key=lambda x: -len(x)):
        if key == k:
            return REPLACEMENTS[k]
    # try containing phrase replacements
    out = key
    for k, v in REPLACEMENTS.items():
        out = out.replace(k, v)
    # word by word
    words = out.split(' ')
    mapped = []
    for w in words:
        w_clean = re.sub(r"[^\wáéíóúñüÁÉÍÓÚÑÜ-]", '', w)
        if w_clean in WORD_MAP:
            mapped.append(WORD_MAP[w_clean])
        else:
            mapped.append(w)
    res = ' '.join(mapped)
    # preserve capitalization of the original start
    if orig and orig[0].isupper():
        res = res.capitalize()
    # restore punctuation that wasn't handled
    # naive: return res
    return res

def main():
    if not OUT.exists():
        print('No se encontró', OUT)
        return
    data = json.loads(OUT.read_text(encoding='utf8'))
    data.setdefault('es', {})
    data.setdefault('en', {})

    updated = 0
    for key, es_val in list(data['es'].items()):
        en_val = data['en'].get(key)
        if not en_val or en_val == es_val:
            tr = translate_phrase(es_val)
            data['en'][key] = tr
            updated += 1

    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf8')
    print(f'Actualizadas {updated} entradas en {OUT}')

if __name__ == '__main__':
    main()
