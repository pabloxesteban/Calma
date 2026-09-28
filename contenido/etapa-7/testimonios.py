"""Testimonios con el patrón de la Etapa 7.

Las reseñas son las 14 que hoy están publicadas en /testimonios/ (texto,
nombre, 5 estrellas y enlace a la reseña en Google), copiadas tal cual en
testimonios.json. No se edita el texto de nadie; solo se corrige la comilla
de cierre de la primera («…«  →  «…»). Las fotos de ambiente que acompañaban
cada reseña se quitan: no son de las personas y hacían ver la página como un
blog.

- Cabecera: título, bajada y una figura: catorce puntos (uno por reseña) que
  se encienden alrededor de unas comillas.
- Reseñas en tarjetas de distinto alto (columnas tipo muro), con las cinco
  estrellas como texto accesible, la cita, el nombre y el enlace a Google.
Lo usa generar-bloques.py.
"""
import html
import json
import math
import pathlib

DATOS = pathlib.Path(__file__).with_name('testimonios.json')
TONOS = [('psicologia', '#e2c17e'), ('ia', '#bdb0ee'), ('neurociencia', '#9cc3e3'), ('bienestar', '#9fd0c0'), ('tecnologia', '#ebb79c')]


def e(t):
    return html.escape(t, quote=True)


def estrellas():
    estrella = '<path d="M8 1.5l1.9 4 4.4.5-3.3 3 .9 4.3L8 11.1 4.1 13.3l.9-4.3-3.3-3 4.4-.5Z"/>'
    return ('<p class="calma-resena__estrellas"><span class="screen-reader-text">5 de 5 estrellas</span>'
            + ''.join(f'<svg viewBox="0 0 16 16" width="16" height="16" aria-hidden="true" focusable="false">{estrella}</svg>' for _ in range(5))
            + '</p>')


def figura(n):
    puntos = ''
    for i in range(n):
        a = math.radians(-90 + i * 360 / n)
        tono = TONOS[i % len(TONOS)][1]
        puntos += (f'<circle class="calma-resenas-fig__punto" style="--i:{i};--acento:{tono}" '
                   f'cx="{150 + 112 * math.cos(a):.1f}" cy="{150 + 112 * math.sin(a):.1f}" r="9"/>')
    return ('<div class="calma-hero__media calma-resenas-fig" aria-hidden="true"><svg viewBox="0 0 300 300" width="300" height="300" focusable="false">'
            '<circle class="calma-resenas-fig__guia" cx="150" cy="150" r="112"/>' + puntos +
            '<circle class="calma-resenas-fig__halo" cx="150" cy="150" r="62"/>'
            '<circle class="calma-resenas-fig__centro" cx="150" cy="150" r="46"/>'
            '<text class="calma-resenas-fig__comillas" x="150" y="178" text-anchor="middle">«»</text></svg></div>')


def testimonios(cabecera):
    resenas = json.loads(DATOS.read_text(encoding='utf-8'))
    tarjetas = ''
    for i, r in enumerate(resenas):
        texto = r['texto'].strip()
        if texto.endswith('«'):
            texto = texto[:-1].rstrip() + '»'
        tono = TONOS[i % len(TONOS)][0]
        tarjetas += (f'<li class="calma-habito calma-resena calma-tono--{tono}" style="--i:{i}">'
                     f'<figure>{estrellas()}<blockquote><p>{e(texto)}</p></blockquote>'
                     f'<figcaption><span class="calma-resena__inicial" aria-hidden="true">{e(r["nombre"][:1])}</span>'
                     f'<strong>{e(r["nombre"].strip())}</strong>'
                     f'<a href="{e(r["enlace"])}" rel="noopener" target="_blank">Ver reseña en Google'
                     f'<span class="screen-reader-text"> de {e(r["nombre"].strip())} (se abre en una pestaña nueva)</span></a></figcaption>'
                     f'</figure></li>')
    return (cabecera('Testimonios',
                     'Reemplaza TODO el contenido de Testimonios (el bloque de testimonios de Kadence y las fotos). Un solo bloque "HTML personalizado", ancho completo, sin caja ni título de Kadence.\n'
                     '     Mismas 14 reseñas publicadas (texto sin cambios). Si se suma una reseña nueva, agregarla en contenido/etapa-7/testimonios.json y regenerar.')
            + f'''<div class="calma-page calma-recursos calma-testimonios">
<section class="calma-hero" aria-labelledby="testimonios-h1"><div class="calma-hero__inner calma-hero__inner--media"><div>
<h1 id="testimonios-h1"><em>Testimonios</em></h1>
<p class="calma-hero__lead">Lo que cuentan quienes trabajaron con Tatiana X. Stacul. Reseñas publicadas en Google.</p>
<p class="calma-testimonios__dato">{len(resenas)} reseñas · 5 de 5 estrellas en todas</p>
</div>{figura(len(resenas))}</div></section>
<section class="calma-section" aria-label="Reseñas"><div class="calma-container">
<ul class="calma-resenas">{tarjetas}</ul>
</div></section>
<section class="calma-section"><div class="calma-container calma-cta">
<h2>¿Quieres consultar con Tatiana?</h2>
<p>Te respondemos en 48 horas hábiles. Si vemos que este no es el lugar, también te lo decimos.</p>
<p class="calma-actions"><a class="calma-btn calma-btn--on-dark" href="https://codigocalma.com/contacto/?area=habitos">Consultar con Tatiana</a></p>
</div></section>
</div>
''')
