import os
import sys
import json
import django
from pathlib import Path

# ensure project root is on sys.path so Django settings can be imported
project_root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(project_root))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_m6.settings')
django.setup()

from tienda.models import Producto, Categoria

out_path = os.path.join('tienda', 'static', 'tienda', 'i18n_dynamic.json')

data = {}
if os.path.exists(out_path):
    try:
        with open(out_path, 'r', encoding='utf8') as f:
            data = json.load(f)
    except Exception:
        data = {}

for lang in ('en', 'es'):
    data.setdefault(lang, {})

for c in Categoria.objects.all():
    key = c.nombre
    data['es'].setdefault(key, key)
    data['en'].setdefault(key, key)

for p in Producto.objects.all():
    key = p.nombre
    data['es'].setdefault(key, key)
    data['en'].setdefault(key, key)

os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Wrote', out_path)
