#!/usr/bin/env python3
"""Correcciones de la Etapa 3 (se aplican sobre las de Etapas 1 y 2)."""
import json, pathlib
C = []
def add(id, tipo, paginas, donde, antes, despues, html_buscar=None, html_reemplazar=None, origen='', nota=''):
    C.append({k: v for k, v in dict(id=id, tipo=tipo, paginas=paginas, donde=donde, antes=antes, despues=despues,
             html_buscar=html_buscar, html_reemplazar=html_reemplazar, origen=origen, nota=nota).items() if v not in (None, '')})
MARK2 = '<mark style="background-color:rgba(0, 0, 0, 0)" class="has-inline-color has-theme-palette-2-color">'
add('I20', 'encabezado', ['home'], 'Inicio > "Te damos la bienvenida a Código Calma" > Nivel H1 → H2 (el H1 pasa al hero nuevo)',
    'H1', 'H2', '<h1 class="kt-adv-heading1204_e36b0d-85', '<h2 class="kt-adv-heading1204_e36b0d-85', origen='Etapa 3 · hero')
add('M01', 'nota', ['*'], 'Apariencia > Menús (principal y mobile): "Sobre Tatiana" → "Equipo" (página /equipo/)', 'Sobre Tatiana', 'Equipo', origen='Etapa 3')
out = pathlib.Path(__file__).with_name('correcciones.json')
out.write_text(json.dumps({'version': 'etapa-3', 'correcciones': C, 'excluidas': []}, ensure_ascii=False, indent=1), encoding='utf-8')
print(len(C), 'correcciones')
