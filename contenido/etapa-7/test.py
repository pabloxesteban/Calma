"""Test de consumo digital con el lenguaje de la Etapa 7 ("red clara").

Mismo texto y la misma lógica que el bloque de la Etapa 2 (el <script> y todos
los atributos data-calma-* quedan intactos); cambia la forma:

- Cabecera con la figura "12 preguntas, 4 dimensiones": doce puntos en cuatro
  arcos. Mientras respondes, se encienden los puntos de las preguntas ya
  contestadas (lo hace calma-organismo.js mirando la barra de progreso del
  test); al ver el resultado, se encienden todos. Es decorativa: el progreso
  real se anuncia con el texto "Pregunta N de 12".
- "Cómo funciona": tres pasos con un micro-organismo cada uno (elegir entre
  cuatro generaciones, doce preguntas, el perfil que se dibuja).
- "Antes de empezar" y "Qué mide" con su figura; "Qué mide" muestra los 4 × 3
  puntos y la escala de 1 a 4.
- "Dato que vale la pena saber" pasa a un bloque propio (reemplaza las dos
  filas de Kadence) con la imagen que se descubre y tres tarjetas con figura.
Lo usa generar-bloques.py.
"""
import math
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parents[2]
E2 = RAIZ / 'contenido/etapa-2/bloques/test-consumo-digital.html'

# Tono de cada dimensión (arena, lavanda, celeste, verde), en el orden de los arcos.
DIMENSIONES = [('#e2c17e', '#7a4d00'), ('#bdb0ee', '#5b3fb8'), ('#9cc3e3', '#1d5f94'), ('#9fd0c0', '#1f6b47')]


def svg(contenido, caja='0 0 160 100', ancho=160, alto=100, clase='calma-org'):
    return (f'<svg class="{clase}" viewBox="{caja}" width="{ancho}" height="{alto}" aria-hidden="true" focusable="false">'
            + contenido + '</svg>')


def figura_test():
    """Doce puntos en cuatro arcos de tres (las 4 dimensiones × 3 preguntas)."""
    c, r = 130, 130
    puntos, arcos = '', ''
    n = 0
    for d, (acento, texto) in enumerate(DIMENSIONES):
        base = -90 + d * 90
        a0, a1 = math.radians(base - 32), math.radians(base + 32)
        x0, y0 = c + 96 * math.cos(a0), r + 96 * math.sin(a0)
        x1, y1 = c + 96 * math.cos(a1), r + 96 * math.sin(a1)
        arcos += (f'<path class="calma-test-fig__arco" style="--acento:{acento};--i:{d}" pathLength="1" '
                  f'd="M{x0:.1f} {y0:.1f} A96 96 0 0 1 {x1:.1f} {y1:.1f}"/>')
        for k in (-24, 0, 24):
            a = math.radians(base + k)
            x, y = c + 96 * math.cos(a), r + 96 * math.sin(a)
            puntos += (f'<circle class="calma-test-fig__punto" style="--acento:{acento};--texto:{texto};--i:{n}" '
                       f'cx="{x:.1f}" cy="{y:.1f}" r="9"/>')
            n += 1
    return ('<div class="calma-test-fig" data-calma-test-fig aria-hidden="true">'
            + svg(f'<circle class="calma-test-fig__guia" cx="{c}" cy="{r}" r="96"/>{arcos}'
                  f'<circle class="calma-test-fig__halo" cx="{c}" cy="{r}" r="44"/>'
                  f'<circle class="calma-test-fig__nucleo" cx="{c}" cy="{r}" r="30"/>{puntos}'
                  f'<text class="calma-test-fig__num" x="{c}" y="{r + 6}" text-anchor="middle">12</text>',
                  '0 0 260 260', 260, 260, 'calma-test-fig__svg')
            + '</div>')


def org_generacion():
    # Cuatro generaciones en una línea; se elige una.
    nodos = ''.join(f'<circle class="o-nodo" style="--i:{i}" cx="{x}" cy="50" r="{9 if i == 2 else 5}"/>'
                    for i, x in enumerate((28, 62, 98, 132)))
    return svg('<path class="o-trazo" pathLength="1" d="M20 50 H140"/>' + nodos
               + '<circle class="o-anillo" style="--i:0" cx="98" cy="50" r="17"/>')


def org_preguntas():
    # Doce preguntas que se van contestando.
    return svg(''.join(f'<circle class="o-punto" style="--i:{f * 4 + k}" cx="{44 + k * 24}" cy="{26 + f * 24}" r="6"/>'
                        for f in range(3) for k in range(4)))


def org_perfil():
    # Cuatro ejes y el perfil que se dibuja entre ellos.
    c = (80, 50)
    ejes = ''.join(f'<path class="o-eje" d="M80 50 L{x} {y}"/>' for x, y in ((80, 8), (130, 50), (80, 92), (30, 50)))
    return svg(ejes + '<path class="o-trazo o-forma" pathLength="1" d="M80 20 L116 50 L80 80 L50 50 Z"/>'
               f'<circle class="o-nucleo" cx="{c[0]}" cy="{c[1]}" r="4"/>')


def org_pausa():
    # Una onda que se calma: una pausa para mirar cómo usas la tecnología.
    return svg('<path class="o-onda" d="M18 50 C34 22 46 78 62 50 S90 38 102 50 S126 56 142 50"/>'
               '<circle class="o-nucleo" cx="142" cy="50" r="4"/>')


def org_mide():
    # 4 dimensiones × 3 preguntas, y la escala de 1 a 4 puntos.
    puntos = ''.join(f'<circle class="o-punto" style="--i:{d * 3 + k};fill:{DIMENSIONES[d][0]}" cx="{22 + d * 22}" cy="{28 + k * 22}" r="6"/>'
                     for d in range(4) for k in range(3))
    barras = ''.join(f'<rect class="o-barra" style="--i:{i}" x="{112 + i * 11}" y="{78 - (i + 1) * 13}" width="7" height="{(i + 1) * 13}" rx="2"/>'
                     for i in range(4))
    return svg(puntos + barras)


def org_contexto():
    # Tres contextos que colapsan en uno.
    return svg(''.join(f'<circle class="o-contexto" style="--dx:{dx}px;--i:{i}" cx="{80 + off}" cy="50" r="22"/>'
                       for i, (dx, off) in enumerate(((-34, -10), (0, 0), (34, 10)))))


def org_datos():
    # Puntos de conducta; algunos se unen y dibujan un patrón.
    pts = [(28 + k * 26, 24 + f * 26) for f in range(3) for k in range(5)]
    marcados = [0, 6, 8, 14]
    dots = ''.join(f'<circle class="o-punto{" o-marcado" if i in marcados else ""}" style="--i:{i}" cx="{x}" cy="{y}" r="{5 if i in marcados else 3}"/>'
                   for i, (x, y) in enumerate(pts))
    d = 'M' + ' L'.join(f'{pts[i][0]} {pts[i][1]}' for i in marcados)
    return svg(f'<path class="o-trazo" pathLength="1" d="{d}"/>' + dots)


def org_reflejo():
    # Una forma y su reflejo: el valor está en mirarse, no en compararse.
    return svg('<path class="o-corte" d="M24 52 H136"/>'
               '<circle class="o-nucleo" cx="80" cy="26" r="7"/><path d="M62 46 C66 34 94 34 98 46"/>'
               '<g class="o-reflejo"><circle cx="80" cy="78" r="7"/><path d="M62 58 C66 70 94 70 98 58"/></g>')


def test(cabecera):
    s = E2.read_text(encoding='utf-8')
    s = re.sub(r'^<!--.*?-->\n', '', s, count=1, flags=re.S)
    s = s.replace('<div class="calma-test" id="calma-test">', '<div class="calma-test calma-test--e7" id="calma-test">', 1)
    # Cabecera: título y bajada a la izquierda, figura a la derecha.
    titulo = ('<h1 class="calma-test__title">Test de consumo digital</h1>\n'
              '<p class="calma-test__lead">Descubre cómo es tu relación con la tecnología en 5 minutos</p>')
    assert titulo in s
    s = s.replace(titulo, f'<header class="calma-test__hero"><div class="calma-test__hero-texto">\n{titulo}\n</div>{figura_test()}</header>', 1)
    # Intro: mismas frases, con figuras.
    a = s.index('<section class="calma-test__intro" data-calma-intro')
    b = s.index('</section>', a) + len('</section>')
    intro = s[a:b]
    nojs = re.search(r'<p class="calma-test__nojs" data-calma-nojs>.*?</p>', intro, re.S).group(0)
    empezar = re.search(r'<button type="button" class="calma-test__btn calma-test__btn--primary calma-test__btn--block" data-calma-start hidden>.*?</button>', intro, re.S).group(0)
    pasos = [
        (org_generacion, '<strong>Eliges tu generación</strong> para personalizar el contexto', 'psicologia'),
        (org_preguntas, '<strong>Respondes 12 preguntas</strong> sobre 4 dimensiones de tu vida digital', 'ia'),
        (org_perfil, '<strong>Obtienes tu perfil</strong> con análisis y recomendaciones concretas', 'neurociencia'),
    ]
    lis = ''.join(f'<li class="calma-test__paso calma-tono--{tono}" style="--i:{i}">{fig()}'
                  f'<span class="calma-test__num" aria-hidden="true">{i + 1}</span><span>{texto}</span></li>'
                  for i, (fig, texto, tono) in enumerate(pasos))
    nueva = f'''<section class="calma-test__intro" data-calma-intro aria-labelledby="calma-test-antes">
<div class="calma-test__card calma-test__antes calma-tono--bienestar">{org_pausa()}<div>
<h2 id="calma-test-antes" tabindex="-1">Antes de empezar</h2>
<p>Este test es <strong>educativo y orientativo</strong>. No reemplaza una evaluación profesional. Se basa en investigación sobre comportamiento digital y está diseñado para invitarte a reflexionar.</p>
</div></div>
<div class="calma-test__bloque">
<h2>Cómo funciona</h2>
<ol class="calma-test__howto">{lis}</ol>
</div>
<div class="calma-test__card calma-test__mide calma-tono--neurociencia"><div>
<h2>Qué mide</h2>
<p>Las 12 preguntas recorren 4 dimensiones de tu vida digital:</p>
<p class="calma-test__placeholder">[COMPLETAR: nombres de las 4 dimensiones que mide el test; el test original no las define]</p>
<p>Cada respuesta suma de 1 a 4 puntos, con un máximo de 48. Tu perfil se calcula a partir del puntaje total.</p>
</div>{org_mide()}</div>
{nojs}
{empezar}
</section>'''
    s = s[:a] + nueva + s[b:]
    return (cabecera('Test de consumo digital',
                     'Reemplaza el bloque "HTML personalizado" del test (Etapa 2) en /test/ (id 1941). Misma lógica y mismos textos;\n'
                     '     cambia la forma (figuras y movimiento). Estilos y movimiento: plugin (calma-etapa7.css y calma-organismo.js).')
            + s)


def dato(cabecera):
    tarjetas = [
        (org_contexto, 'psicologia', 'Contexto colapsado',
         'Lo que compartimos en un contexto (aquí, con intención reflexiva) puede leerse de forma muy distinta en otro (redes, trabajo, familia).'),
        (org_datos, 'ia', 'Datos de comportamiento',
         'Los patrones de consumo digital son datos sensibles. Revelarlos públicamente puede usarse para inferir hábitos, vulnerabilidades o estados emocionales.'),
        (org_reflejo, 'neurociencia', 'El valor está en la reflexión',
         'Este test no está diseñado para compararse con otros. Está diseñado para que cada persona se conozca mejor, a su ritmo y en privado.'),
    ]
    lis = ''.join(f'<li class="calma-dato__tarjeta calma-tono--{tono}" style="--i:{i}">{fig()}<h3>{t}</h3><p>{p}</p></li>'
                  for i, (fig, tono, t, p) in enumerate(tarjetas))
    return (cabecera('Test · Dato que vale la pena saber',
                     'Reemplaza las dos filas de Kadence debajo del test (la imagen con "Dato que vale la pena saber" y las tres cajas con ícono).\n'
                     '     Un bloque "HTML personalizado", ancho completo. Mismo texto y la misma imagen.')
            + f'''<section class="calma-dato" aria-labelledby="calma-dato-h2">
<div class="calma-dato__cabeza">
<figure class="calma-dato__imagen"><img src="https://codigocalma.com/wp-content/uploads/2026/06/test-1.jpg" width="520" height="520" alt="Test de Consumo Digital." loading="lazy" decoding="async"></figure>
<div class="calma-dato__texto">
<h2 id="calma-dato-h2">Dato que vale la pena saber</h2>
<p class="calma-dato__lema">Tus resultados <em>son tuyos.</em></p>
<p>Compartir los resultados de un test puede parecer inofensivo, pero cada vez que lo hacemos estamos construyendo un perfil público de nuestro comportamiento digital que no siempre controlamos.</p>
</div>
</div>
<ul class="calma-dato__tarjetas">{lis}</ul>
</section>
''')
