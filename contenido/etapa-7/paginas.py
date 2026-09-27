"""Servicios y Contacto con el lenguaje de la Etapa 7. Mismo texto que la
Etapa 3 (contenido/etapa-3/copy.md); cambia la forma:

- Servicios: la página de la Etapa 3 con una figura en el hero, "tu
  recorrido", con los mismos cuatro momentos que la sección "Qué pasa en cada
  etapa" (decorativa: el contenido está en el texto).
- Contacto: el formulario queda solo a la izquierda (menos carga al
  escribir) y "Qué pasa después de enviar" pasa a la columna derecha como un
  recorrido de tres pasos conectados, en lugar de la ilustración.
Lo usa generar-bloques.py.
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parents[2]
E3 = RAIZ / 'contenido/etapa-3/bloques'

# Nodos del recorrido: (x, y, texto) en un lienzo de 420 × 380. Los textos van
# hacia afuera (izquierda o derecha), lejos de la línea.
RECORRIDO = [
    (150, 40, 'Nos escribes'),
    (262, 140, 'Primer encuentro'),
    (150, 240, 'De 3 a 6 sesiones'),
    (262, 340, 'Tu plan por escrito'),
]


def figura_recorrido():
    pts = RECORRIDO
    # Ruta de circuito: tramo vertical, diagonal a 45° y tramo vertical.
    d = f'M{pts[0][0]} {pts[0][1]}'
    for (x0, y0, _), (x1, y1, _) in zip(pts, pts[1:]):
        dx, dy = x1 - x0, y1 - y0
        diag = min(abs(dx), dy)
        recto = (dy - diag) / 2
        signo = 1 if dx > 0 else -1
        d += f' L{x0} {y0 + recto:.0f} L{x0 + signo * diag:.0f} {y0 + recto + diag:.0f} L{x1} {y1}'
    nodos = ''.join(
        f'<g class="calma-recorrido__nodo" style="--i:{i}"><circle cx="{x}" cy="{y}" r="{11 if i == len(pts) - 1 else 8}"/>'
        f'<circle class="calma-recorrido__halo" cx="{x}" cy="{y}" r="{20 if i == len(pts) - 1 else 16}"/>'
        f'<text x="{x - 26 if x < 200 else x + 26}" y="{y + 5}" text-anchor="{"end" if x < 200 else "start"}">{t}</text></g>'
        for i, (x, y, t) in enumerate(pts))
    return ('<div class="calma-hero__media calma-recorrido" aria-hidden="true">'
            '<svg viewBox="0 0 420 380" width="420" height="380" focusable="false">'
            f'<path class="calma-recorrido__base" d="{d}"/><path class="calma-recorrido__linea" pathLength="1" d="{d}"/>'
            f'<path class="calma-recorrido__senal" pathLength="1" d="{d}"/>{nodos}</svg></div>')


def servicios(cabecera):
    s = (E3 / 'servicios.html').read_text(encoding='utf-8')
    s = re.sub(r'^<!--.*?-->\n', '', s, count=1, flags=re.S)
    s = s.replace('<div class="calma-hero__inner">', '<div class="calma-hero__inner calma-hero__inner--media">', 1)
    # La figura va después de la columna de texto del hero.
    i = s.index('</ul>\n</div>\n</div>\n</section>', s.index('calma-facts'))
    corte = i + len('</ul>\n</div>\n')
    s = s[:corte] + figura_recorrido() + '\n' + s[corte:]
    return (cabecera('Servicios',
                     'Reemplaza TODO el contenido de Servicios (el bloque de la Etapa 3). Un solo bloque "HTML personalizado".\n'
                     '     Mismo texto que la Etapa 3; se agrega la figura "tu recorrido" en el hero. Estilos: plugin (calma-etapa7.css).')
            + s)


def contacto_intro(cabecera):
    return (cabecera('Contacto · intro',
                     'Reemplaza el bloque de intro de la Etapa 3 (encima del formulario). "Qué pasa después de enviar" se muda a la columna derecha.')
            + '''<div class="calma-page calma-contact-intro">
<h1>¿Cómo podemos ayudarte?</h1>
<p class="calma-contact-intro__lead">Cuéntanos en unas líneas qué está pasando. Con eso te decimos quién del equipo encaja mejor y cómo sería el primer encuentro.</p>
</div>
''')


def contacto_proceso(cabecera):
    pasos = [
        ('Leemos tu mensaje.', 'En 48 horas hábiles te respondemos desde hola@codigocalma.com con quién del equipo encaja mejor.'),
        ('Te proponemos un primer encuentro.', 'Una hora, online, para entender tu contexto y salir con un objetivo por escrito.'),
        ('Decides si seguimos.', 'Si seguimos, trabajamos de tres a seis sesiones. Si vemos que este no es el lugar, te lo decimos y te orientamos.'),
    ]
    items = ''.join(f'<li><strong>{t}</strong> {d}</li>' for t, d in pasos)
    return (cabecera('Contacto · qué pasa después (columna derecha)',
                     'Reemplaza la ilustración de la columna derecha de Contacto. Bloque "HTML personalizado". Mismo texto que la Etapa 3.')
            + f'''<aside class="calma-proceso" aria-labelledby="proceso-titulo">
<h2 id="proceso-titulo">Qué pasa después de enviar</h2>
<ol class="calma-proceso__pasos">{items}</ol>
</aside>
''')
