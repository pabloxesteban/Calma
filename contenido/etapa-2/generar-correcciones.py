#!/usr/bin/env python3
"""Correcciones de la Etapa 2 (mismo formato que contenido/etapa-1). Se aplican
sobre las de la Etapa 1. Ejecutar: python3 contenido/etapa-2/generar-correcciones.py"""
import json, pathlib

C = []
def add(id, tipo, paginas, donde, antes, despues, html_buscar=None, html_reemplazar=None, origen='', nota=''):
    C.append({k: v for k, v in dict(id=id, tipo=tipo, paginas=paginas, donde=donde, antes=antes, despues=despues,
             html_buscar=html_buscar, html_reemplazar=html_reemplazar, origen=origen, nota=nota).items() if v not in (None, '')})

add('H10', 'encabezado', ['herramientas'], 'Herramientas > "Aquí encontrarás recomendaciones…" > Nivel H6 → Párrafo (es una bajada)',
    'H6', 'Párrafo', '<h6 class="wp-block-heading has--font-size has-medium-font-size">Aquí', '<p class="has-medium-font-size">Aquí',
    origen='QA a11y etapa 1 (heading-order)')
for hid, app in [('196c3e-73', 'Headspace'), ('54dd54-e0', 'Finch'), ('0cf81c-b9', 'Calm'), ('0e7c38-7b', 'Daylio'), ('db9f2d-e0', 'PTSD Coach y Mindfulness Coach')]:
    add(f'H11-{hid[:4]}', 'encabezado', ['herramientas'], f'Herramientas > nombre de la app «{app}» > Nivel H6 → H3',
        'H6', 'H3', f'<h6 class="kt-adv-heading1618_{hid}', f'<h3 class="kt-adv-heading1618_{hid}', origen='QA a11y etapa 1 (heading-order)')

add('T20', 'encabezado', ['test'], 'Test > bloque "Dato que vale la pena saber" > Nivel H6 → H2 (sección de la página)',
    'H6', 'H2', '<h6 class="kt-adv-heading1941_513169-0a', '<h2 class="kt-adv-heading1941_513169-0a', origen='QA a11y etapa 1 (heading-order)')
add('T21', 'encabezado', ['test'], 'Test > las 3 Info Box de "Tus resultados son tuyos" > Etiqueta HTML del título: H5 → H3',
    'H5 (×3)', 'H3 (×3)', '<h5 class="kt-blocks-info-box-title">', '<h3 class="kt-blocks-info-box-title">', origen='QA a11y etapa 1 (heading-order)', nota='todas')

out = pathlib.Path(__file__).with_name('correcciones.json')
out.write_text(json.dumps({'version': 'etapa-2', 'correcciones': C, 'excluidas': []}, ensure_ascii=False, indent=1), encoding='utf-8')
md = ['# Correcciones de encabezados — Etapa 2', '', 'Generado desde `correcciones.json`. Se aplican después de las de la Etapa 1.', '',
      '| ✓ | ID | Dónde | Antes | Después | Origen |', '|---|---|---|---|---|---|']
md += [f"| ☐ | {c['id']} | {c['donde']} | {c['antes']} | {c['despues']} | {c.get('origen','')} |" for c in C]
out.with_name('correcciones.md').write_text('\n'.join(md) + '\n', encoding='utf-8')
print(len(C), 'correcciones ->', out)
