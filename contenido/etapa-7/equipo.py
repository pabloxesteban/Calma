"""Equipo y perfiles con el lenguaje de la Etapa 7. Mismo texto que la Etapa 3
(contenido/etapa-3/copy.md); cambia la forma:

- Equipo: figura "tres miradas" en el hero (las tres áreas que convergen en lo
  que trae cada persona, tal como lo dice el texto de la página) y tarjetas con
  el tono de cada área y el enlace siempre abajo.
- Perfiles: cada página toma el tono de su persona; "Equipo" pasa a ser un
  enlace de vuelta visible; "Formación declarada" se lee como un recorrido;
  las reseñas pierden el ícono duplicado de comillas; los artículos se muestran
  con su tema (sale de data/mapa-temas.json).
Lo usa generar-bloques.py.
"""
import json
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parents[2]
E3 = RAIZ / 'contenido/etapa-3/bloques'
MAPA = RAIZ / 'wp-content/plugins/codigo-calma/data/mapa-temas.json'

PERSONAS = {
    'tatiana-x-stacul': 'tatiana',
    'francisca-cortes-santoro': 'francisca',
    'emanuel-c-franco': 'emanuel',
}

# (x, y, iniciales, persona, área) en un lienzo de 420 × 360. El centro es "lo que traigas".
CENTRO = (210, 190)
MIRADAS = [
    (100, 70, 'TS', 'tatiana', 'Psicología'),
    (320, 70, 'FC', 'francisca', 'Accesibilidad cognitiva'),
    (210, 320, 'EF', 'emanuel', 'Gestión de proyectos'),
]


def sin_cabecera(s):
    return re.sub(r'^<!--.*?-->\n', '', s, count=1, flags=re.S)


def figura_miradas():
    cx, cy = CENTRO
    lineas, nodos = '', ''
    for i, (x, y, ini, persona, area) in enumerate(MIRADAS):
        # Tramo corto recto y diagonal a 45° hasta el centro (misma gramática de circuito que el hero).
        if x == cx:
            d = f'M{x} {y} L{cx} {cy}'
        else:
            dx = abs(cx - x)
            d = f'M{x} {y} L{x} {cy - dx} L{cx} {cy}'
        lineas += (f'<path class="calma-miradas__base" d="{d}"/>'
                   f'<path class="calma-miradas__linea calma-miradas__linea--{persona}" pathLength="1" style="--i:{i}" d="{d}"/>'
                   f'<path class="calma-miradas__senal calma-miradas__senal--{persona}" pathLength="1" d="{d}"/>')
        ty = y - 42 if y < cy else y + 52
        nodos += (f'<g class="calma-miradas__nodo calma-miradas__nodo--{persona}" style="--i:{i}">'
                  f'<circle cx="{x}" cy="{y}" r="28"/><text class="calma-miradas__ini" x="{x}" y="{y + 7}" text-anchor="middle">{ini}</text>'
                  f'<text x="{x}" y="{ty}" text-anchor="middle">{area}</text></g>')
    centro = (f'<g class="calma-miradas__centro"><circle class="calma-miradas__halo" cx="{cx}" cy="{cy}" r="24"/>'
              f'<circle cx="{cx}" cy="{cy}" r="11"/><text x="{cx + 26}" y="{cy + 34}">Lo que traigas</text></g>')
    return ('<div class="calma-hero__media calma-miradas" aria-hidden="true">'
            '<svg viewBox="0 0 420 380" width="420" height="380" focusable="false">'
            f'{lineas}{nodos}{centro}</svg></div>')


def equipo(cabecera):
    s = sin_cabecera((E3 / 'equipo.html').read_text(encoding='utf-8'))
    s = s.replace('<div class="calma-page">', '<div class="calma-page calma-equipo">', 1)
    s = s.replace('<div class="calma-hero__inner">', '<div class="calma-hero__inner calma-hero__inner--media">', 1)
    corte = s.index('</div></div></section>', s.index('calma-hero__lead')) + len('</div>')
    s = s[:corte] + figura_miradas() + s[corte:]
    for slug, persona in PERSONAS.items():
        s = s.replace(f'<article class="calma-card calma-person"><div class="calma-person__head"><span class="calma-avatar" role="img" aria-label="Foto de {nombre(slug)}',
                      f'<article class="calma-card calma-person calma-person--{persona}"><div class="calma-person__head"><span class="calma-avatar" role="img" aria-label="Foto de {nombre(slug)}', 1)
    return (cabecera('Equipo',
                     'Reemplaza TODO el contenido de la página Equipo (el bloque de la Etapa 3). Un solo bloque "HTML personalizado".\n'
                     '     Mismo texto que la Etapa 3; se agrega la figura "tres miradas" en el hero. Estilos: plugin (calma-etapa7.css).')
            + s)


def nombre(slug):
    return {'tatiana-x-stacul': 'Tatiana X. Stacul', 'francisca-cortes-santoro': 'Francisca Cortés Santoro',
            'emanuel-c-franco': 'Emanuel C. Franco'}[slug]


def articulos_con_tema(s):
    datos = json.loads(MAPA.read_text(encoding='utf-8'))
    temas = {t['k']: t['nombre'] for t in datos['temas']}

    def item(m):
        href, titulo = m.group(1), m.group(2)
        slug = href.rstrip('/').rsplit('/', 1)[-1]
        tema = datos['articulos'].get(slug, {}).get('tema')
        chip = f'<span class="calma-perfil__tema" data-tema="{tema}">{temas[tema]}</span>' if tema else ''
        return f'<li><a href="{href}">{chip}<span class="calma-perfil__titulo">{titulo}</span></a></li>'

    return re.sub(r'<li><a href="([^"]+)">(.*?)</a></li>', item, s)


def perfil(cabecera, slug):
    persona = PERSONAS[slug]
    s = sin_cabecera((E3 / f'equipo-{slug}.html').read_text(encoding='utf-8'))
    s = s.replace('<div class="calma-page">', f'<div class="calma-page calma-perfil calma-perfil--{persona}">', 1)
    # "Equipo" deja de ser rótulo (oculto en la Etapa 7) y pasa a ser un enlace de vuelta.
    # Va primero en el hero, antes del avatar, para que en el celular no quede debajo de la foto.
    s = s.replace('<p class="calma-eyebrow"><a href="https://codigocalma.com/equipo/">Equipo</a></p>', '', 1)
    s = s.replace('<div class="calma-hero__inner">',
                  '<div class="calma-hero__inner"><p class="calma-volver"><a href="https://codigocalma.com/equipo/">Volver al equipo</a></p>', 1)
    s = s.replace('<div class="calma-grid" style="margin-top:var(--calma-space-8)">', '<div class="calma-perfil__datos">', 1)
    s = re.sub(r'(<h2 style="font-size:var\(--calma-fs-lg\)">Formación declarada</h2><ul) class="calma-person__topics"',
               r'\1 class="calma-formacion"', s, count=1)
    # Artículos: lista con el tema de cada uno.
    i = s.find('<ul class="calma-person__topics" style="margin-top:var(--calma-space-4)">')
    if i >= 0:
        j = s.index('</ul>', i) + len('</ul>')
        lista = s[i:j].replace(' class="calma-person__topics" style="margin-top:var(--calma-space-4)"', ' class="calma-perfil__articulos"', 1)
        s = s[:i] + articulos_con_tema(lista) + s[j:]
    return (cabecera(nombre(slug),
                     f'Reemplaza TODO el contenido de la página {nombre(slug)} (hija de Equipo, bloque de la Etapa 3). Un solo bloque "HTML personalizado".\n'
                     '     Mismo texto que la Etapa 3; cambia la forma. Estilos: plugin (calma-etapa7.css).')
            + s)
