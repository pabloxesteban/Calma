"""Página pilar «¿Qué es la ciberpsicología?» con el patrón de la Etapa 7.

Mismo texto que la Etapa 5 (contenido/etapa-5/bloques/ciberpsicologia.html):
se toma de ese archivo, no se reescribe. Cambia la forma, con el patrón del
Test: cabecera con figura propia, títulos de sección a la izquierda y tarjetas
con figura animada (clase calma-habito, así heredan la luz, la aparición y la
animación al pasar el puntero).

- La nota interna de implementación (visible hasta ahora) pasa a comentario.
- El comentario anidado «verificar: …» (dejaba «-->» visible) se corrige.
- El mapa de temas se sigue insertando antes de «¿Cómo se ve…?» (id dia-a-dia).
Lo usa generar-bloques.py.
"""
import pathlib
import re

RAIZ = pathlib.Path(__file__).resolve().parents[2]
E5 = RAIZ / 'contenido/etapa-5/bloques/ciberpsicologia.html'


def svg(contenido):
    return ('<svg class="calma-org" viewBox="0 0 160 100" width="160" height="100" aria-hidden="true" focusable="false">'
            + contenido + '</svg>')


# ---------------------------------------------------------------- figuras
def f_revistas():
    return svg('<rect x="44" y="18" width="46" height="62" rx="4"/><rect x="62" y="24" width="46" height="62" rx="4"/>'
               '<path class="o-trazo" pathLength="1" d="M70 40h30M70 50h30M70 60h20"/>')


def f_manual():
    return svg('<path d="M80 26c-12-8-28-8-38-4v56c10-4 26-4 38 4 12-8 28-8 38-4V22c-10-4-26-4-38 4Z"/>'
               '<path class="o-trazo" pathLength="1" d="M80 26v56"/><circle class="o-nucleo" cx="80" cy="18" r="3"/>')


def f_programas():
    return svg('<path d="M80 22 124 40 80 58 36 40Z"/><path class="o-trazo" pathLength="1" d="M56 48v18c14 10 34 10 48 0V48"/>'
               '<path d="M124 40v22"/><circle class="o-nucleo" cx="124" cy="66" r="3"/>')


def f_identidad():
    return svg('<circle cx="64" cy="42" r="12"/><path d="M44 78c2-14 38-14 40 0"/>'
               '<rect class="o-trazo" pathLength="1" x="92" y="30" width="36" height="40" rx="6"/><circle class="o-nucleo" cx="110" cy="46" r="4"/>')


def f_relaciones():
    return svg(''.join(f'<circle class="o-punto" style="--i:{i}" cx="{x}" cy="{y}" r="6"/>' for i, (x, y) in
                       enumerate(((50, 30), (110, 30), (80, 74), (40, 70), (122, 68))))
               + '<path class="o-trazo" pathLength="1" d="M50 30 110 30 80 74 50 30M40 70 80 74 122 68"/>')


def f_salud():
    return svg('<path class="o-trazo" pathLength="1" d="M20 54h28l8-18 12 36 10-26 6 8h56"/><circle class="o-nucleo" cx="140" cy="54" r="4"/>')


def f_juego():
    return svg('<rect x="42" y="34" width="76" height="40" rx="20"/><path d="M60 46v16M52 54h16"/>'
               '<circle class="o-punto" style="--i:0" cx="98" cy="48" r="4"/><circle class="o-punto" style="--i:1" cx="106" cy="58" r="4"/>')


def f_proteccion():
    return svg('<path class="o-trazo" pathLength="1" d="M80 14 108 26v22c0 18-12 30-28 38-16-8-28-20-28-38V26Z"/>'
               '<path class="o-arco" d="M72 50v-6a8 8 0 0 1 16 0v6"/><rect x="68" y="50" width="24" height="18" rx="4"/>')


def f_vida():
    return svg('<path class="o-trazo" pathLength="1" d="M20 70C50 70 50 30 80 30s30 40 60 40"/>'
               + ''.join(f'<circle class="o-punto" style="--i:{i}" cx="{x}" cy="{y}" r="{r}"/>' for i, (x, y, r) in
                         enumerate(((30, 70, 4), (80, 30, 6), (130, 68, 8)))))


def f_factor(i):
    # Seis factores de Suler: seis variaciones de «persona ↔ pantalla».
    figuras = [
        '<circle cx="60" cy="50" r="16" stroke-dasharray="3 4"/><path class="o-trazo" pathLength="1" d="M84 50h40"/><rect x="124" y="36" width="20" height="28" rx="4"/>',
        '<circle cx="50" cy="50" r="16"/><path d="M34 34l32 32"/><path class="o-trazo" pathLength="1" d="M76 50h44"/><rect x="120" y="36" width="20" height="28" rx="4"/>',
        '<circle cx="40" cy="50" r="10"/><path class="o-trazo" pathLength="1" d="M56 50h24M92 50h24" stroke-dasharray="1"/><circle class="o-punto" style="--i:0" cx="86" cy="50" r="3"/><circle cx="130" cy="50" r="10" stroke-dasharray="3 4"/>',
        '<circle cx="54" cy="50" r="18"/><path class="o-onda" d="M42 50c4-8 8-8 12 0s8 8 12 0"/><circle cx="118" cy="50" r="12" stroke-dasharray="3 4"/>',
        '<circle cx="60" cy="50" r="14"/><path class="o-trazo" pathLength="1" d="M96 26a30 30 0 1 1 0 48"/><circle class="o-nucleo" cx="108" cy="50" r="4"/>',
        '<path d="M50 30h20v40H50zM90 44h20v26H90z"/><path class="o-trazo" pathLength="1" d="M40 74h80"/>',
    ]
    return svg(figuras[i])


def f_dia(i):
    figuras = [
        '<rect x="48" y="16" width="40" height="68" rx="8"/><path class="o-trazo" pathLength="1" d="M58 36h20M58 46h14"/><path class="o-onda" d="M96 50c8-10 16 10 24 0s16 10 24 0"/>',
        '<rect x="62" y="16" width="36" height="68" rx="8"/><path class="o-trazo" pathLength="1" d="M40 60a40 40 0 0 1 20-40M120 20a40 40 0 0 1 0 60"/><circle class="o-nucleo" cx="80" cy="74" r="3"/>',
        '<circle cx="60" cy="40" r="12"/><path d="M40 78c2-14 38-14 40 0"/><path class="o-trazo" pathLength="1" d="M96 70l12-16 10 8 18-26"/>',
        '<rect x="34" y="28" width="92" height="52" rx="6"/><path d="M34 32l46 30 46-30"/><circle class="o-nucleo" cx="126" cy="28" r="7"/>',
        '<circle class="o-trazo" pathLength="1" cx="80" cy="50" r="30"/><path d="M80 32v18l12 8"/><circle class="o-nucleo" cx="80" cy="50" r="3"/>',
    ]
    return svg(figuras[i])


def f_tema(clave):
    figuras = {
        'bienestar': '<circle class="o-anillo" style="--i:0" cx="80" cy="50" r="14"/><circle class="o-anillo" style="--i:1" cx="80" cy="50" r="26"/><circle class="o-anillo" style="--i:2" cx="80" cy="50" r="38"/><circle class="o-nucleo" cx="80" cy="50" r="5"/>',
        'habitos': '<path class="o-trazo" pathLength="1" d="M30 70c20 0 20-40 40-40s20 40 40 40 20-40 30-40"/><circle class="o-nucleo" cx="140" cy="30" r="4"/>',
        'ia': ''.join(f'<circle class="o-punto" style="--i:{i}" cx="{x}" cy="{y}" r="4"/>' for i, (x, y) in enumerate(((40, 30), (40, 70), (80, 20), (80, 50), (80, 80), (120, 40), (120, 60)))) + '<path class="o-trazo" pathLength="1" d="M40 30 80 50 40 70M80 20 120 40 80 50 120 60 80 80"/>',
        'redes': '<circle cx="80" cy="50" r="12"/>' + ''.join(f'<circle class="o-punto" style="--i:{i}" cx="{x}" cy="{y}" r="6"/>' for i, (x, y) in enumerate(((36, 26), (124, 26), (36, 76), (124, 76)))) + '<path class="o-trazo" pathLength="1" d="M42 30 70 44M118 30 90 44M42 72 70 56M118 72 90 56"/>',
        'ciberseguridad': '<path class="o-arco" d="M68 48v-10a12 12 0 0 1 24 0v10"/><rect x="60" y="48" width="40" height="32" rx="6"/><circle class="o-nucleo" cx="80" cy="63" r="4"/>',
        'neurociencia': '<path class="o-trazo" pathLength="1" d="M80 20c-20 0-34 12-34 30s14 30 34 30 34-12 34-30-14-30-34-30ZM80 20v60M60 36c8 4 12 10 12 14M100 36c-8 4-12 10-12 14"/>',
    }
    return svg(figuras[clave])


def f_recurso(i):
    figuras = [
        '<circle cx="12" cy="12" r="8"/><path d="M8 12c1.5-3 2.5-3 4 0s2.5 3 4 0"/>',
        '<rect x="7" y="3" width="10" height="18" rx="2.5"/><path d="M10 7h4M10 10h4M10 13h4"/>',
        '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="4" r="1.3"/><circle cx="20" cy="12" r="1.3"/><circle cx="12" cy="20" r="1.3"/><circle cx="4" cy="12" r="1.3"/>',
        '<path d="M12 4v11M7 11l5 5 5-5M5 20h14"/>',
        '<rect x="4" y="5" width="16" height="14" rx="2"/><path d="M8 9h8M8 12h8M8 15h5"/>',
    ]
    return (f'<span class="calma-test__icono" aria-hidden="true"><svg viewBox="0 0 24 24" width="24" height="24" focusable="false">'
            f'{figuras[i]}</svg></span>')


def figura_cabecera():
    """La mente y la tecnología: una persona, cuatro entornos digitales y las señales que van y vuelven."""
    entornos = [  # (x, y, tono, dibujo del entorno)
        (360, 70, '#bdb0ee', '<rect x="-14" y="-20" width="28" height="40" rx="6"/><circle cx="0" cy="13" r="1.8" class="o-lleno"/>'),
        (400, 180, '#9cc3e3', '<path d="M-16 -6h32v20h-32zM-20 14h40"/>'),
        (360, 290, '#9fd0c0', '<path d="M-14 -12h28v18H2l-8 8v-8h-8z"/>'),
        (250, 330, '#e2c17e', '<path d="M-8 -2v-6a8 8 0 0 1 16 0v6"/><rect x="-12" y="-2" width="24" height="18" rx="4"/>'),
    ]
    lineas, nodos = '', ''
    for i, (x, y, tono, dib) in enumerate(entornos):
        d = f'M150 190 Q{(150 + x) / 2 + 20} {(190 + y) / 2 - 30} {x} {y}'
        lineas += (f'<path class="calma-cp-fig__base" d="{d}"/>'
                   f'<path class="calma-cp-fig__senal" style="--i:{i};--acento:{tono}" pathLength="1" d="{d}"/>')
        nodos += (f'<g class="calma-cp-fig__nodo" style="--i:{i};--acento:{tono}" transform="translate({x} {y})">'
                  f'<circle r="34"/><g class="calma-cp-fig__icono">{dib}</g></g>')
    return ('<div class="calma-hero__media calma-cp-fig" aria-hidden="true">'
            '<svg viewBox="0 0 460 380" width="460" height="380" focusable="false">'
            '<circle class="calma-cp-fig__guia" cx="150" cy="190" r="120"/>'
            f'{lineas}'
            '<g class="calma-cp-fig__persona"><circle class="calma-cp-fig__halo" cx="150" cy="190" r="72"/>'
            '<circle class="calma-cp-fig__halo" cx="150" cy="190" r="54"/>'
            '<circle class="calma-cp-fig__mente" cx="150" cy="190" r="38"/>'
            '<path class="calma-cp-fig__onda" d="M126 190c4-10 8-10 12 0s8 10 12 0 8-10 12 0 8 10 12 0"/></g>'
            f'{nodos}</svg></div>')


# ---------------------------------------------------------------- utilidades
def entre(s, desde, hasta):
    a = s.index(desde)
    return s[a:s.index(hasta, a)]


def lis(bloque):
    return re.findall(r'<li>(.*?)</li>', bloque, re.S)


def tarjeta(fig, tono, titulo, texto, i, chip=None, extra='', tag='h3'):
    chip_html = f'<span class="calma-habito__chip">{chip}</span>' if chip else ''
    return (f'<li class="calma-habito calma-tono--{tono}" style="--i:{i}">{fig}{chip_html}'
            f'<{tag}>{titulo}</{tag}><p>{texto}</p>{extra}</li>')


def partir(li):
    """«<strong>Título:</strong> texto» → (Título, texto)."""
    m = re.match(r'\s*<strong>(.*?)</strong>\s*(.*)', li, re.S)
    titulo = m.group(1).rstrip(':').rstrip().rstrip('.')
    return titulo, mayuscula(m.group(2).strip().lstrip(',').strip())


def mayuscula(t):
    """Primera letra en mayúscula (el texto ya no sigue a un título en la misma línea)."""
    i = 0
    while i < len(t) and (t[i] in '«"' or t[i] == '<'):
        if t[i] == '<':
            i = t.index('>', i) + 1
        else:
            i += 1
    return t[:i] + t[i:i + 1].upper() + t[i + 1:] if i < len(t) else t


TONOS = ['psicologia', 'ia', 'neurociencia', 'bienestar', 'tecnologia']


def pilar(cabecera):
    s = E5.read_text(encoding='utf-8')
    definicion = re.search(r'<p class="calma-definicion">.*?</p>', s, re.S).group(0)
    resumen = re.search(r'<aside class="calma-resumen".*?</aside>', s, re.S).group(0)
    firma = re.search(r'<p><em>Por Tatiana X\. Stacul.*?</em></p>', s, re.S).group(0)

    # ¿De dónde viene?
    origen = entre(s, '<h2>¿De dónde viene la ciberpsicología?</h2>', '<!--')
    origen_ps = re.findall(r'<p>(.*?)</p>', origen, re.S)
    origen_cards = ''.join(
        tarjeta(fig(), TONOS[i], *partir(li), i)
        for i, (fig, li) in enumerate(zip((f_revistas, f_manual, f_programas), lis(origen))))

    # ¿Qué estudia?
    estudia = entre(s, '<h2>¿Qué estudia la ciberpsicología?</h2>', '<h3>Un ejemplo clásico')
    estudia_ps = re.findall(r'<p>(.*?)</p>', estudia, re.S)
    figs = (f_identidad, f_relaciones, f_salud, f_juego, f_proteccion, f_vida)
    estudia_cards = ''.join(tarjeta(figs[i](), (TONOS * 2)[i], *partir(li), i) for i, li in enumerate(lis(estudia)))

    # Suler
    suler = entre(s, '<h3>Un ejemplo clásico', '<h2>Los temas')
    suler_ps = re.findall(r'<p>(.*?)</p>', suler, re.S)
    factores = ''.join(tarjeta(f_factor(i), (TONOS * 2)[i], *partir(li), i, chip=f'Factor {i + 1}', tag='h4')
                       for i, li in enumerate(lis(suler)))

    # Temas
    temas_html = entre(s, '<h2>Los temas de la ciberpsicología en Código Calma</h2>', '<blockquote>')
    temas_intro = re.search(r'</h2>\s*<p>(.*?)</p>', temas_html, re.S).group(1)
    claves = [('bienestar', 'bienestar'), ('habitos', 'psicologia'), ('ia', 'ia'), ('redes', 'tecnologia'),
              ('ciberseguridad', 'neurociencia'), ('neurociencia', 'neurociencia')]
    bloques_tema = re.findall(r'<h3>(.*?)</h3>\s*<p>(.*?)\n→ (.*?)</p>\s*<ul>(.*?)</ul>', temas_html, re.S)
    temas = ''
    for i, ((clave, tono), (nombre, texto, enlaces, ul)) in enumerate(zip(claves, bloques_tema)):
        arts = ''.join(f'<li>{a}</li>' for a in lis(ul))
        temas += (f'<li class="calma-habito calma-tema calma-tono--{tono}" style="--i:{i}">{f_tema(clave)}'
                  f'<h3>{nombre}</h3><p>{texto}</p><ul class="calma-tema__articulos">{arts}</ul>'
                  f'<p class="calma-tema__enlaces">{enlaces}</p></li>')

    # Día a día
    dia = entre(s, '<h2>¿Cómo se ve la ciberpsicología en tu día a día?</h2>', '<h2>Ciberpsicología, psicología clínica')
    dia_ps = re.findall(r'<p>(.*?)</p>', dia, re.S)
    dia_cards = ''.join(tarjeta(f_dia(i), (TONOS * 2)[i], *partir(li), i) for i, li in enumerate(lis(dia)))

    # Diferencias
    dif = entre(s, '<h2>Ciberpsicología, psicología clínica y bienestar digital: ¿en qué se diferencian?</h2>', '<h2>Un mito frecuente')
    dif_intro = re.search(r'</h2>\s*<p>(.*?)</p>', dif, re.S).group(1)
    tabla = re.search(r'<table.*?</table>', dif, re.S).group(0).replace('<table tabindex="0">', '<table class="calma-tabla" tabindex="0">', 1)
    # Etiquetas para leer la tabla como tarjetas en pantallas angostas.
    def etiquetar(fila):
        celdas = re.findall(r'<td>.*?</td>', fila.group(0), re.S)
        if len(celdas) == 3:
            nuevo = fila.group(0).replace(celdas[1], celdas[1].replace('<td>', '<td data-label="Qué es">', 1), 1)
            nuevo = nuevo.replace(celdas[2], celdas[2].replace('<td>', '<td data-label="Pregunta que responde">', 1), 1)
            return nuevo
        return fila.group(0)
    tabla = re.sub(r'<tr>.*?</tr>', etiquetar, tabla, flags=re.S)
    dif_ps = re.findall(r'<p>(.*?)</p>', dif[dif.index('</table>'):dif.index('<blockquote>')], re.S)
    aviso = re.search(r'<blockquote>\s*<p>(.*?)</p>\s*</blockquote>', dif, re.S).group(1)

    # Mito
    mito = entre(s, '<h2>Un mito frecuente: «las horas de pantalla lo explican todo»</h2>', '<h2>Recursos para empezar</h2>')
    mito_intro = re.search(r'</h2>\s*<p>(.*?)</p>', mito, re.S).group(1)
    mito_li = lis(mito)
    mito_cierre = re.findall(r'<p>(.*?)</p>', mito[mito.index('</ul>'):], re.S)[0]
    curva = svg('<path class="o-eje" d="M20 84h124M20 84V14"/><path class="o-trazo" pathLength="1" d="M24 70C50 20 90 20 140 64"/>'
                '<circle class="o-nucleo" cx="68" cy="32" r="4"/>')
    barra = ('<div class="calma-mito__barra" aria-hidden="true"><span class="calma-mito__resto"></span><span class="calma-mito__parte"></span></div>'
             '<p class="calma-mito__cifra" aria-hidden="true"><strong>0,4 %</strong> como mucho</p>')
    mito_cards = (tarjeta(curva, 'psicologia', *partir(mito_li[0]), 0)
                  + tarjeta(barra, 'ia', *partir(mito_li[1]), 1))

    # Recursos
    rec = entre(s, '<h2>Recursos para empezar</h2>', '<h2>Preguntas frecuentes</h2>')
    recursos = ''
    for i, li in enumerate(lis(rec)):
        m = re.match(r'<strong><a href="([^"]+)">(.*?)</a>:</strong>\s*(.*)', li, re.S)
        href, nombre, texto = m.groups()
        tono = TONOS[i % 5]
        recursos += (f'<li class="calma-recurso calma-tono--{tono}"><a class="calma-app__enlace" href="{href}">{f_recurso(i)}'
                     f'<span class="calma-app__nombre">{nombre}</span><span class="calma-app__desc">{mayuscula(texto)}</span>'
                     f'<span class="calma-app__ir calma-app__ir--interno" aria-hidden="true"></span></a></li>')

    # Preguntas frecuentes
    faq = entre(s, '<h2>Preguntas frecuentes</h2>', '<h2>Fuentes</h2>')
    preguntas = ''.join(f'<details><summary><h3>{q}</h3></summary><div><p>{a}</p></div></details>'
                        for q, a in re.findall(r'<h3>(.*?)</h3>\s*<p>(.*?)</p>', faq, re.S))

    # Fuentes, autoría y cierre
    fuentes = re.search(r'<h2>Fuentes</h2>\s*(<ol>.*?</ol>)', s, re.S).group(1)
    autoria = re.findall(r'</ol>\s*(<p>.*?</p>)\s*(<p>.*?</p>)', s[s.index('<h2>Fuentes</h2>'):], re.S)[0]
    cierre = entre(s, '<h2>¿Quieres trabajarlo uno a uno?</h2>', '</div></article>')
    cierre_ps = re.findall(r'<p>(.*?)</p>', cierre, re.S)

    return (cabecera('Ciberpsicología (página pilar)',
                     'Reemplaza TODO el contenido de /ciberpsicologia/ (el bloque de la Etapa 5). Un solo bloque "HTML personalizado", ancho completo, sin caja, título de Kadence oculto.\n'
                     '     Mismo texto que la Etapa 5; cambia la forma. Entre "Los temas…" y "¿Cómo se ve…?" va un bloque Código corto con [calma_mapa] (ver Paso 3c).\n'
                     '     Nota de la Etapa 5 que sigue vigente: debajo de cada área se puede sumar un bloque Kadence Posts filtrado por categoría (3 entradas) para que la lista se actualice sola.')
            + f'''<div class="calma-page calma-recursos calma-pilar">
<!-- verificar: fecha y autoría del primer uso del término «ciberpsicología». Si no se encuentra una fuente fiable, este dato queda fuera. -->
<section class="calma-hero" aria-labelledby="pilar-h1"><div class="calma-hero__inner calma-hero__inner--media"><div>
<h1 id="pilar-h1">¿Qué es la <em>ciberpsicología</em>?</h1>
{definicion.replace('class="calma-definicion"', 'class="calma-definicion calma-hero__lead"', 1)}
<div class="calma-pilar__firma">{firma}</div>
</div>{figura_cabecera()}</div></section>

<section class="calma-section calma-pilar__resumen" aria-label="En resumen"><div class="calma-container">{resumen}</div></section>

<section class="calma-section" aria-labelledby="origen-h2"><div class="calma-container">
<div class="calma-section__head"><h2 id="origen-h2">¿De dónde viene la <em>ciberpsicología</em>?</h2>
<p>{origen_ps[0]}</p><p>{origen_ps[1]}</p></div>
<ul class="calma-habitos">{origen_cards}</ul>
</div></section>

<section class="calma-section" aria-labelledby="estudia-h2"><div class="calma-container">
<div class="calma-section__head"><h2 id="estudia-h2">¿Qué estudia la <em>ciberpsicología</em>?</h2><p>{estudia_ps[0]}</p></div>
<ul class="calma-habitos">{estudia_cards}</ul>
<p class="calma-recursos__nota">{estudia_ps[1]}</p>
</div></section>

<section class="calma-section" aria-labelledby="suler-h3"><div class="calma-container">
<div class="calma-section__head"><h3 id="suler-h3" class="calma-pilar__h3">Un ejemplo clásico: el efecto de desinhibición en línea</h3><p>{suler_ps[0]}</p></div>
<ol class="calma-habitos calma-habitos--factores">{factores}</ol>
<p class="calma-pilar__cierre">{suler_ps[1]}</p>
</div></section>

<section class="calma-section" aria-labelledby="temas-h2"><div class="calma-container">
<div class="calma-section__head"><h2 id="temas-h2">Los temas de la ciberpsicología en <em>Código Calma</em></h2><p>{temas_intro}</p></div>
<ul class="calma-habitos calma-temas">{temas}</ul>
</div></section>

<section class="calma-section" id="dia-a-dia" aria-labelledby="dia-h2"><div class="calma-container">
<div class="calma-section__head"><h2 id="dia-h2">¿Cómo se ve la ciberpsicología en tu <em>día a día</em>?</h2><p>{dia_ps[0]}</p></div>
<ul class="calma-habitos">{dia_cards}</ul>
<p class="calma-recursos__nota">{dia_ps[1]}</p>
</div></section>

<section class="calma-section" aria-labelledby="dif-h2"><div class="calma-container">
<div class="calma-section__head"><h2 id="dif-h2">Ciberpsicología, psicología clínica y bienestar digital: <em>¿en qué se diferencian?</em></h2><p>{dif_intro}</p></div>
{tabla}
<div class="calma-pilar__prosa">{''.join(f'<p>{p}</p>' for p in dif_ps)}</div>
<p class="calma-notice calma-recursos__aviso">{aviso}</p>
</div></section>

<section class="calma-section" aria-labelledby="mito-h2"><div class="calma-container">
<div class="calma-section__head"><h2 id="mito-h2">Un mito frecuente: <em>«las horas de pantalla lo explican todo»</em></h2><p>{mito_intro}</p></div>
<ul class="calma-habitos calma-habitos--2">{mito_cards}</ul>
<p class="calma-pilar__cierre">{mito_cierre}</p>
</div></section>

<section class="calma-section" aria-labelledby="recursos-h2"><div class="calma-container calma-apps calma-tono--neurociencia">
<h2 class="calma-apps__titulo" id="recursos-h2">Recursos para empezar</h2>
<ul class="calma-apps__lista">{recursos}</ul>
</div></section>

<section class="calma-section" aria-labelledby="faq-h2"><div class="calma-container calma-pilar__faq">
<div class="calma-section__head"><h2 id="faq-h2">Preguntas <em>frecuentes</em></h2></div>
<div class="calma-faq">{preguntas}</div>
</div></section>

<section class="calma-section" aria-labelledby="fuentes-h2"><div class="calma-container">
<div class="calma-section__head"><h2 id="fuentes-h2">Fuentes</h2></div>
<div class="calma-pilar__fuentes">{fuentes}</div>
<div class="calma-pilar__autoria">{autoria[0]}{autoria[1]}</div>
</div></section>

<section class="calma-section"><div class="calma-container calma-cta">
<h2>¿Quieres trabajarlo uno a uno?</h2>
<p>{cierre_ps[0]}</p>
<p class="calma-actions"><a class="calma-btn calma-btn--on-dark" href="https://codigocalma.com/contacto/">Escribirnos</a> <a class="calma-link" href="https://codigocalma.com/servicios/">Ver servicios</a></p>
<p class="calma-micro">{cierre_ps[2]}</p>
</div></section>
</div>
''')
