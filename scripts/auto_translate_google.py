"""
Rellena las claves faltantes en `tienda/static/tienda/i18n_dynamic.json`
usando Google Cloud Translate API.

Cómo usar (localmente):
1. Instala la librería:
   pip install google-cloud-translate

2. Crea una cuenta de servicio en Google Cloud y descarga el JSON.
   Exporta la ruta en tu shell:
   Windows PowerShell:
     $env:GOOGLE_APPLICATION_CREDENTIALS = 'C:\ruta\a\key.json'
   Linux/macOS:
     export GOOGLE_APPLICATION_CREDENTIALS="/ruta/a/key.json"

3. Ejecuta:
   python scripts/auto_translate_google.py

El script traducirá del español (`es`) a inglés (`en`) las claves que aún
no tengan traducción en `en` o cuyo valor en `en` sea idéntico al de `es`.
"""

import os
import json
import sys
from pathlib import Path

OUT_FILE = Path('tienda') / 'static' / 'tienda' / 'i18n_dynamic.json'

def load_json(path):
    if not path.exists():
        print('No existe', path)
        sys.exit(1)
    with open(path, 'r', encoding='utf8') as f:
        return json.load(f)

def save_json(path, data):
    with open(path, 'w', encoding='utf8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def translate_with_google(client, text, target='en', source='es'):
    # client is google.cloud.translate_v2.Client
    result = client.translate(text, target_language=target, source_language=source)
    return result.get('translatedText')

def main():
    try:
        data = load_json(OUT_FILE)
    except Exception as e:
        print('Error leyendo JSON:', e)
        sys.exit(1)

    # ensure structure
    data.setdefault('es', {})
    data.setdefault('en', {})

    # detect missing keys to translate
    to_translate = []
    for key, es_val in data['es'].items():
        en_val = data['en'].get(key)
        if not en_val or en_val == es_val:
            to_translate.append((key, es_val))

    if not to_translate:
        print('No hay claves pendientes para traducir.')
        return

    # try to import google client
    try:
        from google.cloud import translate_v2 as translate
    except Exception:
        print('La librería google-cloud-translate no está instalada.')
        print('Instálala con: pip install google-cloud-translate')
        print('Además debes exportar GOOGLE_APPLICATION_CREDENTIALS apuntando al JSON de credenciales.')
        sys.exit(1)

    # create client (uses env var GOOGLE_APPLICATION_CREDENTIALS)
    client = translate.Client()

    print(f'Traduciendo {len(to_translate)} entradas con Google Translate...')
    for key, es_val in to_translate:
        try:
            translated = translate_with_google(client, es_val, target='en', source='es')
            data['en'][key] = translated
            print('OK:', key, '→', translated)
        except Exception as e:
            print('Fallo al traducir', key, e)

    save_json(OUT_FILE, data)
    print('Archivo actualizado en', OUT_FILE)

if __name__ == '__main__':
    main()
